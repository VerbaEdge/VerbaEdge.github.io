# VerbaEdge Systems LLC Website

This repository is prepared for GitHub Pages hosting at:

- Default GitHub Pages URL: `https://VerbaEdge.github.io`
- Custom domain: `https://verbaedge.com`
- Repository path: `https://github.com/VerbaEdge/VerbaEdge.github.io`

## Files

- `index.html` - main one-page website
- `CNAME` - tells GitHub Pages to use `verbaedge.com`
- `.nojekyll` - keeps GitHub Pages from processing the site as a Jekyll project
- `assets/verbaedge-logo.svg` - starter logo

## GitHub Pages setup

1. Create a public repository named `VerbaEdge.github.io` under the `VerbaEdge` GitHub account.
2. Upload all files in this folder to the root of the repository.
3. Go to repository **Settings** > **Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**.
5. Select branch `main` and folder `/root`, then save.
6. Under **Custom domain**, enter `verbaedge.com` and save.
7. After DNS is set correctly and GitHub finishes checking the domain, enable **Enforce HTTPS**.

## DNS records for the domain registrar

For the apex domain `verbaedge.com`, add these A records:

```txt
A     @     185.199.108.153
A     @     185.199.109.153
A     @     185.199.110.153
A     @     185.199.111.153
```

For `www.verbaedge.com`, add this CNAME record:

```txt
CNAME www   VerbaEdge.github.io
```

Remove any conflicting parked-domain, forwarding, or default A/CNAME records for `@` or `www` before testing.

## Business email

Recommended initial addresses:

- `contracts@verbaedge.com`
- `info@verbaedge.com`
- `billing@verbaedge.com`
- `admin@verbaedge.com`
- `robert@verbaedge.com`

Do not publish the email addresses until the mailbox provider is active and DNS MX/SPF/DKIM/DMARC records are configured.
