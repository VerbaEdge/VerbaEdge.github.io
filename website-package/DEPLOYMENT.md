# VerbaEdge three-site deployment plan

The supplied integrated website ZIP is staged for review under `website-package/sites/`. The existing production homepage, branding, portfolio, and root `CNAME` remain unchanged. This package prepares three independent sites; it does not deploy them.

Use only the original GitHub account **VerbaEdge**. The branch is `codex/three-site-package`; the draft pull request remains unmerged pending owner approval. No new repository, Pages workflow, custom-domain configuration, DNS change, or homepage activation is part of this preparation.

These instructions and the updated root `README_UPDATE_INSTRUCTIONS.md` supersede older direct-upload directions. Use review branches and pull requests. Obtain approval before merging or changing live configuration.

## Site map

| Site | Staged source | Repository | Intended domain |
| --- | --- | --- | --- |
| Main company site | `website-package/sites/main/` | Existing `VerbaEdge/VerbaEdge.github.io` | Existing `verbaedge.com` |
| Systems | `website-package/sites/systems/` | Planned `VerbaEdge/verbaedge-systems` | Planned `systems.verbaedge.com` |
| Trade & Logistics Technology | `website-package/sites/logistics/` | Planned `VerbaEdge/verbaedge-logistics` | Planned `logistics.verbaedge.com` |

Systems and Logistics are separate planned GitHub Pages sites. Their domain names come from the supplied source; this preparation does not establish that either domain is active or tested. Keep the main candidate staged until both subdomains have passed their live tests and main activation has been separately approved.

The Logistics site includes `/`, `/demo/`, `/billing/`, `/billing/demo/`, `/fr/`, and `/fr/facturation/`. Both demos use synthetic examples in the browser. The pages do not establish a live shipment platform, payment service, customs filing service, or certified tax/e-invoicing system. Systems retains the supplied RAG demonstrations/download and the original engineering portfolio. Preserve source qualifications about synthetic work samples and service boundaries.

## Validate and export the candidates

Run from the repository root:

```sh
python3 scripts/verify_website_package.py
node scripts/test_demos.cjs
python3 scripts/test_rag_projects.py
python3 scripts/export_website_package.py --output /tmp/verbaedge-three-site-candidate
```

The export destination must be an empty directory. Keep generated output outside the repository publishing root. The exporter produces two candidate builds and checksum JSON without remote or live side effects:

- `release/` retains the supplied site-origin links and metadata for deployment review.
- `preview/` makes cross-site links and metadata local for review; main legacy redirects resolve locally in that preview.

Neither export changes the production homepage or verifies live domains. The three folders inside an export are independent site roots. Transfer only the intended site's contents to its intended repository. Never copy all three folders, a review launcher, or the integrated ZIP into the main publishing root.

`verify_website_package.py` checks the protected baseline files, local and cross-site references, assets, structured data, sitemap references, and exclusion of private sources. The Node checks exercise both synthetic demos. The RAG test runner extracts and tests the supplied portfolio projects in a separate work area. Source provenance and archive equality are recorded in `source-provenance.json`.

Record the exact commands, source commit, output checksums, and results. Supplied historical validation JSON is not current evidence: it predates the latest Logistics additions. Use fresh checks for the prepared candidate. No browser QA has been performed here because the managed profile has no callable `cua` browser tools. Responsive/visual/keyboard review and deployed Pages/subdomain tests remain required.

## Phase 1: approve and test separate Pages sites

Review the package and the backup record in [INSPECTION.md](INSPECTION.md). Obtain owner approval before creating the planned repositories or configuring Pages. Confirm the public content, repository names, and planned domains.

After approval, create the two separate repositories under `VerbaEdge`. Use a branch and pull request in each repository to prepare its reviewed site contents. Merging requires approval. Configure each approved Pages source as supported by GitHub; do not alter the existing main site's source. Leave subsite custom domains unset for initial Pages testing. The staged subsite sources have no `CNAME` files.

First test the temporary URLs actually displayed by GitHub Pages. With the planned repository names, the nominal URLs are:

- `https://verbaedge.github.io/verbaedge-systems/`
- `https://verbaedge.github.io/verbaedge-logistics/`

An account-level custom domain can affect project-site redirects. Record the actual redirect chains and final URLs. Verify that the independent sites work beneath their project paths, including all styles, logos, portfolio pages, downloads, demos, French pages, internal navigation, and contact links. Review cross-site destinations against the intended deployment stage before treating them as launch-ready.

## Phase 2: approve and test both custom subdomains

Only after both independent Pages sites pass their initial tests, obtain approval for the exact custom-domain and DNS changes. Record the current settings first. Preserve apex, `www`, email, verification, and unrelated DNS records.

| DNS record type | Host | Target |
| --- | --- | --- |
| CNAME | `systems` | `VerbaEdge.github.io` |
| CNAME | `logistics` | `VerbaEdge.github.io` |

A DNS CNAME target is a hostname, not a repository path or `https://` URL. Set `systems.verbaedge.com` in the Systems repository's approved Pages configuration and `logistics.verbaedge.com` in the Logistics repository's configuration. Add only that site's matching `CNAME` through its reviewed change. Never reuse the main site's `verbaedge.com` CNAME in a subsite.

Wait for DNS resolution, GitHub domain verification, and certificate provisioning. Enable and verify HTTPS once certificates are available. Test **both** subdomains over HTTPS. A commit, successful static check, or saved DNS record does not establish propagation or a working deployment. Failed or incomplete tests keep main-site activation blocked.

## Phase 3: approve main activation separately

After both subdomains pass, refresh the main repository backup and compare it with the inspected baseline. Obtain approval for the specific main homepage change. Prepare a separate, focused activation pull request in `VerbaEdge/VerbaEdge.github.io`.

Review existing branding, portfolio wording and images, contact details, old inbound links, candidate redirects, metadata, favicon, and both division links. Preserve the root `CNAME` byte-for-byte. Do not remove old assets or routes without first inspecting inbound links and testing any replacement redirects. Merge only after owner approval, then rerun the production regression checks.

No approval to merge this preparation pull request authorizes subdomain configuration, DNS edits, or main activation. Those remain separate explicit approval gates.

## Evidence checklist

Record dates, exact URLs, tested commit SHAs, checksums, redirects, and pass/fail results. Keep credentials and private customer information out of reports and public artifacts.

| Check | Required evidence |
| --- | --- |
| Source and preservation | Supplied ZIP checksums/equality; valid baseline bundle/ZIP; protected root files unchanged |
| Candidate builds | Static verifier, demo and RAG results; release/preview checksums; source SHA |
| Browser review | Desktop/mobile layouts, readable portfolio/images, no overflow, keyboard/focus, image alternatives, headings, contrast, reduced motion |
| Initial Pages | Actual URLs and redirects; independent site assets, pages, downloads, demos, contact links |
| Both subdomains | DNS, valid HTTPS/certificates, pages/assets, redirects, inter-site links, mobile/keyboard checks |
| Main regression | Apex and www behavior, original identity/contact/portfolio, redirects, both division destinations |
| Approval record | Repository/Pages setup, each merge, domains/DNS, and separate main activation |

Baseline/static/Node checks must be reported separately from browser and live deployment tests. Neither planned subdomain has been deployed or live-tested by this preparation.

## Rollback

No live configuration changed during preparation, so no production rollback is needed now. Keep the full Git bundle and baseline source ZIP outside the publishing repository and deliver separate copies.

For a later approved deployment failure, stop rollout and retain the failing URL/commit evidence. Revert the relevant source change through an approved pull request or restore the approved known-good source from backup. The inspected main baseline is `b7ae70f7afcfd40ab120bf11b0c389dbab00dc06`.

Reverting source does not restore DNS or Pages settings. Configuration rollback requires the recorded pre-change settings and owner approval. Preserve the original site and apex domain while resolving a planned subsite failure.
