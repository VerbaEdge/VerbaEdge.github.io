# VerbaEdge three-site review package

Prepared from the supplied integrated archive. The current root website remains
unchanged. This directory contains public website candidates only; private
strategy, finance, and execution planning attachments remain outside the public
repository.

| Candidate | Intended repository | Intended domain | Status |
| --- | --- | --- | --- |
| `sites/main/` | `VerbaEdge/VerbaEdge.github.io` | `verbaedge.com` | Staged replacement; activate last after separate approval |
| `sites/systems/` | `VerbaEdge/verbaedge-systems` | `systems.verbaedge.com` | Separate planned site; not deployed |
| `sites/logistics/` | `VerbaEdge/verbaedge-logistics` | `logistics.verbaedge.com` | Separate planned site; not deployed |

All three are independent buildless static sites. The subsite candidates have no
`CNAME`. The main candidate retains the existing `CNAME` bytes.

The [inspection record](INSPECTION.md) documents the backup and sources.
[Validation](VALIDATION.md) records fresh checks and limitations.
[Deployment](DEPLOYMENT.md) describes the staged rollout and approvals.
`source-provenance.json` records original public source hashes, and
`preserved-files.json` pins the original publishing files.

The supplied public content is retained with four reviewed file changes:

- `main/site.css` and `logistics/site.css`: allow long division labels to wrap on
  narrow screens while keeping the logo size.
- `logistics/sitemap.xml`: remove the shipment demo because its page is `noindex`.
- `logistics/fr/facturation/index.html`: return French readers to the French
  Logistics page; retain the explicit English billing link.

Run `python3 scripts/export_website_package.py --output /tmp/verbaedge-review`
from the repository root with a new, empty destination. `preview/` provides local
cross-site navigation and disables indexing; `release/` retains intended live
origins. Neither is published by this command. Browser QA and both deployed
subdomain tests are still required before main activation.

Do not upload this package directory, the entire integrated ZIP, or all three
sites into the production publishing root. Do not merge or change live
configuration without approval.
