# VerbaEdge GitHub Pages Launch Guide

## Decision

Use `verbaedge.com` as the public business domain and use `https://github.com/VerbaEdge` as the GitHub identity. The website repository should be named `VerbaEdge.github.io` so GitHub Pages serves it as the main site for the account.

## DNS target values

A records for `verbaedge.com`:

- `185.199.108.153`
- `185.199.109.153`
- `185.199.110.153`
- `185.199.111.153`

CNAME record for `www.verbaedge.com`:

- `www` -> `VerbaEdge.github.io`

## Publishing order

1. Buy or confirm control of `verbaedge.com`.
2. Log in to `https://github.com/VerbaEdge`.
3. Create the repository `VerbaEdge.github.io`.
4. Upload the files from this ZIP into the repository root.
5. Enable GitHub Pages from the `main` branch, `/root` folder.
6. Add `verbaedge.com` in the GitHub Pages custom domain box.
7. Add DNS records at your domain registrar.
8. Wait for DNS propagation.
9. Enable Enforce HTTPS.
10. Test `https://verbaedge.com` and `https://www.verbaedge.com`.
11. Set up business email after the domain is purchased and DNS is accessible.
