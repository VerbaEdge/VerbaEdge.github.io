#!/usr/bin/env python3
"""Export the three reviewed sites for offline review; never deploy anything."""
import argparse
import hashlib
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITES = ROOT / "website-package/sites"
ORIGINS = {
    "verbaedge.com": "main",
    "systems.verbaedge.com": "systems",
    "logistics.verbaedge.com": "logistics",
}


def local_link(match, current):
    url = urlsplit(match.group())
    target = ORIGINS[url.hostname] + "/" + url.path.lstrip("/")
    if url.path.endswith("/"):
        target += "index.html"
    relative = posixpath.relpath(target, posixpath.dirname(current))
    return relative + ("?" + url.query if url.query else "") + ("#" + url.fragment if url.fragment else "")


def export(output):
    output = output.resolve()
    if output.is_relative_to(ROOT) or output == ROOT.parent:
        raise ValueError("Export outside the repository, in a new empty directory.")
    if output.exists() and any(output.iterdir()):
        raise ValueError("Output must be a new or empty directory; existing exports are never overwritten.")
    output.mkdir(parents=True, exist_ok=True)
    for variant in ("release", "preview"):
        shutil.copytree(SITES, output / variant)
    for page in (output / "preview").rglob("*.html"):
        content = page.read_text()
        # Preview has no production indexing/canonical metadata.
        for attribute in ('name=["\']robots["\']', 'property=["\']og:url["\']'):
            content = re.sub(r"<meta\b(?=[^>]*" + attribute + r")[^>]*>", "", content, flags=re.I)
        content = re.sub(r"<link\b(?=[^>]*rel=[\"']canonical[\"'])[^>]*>", "", content, flags=re.I)
        content = re.sub(r"</head>", '<meta name="robots" content="noindex,nofollow"></head>', content, count=1, flags=re.I)
        current = page.relative_to(output / "preview").as_posix()
        content = re.sub(r'https://(?:systems\.|logistics\.)?verbaedge\.com/[^\s"\'<>]*', lambda m: local_link(m, current), content)
        page.write_text(content)
    for site in ORIGINS.values():
        preview = output / "preview" / site
        (preview / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
        (preview / "sitemap.xml").unlink(missing_ok=True)
        (preview / "CNAME").unlink(missing_ok=True)
    (output / "preview/index.html").write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>VerbaEdge package review</title><style>body{font:18px/1.6 system-ui;background:#091321;color:#edf3fb;max-width:760px;margin:60px auto;padding:24px}a{color:#5eead4}</style></head><body><main><h1>VerbaEdge three-site review</h1><p>Local review copies. Proposed subdomains remain unconfigured. No publishing or DNS changes have been made.</p><ul><li><a href="main/">Main site candidate — activate last</a></li><li><a href="systems/">VerbaEdge Systems</a></li><li><a href="logistics/">Trade &amp; Logistics Technology</a></li></ul><p>The current production homepage is preserved in the repository and backup.</p></main></body></html>''')
    (output / "README.txt").write_text(
        "VerbaEdge review package — no deployment performed.\n"
        "preview/: local cross-site navigation; noindex, no CNAME, no sitemap.\n"
        "release/: three standalone publishing roots, with intended live links.\n"
        "Do not upload this whole directory over the existing site.\n"
        "Systems and Logistics have no CNAME until approved configuration.\n"
        "Obtain approval before merging or changing live settings. Test BOTH subdomains before activating main.\n"
        "noindex is not access control; these files contain public website material only.\n"
    )
    manifest = {p.relative_to(output).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(output.rglob("*")) if p.is_file()}
    (output / "checksums.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Exported release/ and preview/ to {output}; no remote changes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        export(args.output)
    except ValueError as error:
        parser.error(str(error))
