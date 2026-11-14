# Deployment status after owner authorization

The owner approved merge and deployment in the working conversation. That
approval persists. Repository creation, app access, Pages enablement, initial
Pages tests, and GitHub custom-domain configuration are complete. DNS access
is the remaining external blocker; certificates and custom-domain HTTPS tests
must follow before main activation.

## Completed

- Merged main preparation [PR #1](https://github.com/VerbaEdge/VerbaEdge.github.io/pull/1)
  at `76666e0b5d586f006ea998f3b462892aa96c2306`. Its Pages build succeeded.
  The live main homepage remains byte-for-byte identical to the baseline,
  with `verbaedge.com`, `main` / `/`, and existing HTTPS enforcement retained.
- Retained verified full-history backups before preparation and after the
  main preparation merge. Pre/post source and domain merge bundles are also
  backed up and verified locally for both subsite repositories.
- Verified 32 original Systems/Logistics root and asset responses at staged
  paths beneath `https://verbaedge.com/website-package/sites/`. These staging
  checks are separate from the actual Pages deployment checks below.
- The owner created both public subsite repositories and granted app access.
  Source [Systems PR #1](https://github.com/VerbaEdge/verbaedge-systems/pull/1)
  merged at `1044c892a66d9cf19a25c025f88fce3bf580fa20`; source
  [Logistics PR #1](https://github.com/VerbaEdge/verbaedge-logistics/pull/1)
  merged at `7be3d33251d1ca33b07b289ec43d904bb16c9950`.
- Each original set of 16 supplied site files matches reviewed hashes exactly,
  accompanied by a public README and source manifest. Private source material
  is excluded.
- The owner enabled Pages in both repositories. API reads confirmed `main` /
  `/` sources and initial builds at the expected source merge commits. The
  earlier Pages API permission failure was resolved by this owner action;
  no further Pages-enablement action is needed.
- Both actual initial Pages URLs passed all **32/32** original root and asset
  response/hash checks: `https://verbaedge.com/verbaedge-systems/` and
  `https://verbaedge.com/verbaedge-logistics/`. Evidence is retained locally in
  `initial-pages-live-verified.json`. These are initial Pages checks, not
  custom-subdomain HTTPS acceptance tests.
- After those tests, merged authorized custom-domain
  [Systems PR #2](https://github.com/VerbaEdge/verbaedge-systems/pull/2) at
  `111f1ca4a522b09f856be18945c15553c3c375f4` and
  [Logistics PR #2](https://github.com/VerbaEdge/verbaedge-logistics/pull/2) at
  `3452919cb22f118267b1b04f56762bd29fa4ecdd`.
- GitHub Pages now confirms `systems.verbaedge.com` and
  `logistics.verbaedge.com` from the merged CNAME files. No additional owner
  custom-domain setting is needed. Both domain builds are confirmed built at
  their matching merge SHAs: Systems updated `2026-11-14T06:40:31Z`, Logistics
  updated `2026-11-14T06:40:43Z`.
- Main activation [PR #2](https://github.com/VerbaEdge/VerbaEdge.github.io/pull/2)
  remains a draft. Its static activation check passes; it retains original
  section anchors, visible engineering portfolio, assets/CNAME, and a complete
  preserved original page. See [ACTIVATION.md](ACTIVATION.md).

## Current blocker: DNS

The latest recorded check at `2026-11-14T06:39:30Z` returned NXDOMAIN for both
`systems.verbaedge.com` and `logistics.verbaedge.com` through Google and
Cloudflare. Neither custom-domain HTTPS connection reached an origin. Apex A
records and the original main homepage remained unchanged.

GitHub's current certificate fields are null and `https_enforced` is false
for both subsites while DNS is pending. No certificate approval or working
custom-domain HTTPS is claimed. A successful source or CNAME merge does not
establish DNS propagation or certificate readiness.

## Required DNS action

The owner has been asked to add the following records at the provider that
controls `verbaedge.com`:

| DNS type | Host | Target |
| --- | --- | --- |
| CNAME | `systems` | `VerbaEdge.github.io` |
| CNAME | `logistics` | `VerbaEdge.github.io` |

Use a hostname target without a scheme or repository path. Preserve all
existing apex, `www`, email, verification, and unrelated records. Nameservers
are `dns1.registrar-servers.com` and `dns2.registrar-servers.com`, consistent
with Namecheap DNS hosting. Repository creation, app grants, Pages enablement,
and GitHub custom-domain entry do not need repeating.

## Remaining verification and main activation gate

After DNS is applied, verify both CNAMEs, wait for certificate issuance, and
enable/verify HTTPS when GitHub permits it.
Run the live checker against both intended custom domains. It checks status,
redirect destinations, trusted proxied HTTPS, and exact reviewed bytes for both
roots and all supplied public files. It cannot independently inspect origin
certificates through the managed proxy.

```sh
python3 -B scripts/verify_website_package.py --activated-main
python3 -B scripts/verify_live_subsites.py
```

No browser tool is callable in this managed environment; rendered responsive,
keyboard, and accessibility QA remain unperformed. Initial Pages HTTP/hash
checks do not replace browser QA or the pending custom-subdomain tests.

Keep main activation PR #2 in draft and unmerged until **both** custom-domain
HTTPS tests pass. The owner approval persists; no repeat approval is needed
for the authorized deployment. The original main homepage stays preserved
while DNS, certificates, and the live acceptance tests remain unresolved.
