# Fresh validation record

Checked November 13, 2026 (America/Phoenix), against production baseline
`b7ae70f7afcfd40ab120bf11b0c389dbab00dc06` and the reviewed preparation tree.
The pull request identifies the exact candidate commit. These results supersede
the supplied ZIP's historical validation reports.

| Check | Result |
| --- | --- |
| Baseline backup | Complete Git bundle verified; baseline source ZIP created before edits |
| Production preservation | All 12 protected publishing files match the baseline SHA-256 values |
| Source identity | Integrated public subtrees match the standalone ZIPs; both main ZIPs are identical |
| Public/private separation | Only three public site subsets copied; private template and management documents excluded |
| Static site checks | 14 HTML pages across 46 source files; local/cross-site links and anchors resolve; unique IDs, one H1 per page, language declarations, JSON-LD and sitemap checks pass |
| Original portfolio | Three original portfolio images match byte-for-byte; original work sample text and Upwork qualification retained in Systems |
| Independent roots | Each site has index and `.nojekyll`; subsite CNAME files absent; main candidate CNAME unchanged |
| JavaScript | Both supplied demo scripts pass Node syntax checks |
| Shipment demonstration | Four lanes; initial, partial, complete, uncheck, reset and lane-switch states pass in Node VM |
| Billing demonstration | Four selected scenarios plus missing PO, combined errors and return-to-match behavior pass in Node VM |
| RAG downloads | Identical reviewed archives; three supplied demonstrations and all 18 regression tests pass (5 retrieval, 5 citation, 8 access control) |
| Exported release | All three standalone roots pass static checks; intended live-origin links retained |
| Exported preview | All three roots and review launcher pass link checks; cross-site links and legacy redirects made local; noindex, no CNAME or sitemap |
| Current live homepage | HTTPS response 200; fetched homepage matches the baseline source; Pages settings read as `main` / `/`, `verbaedge.com`, HTTPS enabled |
| Whitespace | `git diff --check` passes |

Repeat from the repository root:

```sh
python3 -B scripts/verify_website_package.py
node --check website-package/sites/logistics/demo/demo.js
node --check website-package/sites/logistics/billing/demo/check.js
node scripts/test_demos.cjs
python3 -B scripts/test_rag_projects.py
python3 -B scripts/export_website_package.py --output /tmp/verbaedge-new-review
python3 -B scripts/verify_website_package.py --sites /tmp/verbaedge-new-review/release --variant release
python3 -B scripts/verify_website_package.py --sites /tmp/verbaedge-new-review/preview --variant preview
git diff --check
```

Use a new empty export destination. No dependencies need installing. The
exporter makes local files only and refuses to write into the repository.
`validation-results.json` contains the static check results; exported file hashes
are recorded in each export's `checksums.json`.

## Scope and pending acceptance

The RAG results apply only to synthetic, local fixtures. The Node VM checks use
a minimal DOM adapter and do not establish real browser behavior, accessibility,
or responsive layout. The source CSS wrapping fix has not been visually verified.

No browser tool is callable in this managed environment, so no browser QA was
performed. Neither planned subsite was deployed or tested at a GitHub Pages or
custom-domain URL. DNS, certificates, responsive/keyboard/screen-reader review,
live redirects and inter-site navigation remain acceptance requirements.

No GitHub Actions or Pages deployment workflow is added. Local checks passing
do not imply GitHub-hosted CI or a deployment passed. The preparation branch and
draft pull request remain unmerged; no Pages or DNS setting was changed.

Main activation remains blocked until both subdomains pass live tests and the
owner separately approves the activation pull request. See [DEPLOYMENT.md](DEPLOYMENT.md).
