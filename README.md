# VerbaEdge Systems LLC

Official website for VerbaEdge Systems LLC.

Website: https://verbaedge.com

Contact: [contracts@verbaedge.com](mailto:contracts@verbaedge.com)

This repository hosts the public VerbaEdge website through GitHub Pages.

## Integrated website activation candidate

This branch prepares the main overview while retaining the complete original
engineering website at `engineering/`, the original portfolio assets, and the
exact root `CNAME`. Systems and Trade & Logistics Technology remain independent
sites with their own repositories and intended subdomains. Private management
and finance sources are excluded.

The owner approved merge and deployment. The preparation PR is merged; this
activation must wait for the separate sites and their domains to work. See
[deployment status and required account steps](website-package/DEPLOYMENT_STATUS.md),
[activation details](website-package/ACTIVATION.md), and the
[deployment plan](website-package/DEPLOYMENT.md).

Run `python3 -B scripts/verify_website_package.py --activated-main` for this
candidate. Run `python3 -B scripts/verify_live_subsites.py` to check both deployed
subdomains and their supplied files before activation. Historical preparation
checks are recorded in [VALIDATION.md](website-package/VALIDATION.md).
