# VerbaEdge website update instructions

The main company overview publishes from this repository's `main` branch and
`/(root)` through GitHub Pages at `verbaedge.com`. Systems and Trade & Logistics
Technology publish from their own separate repositories. The initial three-site
rollout is complete; see [the deployment record](website-package/DEPLOYMENT_STATUS.md).

1. Back up and inspect the latest repository and Pages settings before editing.
2. Prepare changes on a branch and pull request. Keep each site in its intended
   repository. The original integrated ZIP contains private material; never
   upload the complete archive into a public repository.
3. Preserve the original portfolio, branding, engineering archive and exact root
   CNAME. Do not delete old assets or routes without tested replacements.
4. Run `python3 -B scripts/verify_website_package.py --activated-main` and the
   relevant demo/RAG/live checks documented in the root README. Review rendered
   behavior when a real browser is available.
5. Obtain authorization before merging or changing live configuration. Preserve
   apex, www, email and unrelated DNS records. Verify the resulting Pages build,
   live content, assets, contact links and redirects after deployment.

`preserved-files.json` is the historical original baseline. Its homepage hash
intentionally differs from the approved integrated overview. Activation mode
verifies the other eleven original protected files and the complete preserved
engineering page, plus the reviewed new main overlay.

The older direct ZIP upload instructions are superseded by this branch/PR
workflow. `website-package/sites/` retains the supplied candidates; the active
main overview additionally includes the compatibility changes recorded in
`activation-provenance.json`. Use the actual reviewed root publishing files for
main deployment, rather than replacing them with the unextended source candidate.
