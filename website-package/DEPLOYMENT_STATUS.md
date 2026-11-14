# Deployment status after owner authorization

The owner approved merge and deployment in the working conversation. That
approval persists. Repository creation, app access, Pages enablement, initial
Pages tests, GitHub custom-domain configuration, and DNS propagation are
complete. Both subdomains passed all 32 live HTTPS status/destination/hash
checks. The authorized main activation can now proceed after its final static
checks and backup. This record does not claim that main activation has merged.

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
- The owner updated DNS. Google and Cloudflare now resolve both subdomain
  CNAMEs to `verbaedge.github.io`; their A lookups resolve to the four GitHub
  Pages addresses. Nameservers and the original main homepage are unchanged.
- Both custom HTTPS sites passed **32/32** original root and asset checks at
  `2026-11-14T06:53:18Z`, with HTTP 200, the intended final URL, and exact
  reviewed content hashes. Evidence is retained locally in
  `final-preactivation-subdomains.json`. This includes portfolio/download,
  demo/billing, and French-page files; these are actual custom-domain checks.
- Main activation [PR #2](https://github.com/VerbaEdge/VerbaEdge.github.io/pull/2)
  is authorized to proceed now that the subdomain test requirement is met.
  Its static activation check passes; it retains original section anchors,
  visible engineering portfolio, assets/CNAME, and the complete original
  page. The merge and resulting build must be recorded after they occur.
  See [ACTIVATION.md](ACTIVATION.md).

## DNS and HTTPS state

Both public resolvers confirmed the completed records at
`2026-11-14T06:53:28Z`:

| DNS type | Host | Target |
| --- | --- | --- |
| CNAME | `systems` | `verbaedge.github.io` |
| CNAME | `logistics` | `verbaedge.github.io` |

No further DNS action is required for this activation. Existing apex, `www`,
email, verification, and unrelated records remain outside this subsite change.
The main site's HTTPS enforcement remains enabled.

The 32 custom-domain checks passed over the environment's trusted proxied
HTTPS path. GitHub Pages still reports null certificate fields and
`https_enforced: false` for both subsites. Attempts to enable enforcement with
`PUT .../pages` and `https_enforced: true` returned HTTP 403. Direct origin TLS
inspection could not connect in this environment, so an independent origin
certificate inspection has not passed and certificate approval is not claimed.

Both HTTP subdomain roots currently serve 200 rather than redirecting to HTTPS.
The remaining owner settings task is to enable **Enforce HTTPS** in each
subsite's Pages settings when the checkbox is available. This redirect option
does not block the requested main activation after the successful HTTPS
content checks. Do not disable the main site's existing HTTPS enforcement.

## Main activation and verification limits

Proceed with the already authorized main activation after final static checks
and a fresh full-history backup, then verify its exact deployed source and
Pages build. Record the actual merge SHA and deployment results afterward;
this preactivation record does not state that the merge has already occurred.

```sh
python3 -B scripts/verify_website_package.py --activated-main
python3 -B scripts/verify_live_subsites.py
```

The trusted proxied HTTPS checks establish response status, redirect
destinations, and exact reviewed bytes. They do not independently establish
origin certificate issuance. No browser tool is callable in this managed
environment, so rendered responsive, keyboard, and accessibility QA remain
unperformed. These limitations are reported separately from the successful
32/32 live subdomain checks.

The owner approval persists. Repository creation, app access, Pages setup,
GitHub custom-domain entry, and DNS changes do not need repeating. The original
main homepage is preserved at this preactivation checkpoint; the activation
merge and resulting production behavior will be recorded after deployment.
