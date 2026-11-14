#!/usr/bin/env python3
"""Check preservation and all three static site trees without changing hosting."""
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ORIGINS = {"verbaedge.com": "main", "systems.verbaedge.com": "systems", "logistics.verbaedge.com": "logistics"}
EXPECTED_EDITS = {"main/site.css", "logistics/site.css", "logistics/sitemap.xml", "logistics/fr/facturation/index.html"}


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.ids, self.duplicates, self.refs = set(), [], []
        self.h1, self.lang, self.noindex = 0, None, False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "h1":
            self.h1 += 1
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.duplicates.append(attrs["id"])
            self.ids.add(attrs["id"])
        for key in ("href", "src"):
            if attrs.get(key):
                self.refs.append(attrs[key])
        if tag == "meta":
            if attrs.get("name", "").lower() == "robots":
                self.noindex = "noindex" in attrs.get("content", "").lower()
            if attrs.get("http-equiv", "").lower() == "refresh":
                match = re.search(r"url=(.*)", attrs.get("content", ""), re.I)
                if match:
                    self.refs.append(match[1])


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(sites, variant="source"):
    errors, counts = [], {}
    baseline = json.loads((ROOT / "website-package/preserved-files.json").read_text())
    for name, expected in baseline["files"].items():
        path = ROOT / name
        if not path.is_file() or digest(path) != expected:
            errors.append(f"Protected publishing file changed or missing: {name}")

    pages = {path.resolve(): Page(path.read_text()) for path in sites.rglob("*.html")}

    def resolve(reference, current):
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            if url.scheme not in ("https", "http", "mailto", "tel", "data"):
                errors.append(f"Unsupported link in {current}: {reference}")
            if url.hostname not in ORIGINS:
                return
            target = sites / ORIGINS[url.hostname] / unquote(url.path.lstrip("/"))
        else:
            # Relative paths must stay usable at temporary GitHub Pages project URLs.
            if url.path.startswith("/"):
                errors.append(f"Root-relative link will fail at project Pages URL: {current}: {reference}")
                return
            target = current.parent / unquote(url.path) if url.path else current
        target = target.resolve()
        if not target.is_relative_to(sites.resolve()):
            errors.append(f"Link escapes site package: {current}: {reference}")
            return
        if target.is_dir():
            target = target / "index.html"
        if not target.is_file():
            errors.append(f"Missing reference from {current.relative_to(sites)}: {reference}")
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f"Missing fragment from {current.relative_to(sites)}: {reference}")

    for path, page in pages.items():
        if page.h1 != 1 or page.duplicates or not page.lang:
            errors.append(f"Invalid heading, IDs, or language: {path.relative_to(sites)}")
        if variant == "preview" and not page.noindex:
            errors.append(f"Preview page lacks noindex: {path.relative_to(sites)}")
        for reference in page.refs:
            resolve(reference, path)
        # Structured metadata must remain parseable.
        for data in re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', path.read_text(), re.S | re.I):
            try:
                json.loads(data)
            except ValueError:
                errors.append(f"Invalid JSON-LD: {path.relative_to(sites)}")

    for site in ORIGINS.values():
        directory = sites / site
        if not (directory / "index.html").is_file() or not (directory / ".nojekyll").is_file():
            errors.append(f"Missing standalone publishing root: {site}")
        cname = directory / "CNAME"
        if site != "main" and cname.exists():
            errors.append(f"Unapproved subdomain CNAME: {site}")
        if site == "main" and variant != "preview" and (not cname.exists() or cname.read_bytes() != (ROOT / "CNAME").read_bytes()):
            errors.append("Main candidate CNAME differs from the original")
        if variant == "preview" and cname.exists():
            errors.append("Preview must not contain a CNAME")
        for path in directory.rglob("*.css"):
            for reference in re.findall(r'url\(["\']?([^\)"\']+)', path.read_text()):
                resolve(reference, path)
        sitemap = directory / "sitemap.xml"
        if variant != "preview":
            try:
                for node in ET.parse(sitemap).iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
                    reference = node.text or ""
                    resolve(reference, directory / "index.html")
                    url = urlsplit(reference)
                    target = (directory / url.path.lstrip("/")).resolve()
                    if target.is_dir():
                        target /= "index.html"
                    if target in pages and pages[target].noindex:
                        errors.append(f"Sitemap lists a noindex page: {reference}")
            except (OSError, ET.ParseError) as error:
                errors.append(f"Invalid sitemap for {site}: {error}")
        files = [p for p in directory.rglob("*") if p.is_file()]
        for path in files:
            if re.search(r"private|finance.ops|strategy|forecast_assumptions|risk_register|pipeline_template|governance", path.relative_to(directory).as_posix(), re.I):
                errors.append(f"Private material in public tree: {path}")
        counts[site] = {"files": len(files), "html_pages": sum(p.suffix == ".html" for p in files)}

    if variant == "source":
        provenance = json.loads((ROOT / "website-package/source-provenance.json").read_text())
        actual_edits = set()
        for site, originals in provenance["original_public_files"].items():
            actual_names = {p.relative_to(sites / site).as_posix() for p in (sites / site).rglob("*") if p.is_file()}
            if actual_names != set(originals):
                errors.append(f"Unexpected added or removed source files: {site}")
            for name, original_hash in originals.items():
                path = sites / site / name
                if path.exists() and digest(path) != original_hash:
                    actual_edits.add(f"{site}/{name}")
        if actual_edits != EXPECTED_EDITS:
            errors.append(f"Source changes differ from reviewed fixes: {sorted(actual_edits)}")
        # Both new and pre-existing portfolio image bytes are retained.
        for path in (ROOT / "assets/portfolio").iterdir():
            if digest(path) != digest(sites / "systems/assets/portfolio" / path.name):
                errors.append(f"Original portfolio image changed: {path.name}")
    result = {"variant": variant, "protected_files": len(baseline["files"]), "sites": counts, "errors": errors,
              "scope": "Static preservation, links, assets, metadata and public-tree checks; not browser or deployed subdomain acceptance."}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sites", type=Path, default=ROOT / "website-package/sites")
    parser.add_argument("--variant", choices=("source", "release", "preview"), default="source")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = verify(args.sites.resolve(), args.variant)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["errors"]))
