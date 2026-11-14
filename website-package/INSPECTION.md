# Repository and supplied-source inspection

Inspected the original GitHub account **VerbaEdge** and `VerbaEdge/VerbaEdge.github.io` before editing website files. Backups were created before preparation. The subsequently supplied integrated ZIP is the source for the three staged public sites.

## Production baseline

| Item | Recorded value |
| --- | --- |
| Repository | `https://github.com/VerbaEdge/VerbaEdge.github.io` |
| Visibility and default branch | Public; `main` |
| Baseline commit | `b7ae70f7afcfd40ab120bf11b0c389dbab00dc06` |
| Baseline commit date | November 11, 2026, 10:59:46 p.m. Arizona time (`2026-11-12T05:59:46Z`) |
| Existing remote branches / tags | `main` only; no tags at inspection |
| Existing pull requests | None found before preparation |
| Pages source | Legacy branch publishing; `main`; `/` |
| Pages custom domain / HTTPS | `verbaedge.com`; HTTPS enforcement enabled |
| Main branch protection | No protection configured at inspection |
| Root `CNAME` | `verbaedge.com` followed by a newline; 14 bytes |
| Preparation branch | `codex/three-site-package` |
| Review state | Draft pull request; unmerged pending approval |

The protected root homepage, stylesheet, logos/favicons, portfolio assets, `.nojekyll`, and `CNAME` remain byte-for-byte unchanged. Their SHA-256 values are recorded in `preserved-files.json`. Root update instructions are revised to require the safe review workflow; they do not activate the staged main candidate.

No production DNS, Pages publishing source, custom domain, HTTPS setting, branch protection, or homepage activation is changed by this preparation. No Pages workflow is added. Approval is required before merging or changing live configuration even though branch protection is not configured.

## Baseline backups

The following backups were created outside the website repository before editing:

| File | Contents | SHA-256 |
| --- | --- | --- |
| `VerbaEdge.github.io-before-three-site.bundle` | Complete Git history and refs captured before the preparation branch | `7137f7c31244b7421c45cb49783284bc386c6ef1340383d03679a8b4f39201c2` |
| `VerbaEdge.github.io-main-before-three-site.zip` | Tracked website source at the baseline commit, without Git metadata | `260e4a5b83fa287d21bac3c96f9ddc53d639d6dcd656756c44c68a2c66921a43` |

Preparation copies are in `/workspace/work/backups/`. Separate copies accompany the delivered backup artifacts; neither backup belongs in the Pages publishing root. `git bundle verify` confirmed a valid bundle with complete history. The baseline includes the original homepage/CSS, CNAME, logo/favicon files, all three portfolio images, and root documentation.

Repository backups do not capture external DNS/registrar settings or all mutable Pages/account settings. Record those separately before any approved configuration change. A source restore cannot restore DNS.

To inspect a delivered backup in a separate clone:

```sh
git bundle verify /path/to/VerbaEdge.github.io-before-three-site.bundle
git clone /path/to/VerbaEdge.github.io-before-three-site.bundle /tmp/verbaedge-backup-review
```

Compare the baseline SHA in that clone; do not restore over production as an inspection step.

## Supplied source and provenance

The owner supplied `VerbaEdge_Integrated_Africa_Europe_Business_Websites.zip`, standalone Main, Systems, and TradeOps ZIPs, and a duplicate Main ZIP. The three public subtrees of the integrated ZIP match the corresponding standalone site archives byte-for-byte. Both Main archives match. Original archive SHA-256 values and entry equality are recorded in `source-provenance.json`.

Only the three public site subsets are staged. Their supplied content is retained
with the four reviewed file fixes listed in [README.md](README.md): mobile brand
wrapping in two stylesheets, a noindex sitemap entry, and French return links.

| Integrated ZIP subtree | Staged directory | Files / HTML pages |
| --- | --- | --- |
| `01_MAIN_UPLOAD_LAST__VerbaEdge.github.io/` | `sites/main/` | 14 / 4 |
| `02_SYSTEMS_UPLOAD_FIRST__verbaedge-systems/` | `sites/systems/` | 16 / 4 |
| `03_LOGISTICS_UPLOAD_SECOND__verbaedge-logistics/` | `sites/logistics/` | 16 / 6 |

The planned repositories are `VerbaEdge/verbaedge-systems` and `VerbaEdge/verbaedge-logistics`, with planned domains `systems.verbaedge.com` and `logistics.verbaedge.com`. These are source-defined destinations, not a statement that the sites are deployed or tested. The original `VerbaEdge` account remains the intended owner.

The integrated archive's old validation reports contain counts from earlier Logistics versions. They do not cover the latest six-page Logistics source. Fresh verification and the final report supersede those historical claims; no old validation pass is accepted as a current browser or deployment result.

## Content preserved and staged

The existing public business identity remains **VerbaEdge Systems LLC**, Arizona, United States, with `contracts@verbaedge.com`. Existing dark navy/charcoal, blue/teal branding and logo assets remain at the root. Systems and Trade & Logistics Technology are two service lines of the existing legal seller, not separately incorporated foreign subsidiaries.

The original engineering portfolio remains intact: image classifier deployment to edge hardware, a C++ Edge AI application with accelerated inference, and Yocto Linux image/network boot work. Preserve the qualification that these are technical work samples associated with the Upwork agency, not VerbaEdge client engagements, and retain the agency destination.

The staged Systems site adds the supplied RAG debugging/security focus, three synthetic RAG case studies and downloadable test projects while retaining broader engineering work samples. The Logistics site includes English and French marketing, billing pages, and synthetic browser-only shipment/invoice-reference demonstrations. These pages do not establish operational customs, financial, payment, or certified fiscal services.

The staged main site is a future candidate. It is not copied over the existing root homepage. Main activation requires a separate approval and pull request after both live subdomains have passed tests.

## Private-source exclusions

Private finance and operations templates, private strategy, and mixed public/private execution planning documents from the attachments are excluded from the public repository and website exports. No private finance repository is created by this task.

Do not publish internal forecasts, pipeline/risk/governance files, personnel or delegated-authority details, pricing/resource hypotheses, acquisition plans, legal/tax strategic research, or personal/financial/customer records. The public sites use only the supplied public website subsets. Do not add the complete integrated source ZIP to the publishing repository because it also contains private material.

## Verification and limits

The preparation supplies repeatable static/source checks, Node demo checks, safe extracted RAG-suite execution, and an exporter for independent `release/` and local `preview/` candidates. See [DEPLOYMENT.md](DEPLOYMENT.md) for commands, export behavior, and the rollout checklist. Record actual executed results and candidate checksums in the final report.

No callable `cua` browser tools are available in the managed profile, so browser QA is not performed here. Responsive layout, visual appearance, keyboard behavior, deployed GitHub Pages URLs, certificates, and both live subdomains remain pending checks. Static/Node success does not establish any of those results.

The root `.nojekyll` means staged files can become publicly reachable after an approved merge. The staged sites and local previews are not private access controls. Keep excluded source files and sensitive data outside the public checkout and public artifacts.

The rollout gates remain: review package; approve separate repository/Pages setup and merges; test initial Pages URLs; approve subdomain configuration/DNS; test both subdomains over HTTPS; separately approve and review main activation. Production stays at the preserved baseline until the relevant approvals and tests are complete.
