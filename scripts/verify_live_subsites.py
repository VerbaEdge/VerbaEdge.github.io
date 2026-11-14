#!/usr/bin/env python3
"""Verify both deployed subsite roots and every supplied public site asset."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def check(item):
    site, base, relative, expected = item
    url = urljoin(base.rstrip("/") + "/", quote(relative))
    result = {"site": site, "url": url, "path": relative or "/", "passed": False}
    try:
        request = Request(url, headers={"User-Agent": "VerbaEdge-deployment-verification/1.0"})
        # Inherit the managed network's proxy and trusted CA configuration.
        for attempt in range(3):
            try:
                response = urlopen(request, timeout=15)
                break
            except HTTPError as error:
                if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                    raise
                error.close()
                time.sleep(0.5 * (attempt + 1))
        with response:
            payload = response.read(10_000_001)
            result.update(status=response.status, final_url=response.geturl(),
                          sha256=hashlib.sha256(payload).hexdigest())
            result["passed"] = (response.status == 200 and len(payload) <= 10_000_000
                                and result["sha256"] == hashlib.sha256(expected).hexdigest()
                                and urlsplit(response.geturl()).scheme == "https"
                                and urlsplit(response.geturl()).hostname == urlsplit(base).hostname)
            if not result["passed"]:
                result["error"] = "Response differs from the reviewed file, exceeds the limit, or is not HTTPS."
    except (HTTPError, URLError, TimeoutError, OSError) as error:
        result["error"] = str(error)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--systems-url", default="https://systems.verbaedge.com/")
    parser.add_argument("--logistics-url", default="https://logistics.verbaedge.com/")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    origins = {"systems": args.systems_url, "logistics": args.logistics_url}
    if any(urlsplit(url).scheme != "https" or urlsplit(url).username or urlsplit(url).password
           for url in origins.values()):
        parser.error("Use HTTPS URLs without credentials.")
    source = ROOT / "website-package/sites"
    roots = [(site, url, "", (source / site / "index.html").read_bytes()) for site, url in origins.items()]
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(check, roots))
        # A missing site cannot pass acceptance; avoid fetching all its assets.
        if all(result["passed"] for result in results):
            assets = [(site, url, path.relative_to(source / site).as_posix(), path.read_bytes())
                      for site, url in origins.items() for path in sorted((source / site).rglob("*"))
                      if path.is_file() and path.name not in (".nojekyll", "CNAME")]
            results.extend(pool.map(check, assets))
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "passed": all(result["passed"] for result in results), "checks": results,
              "scope": "HTTP status, redirect destinations, and exact deployed source bytes over trusted proxied HTTPS. Browser behavior and independent origin-certificate inspection are separate checks."}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
