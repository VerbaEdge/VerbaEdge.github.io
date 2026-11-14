#!/usr/bin/env python3
"""Read-only main-site acceptance checks against the reviewed activation tree."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import ssl
import subprocess
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlsplit
from urllib.request import build_opener, HTTPRedirectHandler, HTTPSHandler, Request


class RedirectTrace(HTTPRedirectHandler):
    def __init__(self):
        self.hops = []

    def redirect_request(self, request, response, code, message, headers, new_url):
        self.hops.append({"status": code, "from": request.full_url, "to": new_url})
        return super().redirect_request(request, response, code, message, headers, new_url)


class Metadata(HTMLParser):
    def __init__(self, body):
        super().__init__(convert_charrefs=True)
        self.ids, self.canonical, self.refresh, self.hrefs = set(), [], [], []
        self.noindex, self.h1 = False, 0
        self.feed(body.decode("utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "h1":
            self.h1 += 1
        if "href" in attrs:
            self.hrefs.append(attrs["href"])
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonical.append(attrs.get("href", ""))
        if tag == "meta":
            if attrs.get("name", "").lower() == "robots":
                self.noindex = "noindex" in attrs.get("content", "").lower()
            if attrs.get("http-equiv", "").lower() == "refresh":
                value = attrs.get("content", "")
                if ";" in value and value.split(";", 1)[1].strip().lower().startswith("url="):
                    self.refresh.append(value.split(";", 1)[1].strip()[4:])


def sha(body):
    return hashlib.sha256(body).hexdigest()


def fetch(url):
    trace = RedirectTrace()
    opener = build_opener(trace, HTTPSHandler(context=ssl.create_default_context()))
    result = {"url": url, "redirects": trace.hops}
    body = b""
    try:
        request = Request(url, headers={"User-Agent": "VerbaEdge deployment acceptance check", "Cache-Control": "no-cache"})
        with opener.open(request, timeout=30) as response:
            body = response.read(12_000_001)
            if len(body) > 12_000_000:
                raise ValueError("Response exceeds acceptance-check limit")
            result.update(status=response.status, final_url=response.url,
                          content_type=response.headers.get("Content-Type"),
                          sha256=sha(body), bytes=len(body))
    except HTTPError as error:
        result.update(status=error.code, final_url=error.url, error=str(error))
    except (URLError, OSError, ValueError) as error:
        result.update(error=str(error))
    return result, body


def main(args):
    source = args.source.resolve()
    baseline = json.loads((source / "website-package/preserved-files.json").read_text())
    activation = json.loads((source / "website-package/activation-provenance.json").read_text())
    expected = {**baseline["files"], **activation["activation_files"]}
    errors = []
    for name, digest in expected.items():
        if not (source / name).is_file() or sha((source / name).read_bytes()) != digest:
            errors.append(f"Local candidate no longer matches reviewed manifest: {name}")
    if len(expected) != 20:
        errors.append(f"Expected 20 publishing files; found {len(expected)}")
    if errors:
        raise ValueError("; ".join(errors))

    origin = args.origin.rstrip("/") + "/"
    checks = [(name, urljoin(origin, quote(name)), digest)
              for name, digest in sorted(expected.items()) if name not in {"CNAME", ".nojekyll"}]
    checks += [("/", origin, expected["index.html"]),
               ("/engineering/", urljoin(origin, "engineering/"), expected["engineering/index.html"])]
    bodies, responses = {}, []

    def inspect(check):
        name, url, expected_hash = check
        response, body = fetch(url)
        response.update(path=name, expected_sha256=expected_hash)
        response["passed"] = (response.get("status") == 200
                              and response.get("sha256") == expected_hash
                              and urlsplit(response.get("final_url", "")).scheme == "https")
        return name, response, body

    with ThreadPoolExecutor(max_workers=4) as executor:
        for name, response, body in executor.map(inspect, checks):
            responses.append(response)
            bodies[name] = body
            if not response["passed"]:
                errors.append(f"HTTPS body/status mismatch: {name}")

    metadata_checks = []
    required_ids = {"top", "offers", "services", "capabilities", "portfolio", "industries", "contact"}
    for name, canonical, noindex in (("/", "https://verbaedge.com/", False),
                                     ("/engineering/", "https://verbaedge.com/engineering/", True)):
        page = Metadata(bodies[name])
        passed = required_ids.issubset(page.ids) and page.canonical == [canonical] and page.h1 == 1
        if noindex:
            passed = passed and page.noindex
        check = {"path": name, "passed": passed, "missing_legacy_ids": sorted(required_ids - page.ids),
                 "canonical": page.canonical, "noindex": page.noindex, "h1": page.h1}
        metadata_checks.append(check)
        if not passed:
            errors.append(f"Metadata or legacy anchor mismatch: {name}")

    redirect_destinations = []
    for name in ("access-control.html", "citation-context.html", "retrieval-metadata.html"):
        path = "portfolio/" + name
        target = "https://systems.verbaedge.com/portfolio/" + name
        page = Metadata(bodies[path])
        metadata_ok = page.refresh == [target] and target in page.hrefs
        response, _ = fetch(target)
        target_hash = sha((source / "website-package/sites/systems/portfolio" / name).read_bytes())
        passed = (metadata_ok and response.get("status") == 200 and response.get("sha256") == target_hash
                  and urlsplit(response.get("final_url", "")).scheme == "https")
        redirect_destinations.append({"path": path, "meta_refresh": page.refresh,
                                      "fallback_href_present": target in page.hrefs,
                                      "destination": response, "expected_sha256": target_hash, "passed": passed})
        if not passed:
            errors.append(f"Portfolio meta-refresh or destination mismatch: {path}")

    # Report observed behavior without assuming that www or HTTP is configured
    # identically to the apex. These observations are separate from content passes.
    policy_observations = []
    for url in ("http://verbaedge.com/", "https://www.verbaedge.com/", "http://www.verbaedge.com/"):
        response, _ = fetch(url)
        final = urlsplit(response.get("final_url", ""))
        response.update(final_scheme=final.scheme, final_host=final.hostname,
                        activation_body_matches=response.get("sha256") == expected["index.html"])
        policy_observations.append(response)

    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "candidate_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip(),
        "origin": origin,
        "expected_repository_files": len(expected),
        "repository_only_configuration": ["CNAME", ".nojekyll"],
        "https_content_checks": responses,
        "metadata_checks": metadata_checks,
        "portfolio_destination_checks": redirect_destinations,
        "redirect_policy_observations": policy_observations,
        "errors": errors,
        "passed": not errors,
        "scope": "HTTP content, hashes, metadata and redirect observations through the inherited network path with default TLS verification. No browser QA or direct-origin TLS verification; no configuration changes.",
    }
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return bool(errors)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--origin", default="https://verbaedge.com/")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        raise SystemExit(main(args))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(1, f"Acceptance-check error: {error}\n")
