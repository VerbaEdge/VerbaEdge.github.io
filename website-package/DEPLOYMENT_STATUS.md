# Final VerbaEdge deployment record

The integrated main overview is deployed at **https://verbaedge.com/**. Systems
and Trade & Logistics Technology are separate GitHub Pages sites at
**https://systems.verbaedge.com/** and **https://logistics.verbaedge.com/**.
The owner authorized the merges and deployment in the working conversation.

## Published changes

- Prepared the latest supplied integrated ZIP, verified its three public subsets
  against the standalone ZIPs, and confirmed the duplicate main ZIPs are identical.
- Backed up and inspected the original repository before editing. Verified full
  Git-history bundles and source ZIP snapshots were retained, including a fresh
  backup immediately before the final main activation. Both new repositories
  were also backed up before/after source and custom-domain merges.
- Kept Systems and Logistics independent under the original VerbaEdge account.
  All 16 reviewed site files in each match their source hashes; their deployment
  CNAME files are separate from the original supplied source manifest.
- Published the supplied RAG case studies/download, original engineering work
  samples, Logistics shipment/billing demonstrations and French pages.
- Corrected French return navigation, excluded the noindex demo from the sitemap,
  and allowed long brand labels to wrap in the two family stylesheets.
- Activated the main overview after both custom subdomains passed their checks.
  The complete original page is preserved at **https://verbaedge.com/engineering/**.
  All seven original fragment targets, visible portfolio, original image assets,
  branding, stylesheet and exact `verbaedge.com` CNAME are retained.
- Excluded private strategy, finance, mixed management instructions and personal
  records from the public source. No private finance repository was created.
- Used branches and pull requests throughout; no direct source push to main.
  The owner performed the required Pages UI and DNS actions where the app lacked
  service access. Apex/www/email DNS and the main HTTPS setting were preserved.

## Merge and build record

| Change | Pull request | Merge commit |
| --- | --- | --- |
| Main preparation | [Main PR #1](https://github.com/VerbaEdge/VerbaEdge.github.io/pull/1) | `76666e0b5d586f006ea998f3b462892aa96c2306` |
| Systems source | [Systems PR #1](https://github.com/VerbaEdge/verbaedge-systems/pull/1) | `1044c892a66d9cf19a25c025f88fce3bf580fa20` |
| Logistics source | [Logistics PR #1](https://github.com/VerbaEdge/verbaedge-logistics/pull/1) | `7be3d33251d1ca33b07b289ec43d904bb16c9950` |
| Systems custom domain | [Systems PR #2](https://github.com/VerbaEdge/verbaedge-systems/pull/2) | `111f1ca4a522b09f856be18945c15553c3c375f4` |
| Logistics custom domain | [Logistics PR #2](https://github.com/VerbaEdge/verbaedge-logistics/pull/2) | `3452919cb22f118267b1b04f56762bd29fa4ecdd` |
| Main activation | [Main PR #2](https://github.com/VerbaEdge/VerbaEdge.github.io/pull/2) | `46d624503c86ec27ec3dcddee0bea8e1a2150076` |

GitHub Pages confirmed the exact main activation commit built successfully at
`2026-11-14T06:57:20Z`, with no reported build error. The final live regression
passed at `2026-11-14T06:57:55Z`. Both subsite custom-domain builds were confirmed
built at their domain merge SHAs. A later documentation-only report merge does
not change these tested publishing files.

## Test results

| Check | Result |
| --- | --- |
| Initial source and static checks | 14 HTML pages / 46 supplied site files pass links, anchors, metadata, sitemap and public-tree checks |
| Preservation | Eleven unchanged original root files verified; new homepage pinned separately; complete original engineering page verified against the original after documented path/metadata reversal |
| JavaScript | Both syntax checks and both Node VM demo user-flow checks pass |
| RAG portfolio | Three supplied synthetic demonstrations and all 18 existing regression tests pass |
| Initial separate Pages sites | 32/32 root and asset status/hash checks pass before domain binding |
| Both custom subdomains | 32/32 HTTPS status/destination/hash checks pass after DNS propagation |
| Main content and URL aliases | 20/20 HTTPS checks match the expected source, including homepage, archive, stylesheet/images and RAG download |
| Main metadata | All seven original anchors retained on main and engineering archive; correct canonicals, one H1, archive noindex |
| Portfolio relocation | All three meta-refresh pages, fallback links and actual Systems destination hashes pass |
| Apex and www | HTTP apex, HTTPS www and HTTP www each redirect 301 to the correct HTTPS main homepage |
| Whitespace | `git diff --check` passes |

Evidence files: [initial Pages](initial-pages-validation.json),
[custom subdomains](custom-subdomains-validation.json),
[final main regression](final-main-validation.json). Historical source checks,
provenance and inspection remain alongside them. The source archives and
full-history backup bundles are kept outside the public publishing tree.

## DNS and remaining HTTPS setting

The owner configured these records; Google and Cloudflare both confirmed them:

| Type | Host | Target |
| --- | --- | --- |
| CNAME | `systems` | `verbaedge.github.io` |
| CNAME | `logistics` | `verbaedge.github.io` |

The main site's HTTPS enforcement remains enabled and its certificate is
reported approved by GitHub. Both subdomains serve the expected content over
the environment's trusted HTTPS connection, but GitHub still reports null
subsite certificate metadata and `https_enforced: false`. Their HTTP roots
currently serve 200 rather than redirecting to HTTPS.

**Remaining owner setting:** when GitHub makes the checkbox available, enable
**Enforce HTTPS** in [Systems Pages settings](https://github.com/VerbaEdge/verbaedge-systems/settings/pages)
and [Logistics Pages settings](https://github.com/VerbaEdge/verbaedge-logistics/settings/pages).
The integration's attempt to enable each with `PUT /pages` was rejected with
HTTP 403, Resource not accessible by integration. Existing deployment approval
is recorded; this is a service permission limitation, not a request for approval.
Do not disable the main site's existing HTTPS enforcement.

## Verification scope and maintenance

Live results verify HTTP status, redirect destination, metadata and exact
reviewed bytes over the inherited trusted proxy with TLS verification enabled.
Direct origin TLS inspection could not connect from this environment, so it
is not an independent origin-certificate test. No browser tool was available;
rendered mobile/desktop, keyboard, screen-reader and visual QA are unperformed.
The RAG and demo tests are synthetic local examples, not client outcomes.

Repeat relevant checks from the repository root:

```sh
python3 -B scripts/verify_website_package.py --activated-main
node scripts/test_demos.cjs
python3 -B scripts/test_rag_projects.py
python3 -B scripts/verify_live_subsites.py
python3 -B scripts/verify_live_main.py
```

For future changes, back up the latest state, use a branch and PR, preserve
CNAME/assets/routes, and verify the built commit plus live behavior. See
[ACTIVATION.md](ACTIVATION.md) for the compatibility record and rollback.
