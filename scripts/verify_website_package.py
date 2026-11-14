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
        self.canonical = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "h1":
            self.h1 += 1
        if tag == "link" and "canonical" in attrs.get("rel", "").lower().split():
            self.canonical.append(attrs.get("href", ""))
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


def verify_activation(baseline, errors):
    """Check the explicit activation overlay while retaining historical pins."""
    provenance_path = ROOT / "website-package/activation-provenance.json"
    if not provenance_path.is_file():
        errors.append("Activation provenance is missing")
        return
    provenance = json.loads(provenance_path.read_text())
    for name, expected in provenance["activation_files"].items():
        path = ROOT / name
        if not path.is_file() or digest(path) != expected:
            errors.append(f"Activation file changed or missing: {name}")

    # Every supplied main publishing file is copied exactly except the homepage,
    # whose compatibility additions are pinned in the activation record.
    for source in (ROOT / "website-package/sites/main").rglob("*"):
        if source.is_file() and source.name != "index.html":
            target = ROOT / source.relative_to(ROOT / "website-package/sites/main")
            if not target.is_file() or digest(target) != digest(source):
                errors.append(f"Main overlay differs from reviewed source: {target.relative_to(ROOT)}")

    main_path = ROOT / "index.html"
    engineering_path = ROOT / "engineering/index.html"
    if not main_path.is_file() or not engineering_path.is_file():
        errors.append("Activated homepage or preserved engineering page is missing")
        return
    pages = {path: Page(path.read_text()) for path in (main_path, engineering_path)}
    main, engineering = pages[main_path], pages[engineering_path]
    required_ids = {"top", "offers", "services", "capabilities", "portfolio", "industries", "contact"}
    if not required_ids.issubset(main.ids):
        errors.append(f"Main compatibility anchors missing: {sorted(required_ids - main.ids)}")
    if main.canonical != ["https://verbaedge.com/"]:
        errors.append("Activated main canonical must remain https://verbaedge.com/")
    if not engineering.noindex or not required_ids.issubset(engineering.ids):
        errors.append("Engineering archive must retain original anchors and noindex")
    if (ROOT / "engineering/CNAME").exists():
        errors.append("Engineering archive must not contain a CNAME")

    # Reverse only the documented archive path/metadata adjustments. Everything
    # else, including all original portfolio text, must match the historical page.
    restored = engineering_path.read_text()
    restored = restored.replace('name="robots" content="noindex, follow"', 'name="robots" content="index, follow"')
    restored = restored.replace('property="og:url" content="https://verbaedge.com/engineering/"', 'property="og:url" content="https://verbaedge.com/"')
    restored = restored.replace('  <link rel="canonical" href="https://verbaedge.com/engineering/">\n', "", 1)
    restored = re.sub(r'((?:href|src)=")\.\./', r'\1', restored)
    if hashlib.sha256(restored.encode()).hexdigest() != baseline["files"]["index.html"]:
        errors.append("Preserved engineering page differs from original content")

    for path, page in pages.items():
        if page.h1 != 1 or page.duplicates or not page.lang:
            errors.append(f"Invalid activation page structure: {path.relative_to(ROOT)}")
        for reference in page.refs:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                if url.hostname == "verbaedge.com":
                    target = ROOT / unquote(url.path.lstrip("/"))
                elif url.hostname in ORIGINS:
                    target = ROOT / "website-package/sites" / ORIGINS[url.hostname] / unquote(url.path.lstrip("/"))
                else:
                    continue
            else:
                target = ROOT / unquote(url.path.lstrip("/")) if url.path.startswith("/") else path.parent / unquote(url.path) if url.path else path
            target = target.resolve()
            if not target.is_relative_to(ROOT):
                errors.append(f"Activation reference escapes repository: {reference}")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"Missing activation reference: {path.relative_to(ROOT)}: {reference}")
            elif url.fragment and target.suffix == ".html" and unquote(url.fragment) not in Page(target.read_text()).ids:
                errors.append(f"Missing activation fragment: {reference}")


def verify(sites, variant="source", activated_main=False):
    errors, counts = [], {}
    baseline = json.loads((ROOT / "website-package/preserved-files.json").read_text())
    for name, expected in baseline["files"].items():
        if activated_main and name == "index.html":
            continue
        path = ROOT / name
        if not path.is_file() or digest(path) != expected:
            errors.append(f"Protected publishing file changed or missing: {name}")

    if activated_main:
        verify_activation(baseline, errors)

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
    result = {"variant": variant, "activated_main": activated_main, "protected_files": len(baseline["files"]) - int(activated_main), "sites": counts, "errors": errors,
              "scope": "Static preservation, links, assets, metadata and public-tree checks; not browser or deployed subdomain acceptance."}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sites", type=Path, default=ROOT / "website-package/sites")
    parser.add_argument("--variant", choices=("source", "release", "preview"), default="source")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--activated-main", action="store_true", help="Verify the pinned main activation overlay; retain the other 11 historical publishing pins")
    args = parser.parse_args()
    result = verify(args.sites.resolve(), args.variant, args.activated_main)
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(bool(result["errors"]))
