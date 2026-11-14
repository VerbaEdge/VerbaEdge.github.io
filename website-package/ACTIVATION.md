# Main homepage activation candidate

The owner approved merging and deployment in the current conversation; that
approval persists. Repository creation and app access are resolved, and the
source PR #1 is merged in both subsite repositories. Pages enablement still
returns HTTP 403, Resource not accessible by integration, for both repositories;
the owner has been asked to enable Pages from main / (root) in Settings. Both
planned subdomains remained NXDOMAIN at 2026-11-14T06:20:26Z. Main activation
PR #2 remains a draft: this branch prepares the candidate and does not mean
activation has occurred. Enable and test the temporary Pages sites, complete
custom-domain/DNS setup, and pass both subdomain tests before merging.

## Candidate changes

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

Static checks do not establish live deployment, browser behavior, valid
certificates, or working subdomains. Record successful HTTPS tests for
`systems.verbaedge.com` and `logistics.verbaedge.com`, their pages/assets,
downloads/demos, French routes, and inter-site navigation before merging. Review
the main candidate and preserved engineering page on desktop/mobile and with
keyboard navigation. Existing approval remains applicable; the unmet subdomain
test requirement is the reason this branch stays a draft.

## Rollback

The current live homepage remains the original baseline while this draft is
unmerged. After any later activation failure, revert the activation merge or
restore the original root `index.html` from the pre-edit backup or baseline
commit `b7ae70f7afcfd40ab120bf11b0c389dbab00dc06` through the authorized review
workflow. Retain the original assets, stylesheet, and CNAME. Restoring website
source does not restore external DNS or Pages settings; use recorded settings
for any configuration rollback.
