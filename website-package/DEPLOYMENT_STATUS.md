# Deployment status after owner authorization

The owner approved merge and deployment in the working conversation. That
approval remains applicable; no repeat approval is required for this scope.
Repository creation and source access are resolved. Pages administration and
custom-domain setup remain blocked by service permissions and DNS configuration.

## Completed

- Merged main preparation [PR #1](https://github.com/VerbaEdge/VerbaEdge.github.io/pull/1)
  at `76666e0b5d586f006ea998f3b462892aa96c2306`. GitHub Pages reports a successful
  build; the live homepage returns HTTPS 200 and remains byte-for-byte identical
  to the original baseline.
- Main remains branch-based Pages from `main` / `/`, with `verbaedge.com` and
  HTTPS enforcement retained. No DNS or main domain settings were changed.
- Retained verified full-history backups before editing and after the approved
  main preparation merge.
- Verified all 32 Systems/Logistics root and asset responses at the public
  staged paths beneath `https://verbaedge.com/website-package/sites/` against
  reviewed source hashes. One temporary robots response returned 503; its retry
  returned the correct 200 body. These staged-path checks are separate from
  actual project Pages and custom-subdomain acceptance tests.
- The owner created public `VerbaEdge/verbaedge-systems` and
  `VerbaEdge/verbaedge-logistics` and granted the connected app access.
- Merged Systems source [PR #1](https://github.com/VerbaEdge/verbaedge-systems/pull/1)
  at `1044c892a66d9cf19a25c025f88fce3bf580fa20` and Logistics source
  [PR #1](https://github.com/VerbaEdge/verbaedge-logistics/pull/1) at
  `7be3d33251d1ca33b07b289ec43d904bb16c9950`.
- Each subsite repository contains its 16 original reviewed site files with
  exact matching hashes, plus a public README and source hash manifest. No
  private source material is included. Full-history bundles were backed up
  locally before and after both subsite source merges.
- Opened separate draft custom-domain [Systems PR #2](https://github.com/VerbaEdge/verbaedge-systems/pull/2)
  and [Logistics PR #2](https://github.com/VerbaEdge/verbaedge-logistics/pull/2).
  Both are unmerged; domain files are not applied to the publishing branches.
- Prepared the main activation candidate as draft
  [PR #2](https://github.com/VerbaEdge/VerbaEdge.github.io/pull/2), retaining
  original section anchors, visible engineering portfolio, assets/CNAME, and
  the complete original page. Its static activation check passes. See
  [ACTIVATION.md](ACTIVATION.md).

## Current blockers

The app can push source and merge pull requests, but cannot enable Pages.
`POST /repos/{owner}/{repo}/pages` returns HTTP 403, **Resource not accessible by
integration**, for both subsite repositories. This is a Pages administration
permission limitation, not a repository creation or source/build failure.
The owner has been asked to enable Pages in each repository's settings; no
Pages-enabled confirmation has been received yet. API `GET /pages` returns 404
for both repositories after their source merges.

The nominal initial URL `https://verbaedge.github.io/verbaedge-systems/` redirects
to `https://verbaedge.com/verbaedge-systems/` and returns HTTP 404. The Logistics
URL similarly redirects to `https://verbaedge.com/verbaedge-logistics/` and returns
404. The account-level custom domain is inherited, but the separate Pages sites
are not enabled. These are failed initial URL checks, not hosted-site passes.

At `2026-11-14T06:20:26Z`, both Google and Cloudflare DNS checks still returned
NXDOMAIN for `systems.verbaedge.com` and `logistics.verbaedge.com`. HTTPS could
not reach either site. Apex A records were unchanged, and the existing main
homepage still returned the exact baseline over HTTPS.

Neither subsite is established as hosted by a source merge. Initial temporary
Pages URL tests and both custom-subdomain tests remain pending. No browser tool
is callable in this managed environment, so rendered responsive, keyboard,
and accessibility QA have not been performed.

## Required account steps

1. Open [Systems Settings → Pages](https://github.com/VerbaEdge/verbaedge-systems/settings/pages)
   and [Logistics Settings → Pages](https://github.com/VerbaEdge/verbaedge-logistics/settings/pages).
   Under **Build and deployment**, set **Source: Deploy from a branch**, choose **main** and **/(root)**, then
   **Save**. Repository creation and app access do not need repeating.
2. After Pages builds, the agent can test each temporary URL displayed by
   GitHub, including redirects, all supplied site files, downloads and demos.
   No manual source/HTTP checks are required from the owner.
3. Then complete each custom-domain setting and the two DNS records below.
   The agent will attempt supported configuration using existing authorization;
   owner assistance is needed if Pages administration still returns HTTP 403
   or the DNS provider remains unavailable to the connection. Custom-domain
   draft PR #2 in each subsite repository is separate from the initial Pages
   source deployment; do not treat an open PR as applied domain configuration.

| Repository | Intended Pages custom domain |
| --- | --- |
| `VerbaEdge/verbaedge-systems` | `systems.verbaedge.com` |
| `VerbaEdge/verbaedge-logistics` | `logistics.verbaedge.com` |

| DNS type | Host | Target |
| --- | --- | --- |
| CNAME | `systems` | `VerbaEdge.github.io` |
| CNAME | `logistics` | `VerbaEdge.github.io` |

The intended names come from the supplied source. Neither is claimed active.
Existing nameservers are `dns1.registrar-servers.com` and
`dns2.registrar-servers.com`, consistent with Namecheap DNS hosting; use the
provider that actually controls the zone. Preserve apex, `www`, email and
unrelated records. Once domain configuration is applied, wait for DNS and valid
HTTPS before accepting the subdomains.

## Remaining verification and main activation gate

Run the live checker first against each actual temporary Pages URL, then
against both intended custom domains. It verifies status, redirect destination,
HTTPS through the configured trusted network, and exact reviewed bytes for both
roots and every supplied public file. It does not independently inspect the
origin certificate through the managed proxy or replace a real browser.

```sh
python3 -B scripts/verify_website_package.py --activated-main
python3 -B scripts/verify_live_subsites.py
```

Keep main activation PR #2 in draft and unmerged until both intended subdomain
sites pass their live tests. The owner approval persists. Further owner action
is needed only for Pages settings and, if the connection cannot perform them,
custom-domain/DNS configuration. The current main homepage stays preserved while
those deployment prerequisites are unresolved.
