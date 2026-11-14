# Deployment status after owner authorization

The owner approved merge and deployment in the working conversation. No repeat
approval is required for that scope. The outstanding blockers are service
permissions and domain configuration.

## Completed

- Merged preparation [PR #1](https://github.com/VerbaEdge/VerbaEdge.github.io/pull/1)
  at `76666e0b5d586f006ea998f3b462892aa96c2306`.
- GitHub Pages reports that merge as successfully built. The live homepage
  returns HTTPS 200 and remains byte-for-byte identical to the original baseline.
- Main remains branch-based Pages from `main` / `/`, with `verbaedge.com` and
  HTTPS enforcement retained. No DNS or domain settings were changed.
- Created another verified full-history backup after the approved merge.
- Verified all 32 Systems/Logistics root and asset responses at the public
  staged paths beneath `https://verbaedge.com/website-package/sites/` against
  the reviewed source hashes. One temporary robots response returned 503;
  its retry returned the correct 200 body. These are staged paths, not the
  intended separate-site deployments or custom-subdomain acceptance tests.
- Prepared separate local deployment folders for each subsite, with public
  README and source checksums. The supplied 16 site files in each remain exact.
- Prepared the main activation candidate, preserving all original section
  anchors, visible engineering portfolio, assets/CNAME and full original page.
  The activation static check passes. See [ACTIVATION.md](ACTIVATION.md).

## Current blockers

The connected GitHub integration cannot create repositories. Both GitHub's
GraphQL createRepository operation and REST `POST /user/repos` reject the action
as **Resource not accessible by integration** (REST HTTP 403). This is a GitHub
permission failure, not a source/build failure.

Public DNS queries through two resolvers return NXDOMAIN for both planned
subdomains. No DNS-management connection is available here. The existing
nameservers are `dns1.registrar-servers.com` and `dns2.registrar-servers.com`,
consistent with Namecheap DNS hosting; use the provider that actually controls
the zone.

The live checker correctly fails both intended subdomains before setup. No
browser tool is callable in this managed environment, so rendered browser and
accessibility QA have not been performed. The owner does not need to perform
the source/HTTP checks manually; the agent can run those after access is ready.

## Required account steps

1. As **VerbaEdge**, create public repositories `verbaedge-systems` and
   `verbaedge-logistics`, each initialized with a README on `main`.
2. Grant the connected GitHub app access to both new repositories. The agent
   can then push source branches, open and merge the authorized PRs, and attempt
   Pages setup. If GitHub also denies Pages administration, enable Pages from
   `main` / `/` in each repository's settings when the reviewed files are merged.
3. After the sites are configured, add these records at the DNS provider:

| Type | Host | Target |
| --- | --- | --- |
| CNAME | `systems` | `VerbaEdge.github.io` |
| CNAME | `logistics` | `VerbaEdge.github.io` |

Preserve apex, `www`, email and unrelated records. Do not send credentials or
API keys in chat. Once the connection and records are ready, the agent can
finish configuration, wait for valid HTTPS, verify both actual sites and then
merge the authorized main activation.

## Remaining verification

Run the live checker first against each actual temporary Pages URL and then
against both intended custom domains. It verifies status, redirect destination,
HTTPS through the configured trusted network and exact reviewed bytes for both
roots and every supplied public file. It does not inspect an independent origin
certificate through the managed proxy or replace a real browser.

```sh
python3 -B scripts/verify_website_package.py --activated-main
python3 -B scripts/verify_live_subsites.py
```

Keep the main activation draft unmerged while the two intended sites are
unavailable. Existing approval is recorded; further owner action is needed only
for the service access and DNS setup described above.
