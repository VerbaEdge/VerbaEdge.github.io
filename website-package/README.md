# VerbaEdge integrated website source and records

The approved three-site rollout is published. The supplied public source
subsets remain here for provenance. Private strategy, finance and mixed
management attachments are excluded from the public repository and exports.

| Site | Supplied source | Repository | Published URL |
| --- | --- | --- | --- |
| Main overview | `sites/main/` | `VerbaEdge/VerbaEdge.github.io` | https://verbaedge.com/ |
| Systems | `sites/systems/` | `VerbaEdge/verbaedge-systems` | https://systems.verbaedge.com/ |
| Trade & Logistics Technology | `sites/logistics/` | `VerbaEdge/verbaedge-logistics` | https://logistics.verbaedge.com/ |

The active main site adds compatibility sections and the complete original
engineering page at `/engineering/`; those additions are pinned in
`activation-provenance.json`. The original assets, stylesheet, CNAME and
portfolio remain preserved. Each subsite has its own domain CNAME in its own
repository. The original supplied subsite source subsets here remain unchanged
from the reviewed content, without deployment CNAMEs.

[DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md) is the final rollout record and
includes remaining HTTPS setting limitations. [ACTIVATION.md](ACTIVATION.md)
records preservation and rollback. [INSPECTION.md](INSPECTION.md),
[VALIDATION.md](VALIDATION.md) and [DEPLOYMENT.md](DEPLOYMENT.md) retain the
historical audit, preparation checks and rollout plan. Their statements about
unmerged drafts or unchanged homepage describe the preactivation checkpoint.

Fresh live evidence is in `initial-pages-validation.json`,
`custom-subdomains-validation.json` and `final-main-validation.json`.
The public source provenance and original SHA-256 baseline are retained in
`source-provenance.json` and `preserved-files.json`.

Four source fixes were reviewed before deployment: narrow-screen brand wrapping
in two stylesheets, the noindex demo sitemap entry, and French billing return
links. The full original engineering portfolio and supplied synthetic RAG
demonstrations were retained.

The offline exporter still exports the three supplied source candidates, with
local preview links or intended release origins. It does not export the extended
production main overlay; use the root publishing files and activation manifest
for that site. Exporting never publishes or changes DNS.
