# VerbaEdge Systems LLC

Official company website: https://verbaedge.com/

Contact: [contracts@verbaedge.com](mailto:contracts@verbaedge.com)

## Published websites

| Website | Repository |
| --- | --- |
| [VerbaEdge overview](https://verbaedge.com/) | `VerbaEdge/VerbaEdge.github.io` |
| [VerbaEdge Systems](https://systems.verbaedge.com/) | `VerbaEdge/verbaedge-systems` |
| [Trade & Logistics Technology](https://logistics.verbaedge.com/) | `VerbaEdge/verbaedge-logistics` |

The complete original engineering website is retained at
[verbaedge.com/engineering/](https://verbaedge.com/engineering/). The original
portfolio assets, stylesheet, branding and main CNAME remain preserved.
The main overview retains the original section anchors and visible portfolio.

The owner approved deployment. All three repositories use separate GitHub Pages
sites; main activation followed successful checks on both custom subdomains.
Private strategy and finance sources are excluded.

See [the final deployment record](website-package/DEPLOYMENT_STATUS.md),
[activation and rollback details](website-package/ACTIVATION.md), and the
[historical source inspection](website-package/INSPECTION.md).

## Repeatable checks

```sh
python3 -B scripts/verify_website_package.py --activated-main
node scripts/test_demos.cjs
python3 -B scripts/test_rag_projects.py
python3 -B scripts/verify_live_subsites.py
python3 -B scripts/verify_live_main.py
```

Use branches and pull requests for future changes. Obtain authorization before
changing live configuration. Preserve root CNAME and email/domain records.
