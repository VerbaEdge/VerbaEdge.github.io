# VerbaEdge website update instructions

The repository root currently publishes `verbaedge.com` from `main` through
GitHub Pages. Preserve the homepage, stylesheet, branding, portfolio, and root
`CNAME` during preparation. The three-site candidate is staged separately in
`website-package/sites/`.

These directions supersede the older instructions to upload a ZIP directly over
the publishing root:

1. Back up and inspect the current repository and Pages settings before editing.
2. Prepare changes on a new branch and pull request. Keep Systems and Trade &
   Logistics Technology as independent sites in their own planned repositories.
   Copy only the reviewed public site subset; the integrated source ZIP also
   contains private material and must not be committed to this public repository.
3. Run the checks in [website-package/VALIDATION.md](website-package/VALIDATION.md).
   Review both candidates in real browsers and test their initial Pages URLs.
4. Obtain approval before merging or changing Pages, domains, or DNS. Preserve
   the existing root `CNAME` and unrelated website/email DNS records.
5. Deploy and test **both** approved subdomains before preparing a separate main
   homepage activation pull request. Obtain approval for that merge too.

See [website-package/DEPLOYMENT.md](website-package/DEPLOYMENT.md) for the exact
site map, approval gates, acceptance checks, and rollback requirements. A merge
of the preparation package does not authorize homepage activation or live
configuration changes.
