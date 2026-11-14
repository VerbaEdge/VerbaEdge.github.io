# Main homepage activation record

Main activation [PR #2](https://github.com/VerbaEdge/VerbaEdge.github.io/pull/2)
merged as `46d624503c86ec27ec3dcddee0bea8e1a2150076` after owner authorization
and successful checks of both custom subdomains. GitHub Pages built that exact
commit at `2026-11-14T06:57:20Z`. The final regression passed all 20 main
content/alias checks, three portfolio destinations, original anchors and
metadata, and apex/www HTTPS redirects.

The complete original engineering website is preserved at `/engineering/`.
All eleven original protected files other than the homepage remain unchanged,
including the main CNAME.
See [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md) for the final rollout record,
remaining subsite Enforce HTTPS settings, and verification limitations.

## Published compatibility changes

The supplied main public site is overlaid onto the publishing root. Existing
assets, the original `styles.css`, and the root `CNAME` bytes are retained. No
files are removed. The original main package under `sites/main/` remains intact
as the supplied source candidate.

The root homepage adds visible Engineering portfolio navigation, the three
original work sample titles and images, their original non-client-work
qualification, and links to the Systems portfolio and existing Upwork agency.
The original `#top`, `#offers`, `#services`, `#capabilities`, `#portfolio`,
`#industries`, and `#contact` targets remain meaningful. Engineering service,
engagement, capability, and industry links lead to both the corresponding
Systems sections and the preserved original overview.

`engineering/index.html` preserves the complete original page, including its
portfolio descriptions and service content. Only relative asset paths and
archive metadata change: paths use `../`, robots is `noindex, follow`, and the
canonical/Open Graph URL identifies `/engineering/`. There is no archive CNAME.
Noindex is indexing guidance, not an access control.

`activation-provenance.json` records the distinct activation overlay and archive
hashes. The original `preserved-files.json` and source provenance stay unchanged.

## Checks and rollout gate

```sh
python3 -B scripts/verify_website_package.py --activated-main
node scripts/test_demos.cjs
python3 -B scripts/test_rag_projects.py
git diff --check
```

The explicit activation mode checks the other eleven original protected file
hashes, the exact main overlay and CNAME, canonical URL, compatibility anchors,
and local page/asset links. It also reverses the documented archive metadata and
path adjustments to verify the complete original page against its original
hash. Running without `--activated-main` intentionally flags the changed root
homepage against the historical baseline.

Static checks do not establish live deployment or browser behavior. Both
subdomains have now passed all 32 HTTPS root/asset response and hash checks,
including downloads, demos, and French routes. The result is recorded in
`custom-subdomains-validation.json`. Existing approval applied to the completed activation. Browser/keyboard review
and independent origin certificate inspection remain unperformed. The deployed
main page and archive passed the recorded post-merge checks.

## Rollback

The live homepage is the integrated overview; the original complete page is
preserved under `/engineering/`. For an activation regression, revert the activation merge or
restore the original root `index.html` from the pre-edit backup or baseline
commit `b7ae70f7afcfd40ab120bf11b0c389dbab00dc06` through the authorized review
workflow. Retain the original assets, stylesheet, and CNAME. Restoring website
source does not restore external DNS or Pages settings; use recorded settings
for any configuration rollback.
