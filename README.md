# HospiJunction Website

This is the public-facing website for HospiJunction. It serves two purposes:

1. **The landing page Razorpay verifies** when you submit your application.
2. **The host for your legal `.md` files** — your in-app `LegalScreen` fetches these from `https://hospijunction.com/legal/terms.md` etc., and uses bundled offline copies as a fallback.

---

## What's in this folder

```
hospijunction-website/
├── index.html               ← Landing page
├── styles.css               ← All visual styling
├── vercel.json              ← Vercel deployment config (MIME types, headers)
├── build_legal_html.py      ← Script that re-builds the /legal/*.html pages from .md
├── README.md                ← This file
└── legal/
    ├── index.html           ← Legal hub (lists all 6 docs)
    ├── terms.html           ← Rendered HTML versions (for humans visiting the site)
    ├── privacy.html
    ├── refund.html
    ├── cancellation.html
    ├── contact.html
    ├── about.html
    ├── terms.md             ← Raw markdown (your APP fetches these)
    ├── privacy.md
    ├── refund.md
    ├── cancellation.md
    ├── contact.md
    └── about.md
```

> The `.md` files are the **source of truth**. The `.html` files are auto-generated from them. If you edit policy text, edit the `.md` and re-run the build script.

---

## Step 1 — Buy the domain (~₹900/yr)

1. Go to https://www.namecheap.com
2. Search `hospijunction.com`. If available, add to cart.
3. **Turn ON WhoisGuard / Domain Privacy** (free, hides your personal details from public WHOIS lookups).
4. Skip every upsell except SSL (you don't need it — Vercel gives free SSL).
5. Complete checkout.

After purchase you'll have a Namecheap dashboard with `hospijunction.com` listed.

---

## Step 2 — Push this folder to GitHub

Since your existing app repo is private, create a **separate, public** repo for the website. Public is fine — there are no secrets in this folder.

1. Go to https://github.com/new
2. Repository name: `hospijunction-website`
3. Visibility: **Public**
4. Don't initialize with README (we have one).
5. Click **Create repository**.

Then in PowerShell or Git Bash on your machine:

```bash
cd C:\Users\asmch\Documents
# Extract the zip I gave you into a folder called hospijunction-website
cd hospijunction-website

git init
git add .
git commit -m "Initial website"
git branch -M main
git remote add origin https://github.com/Subramanyam99-creator/hospijunction-website.git
git push -u origin main
```

---

## Step 3 — Deploy to Vercel (free)

1. Go to https://vercel.com/signup and sign up with your GitHub account.
2. Once in, click **Add New → Project**.
3. Import the `hospijunction-website` repo.
4. **Framework Preset**: select **"Other"** (this is a plain static site — no framework).
5. **Build & Output Settings**: leave everything default.
   - Build Command: *(leave empty)*
   - Output Directory: *(leave empty — root)*
   - Install Command: *(leave empty)*
6. Click **Deploy**.

Vercel will give you a URL like `hospijunction-website-xyz.vercel.app`. Open it — your site should be live in ~30 seconds.

---

## Step 4 — Connect the domain

1. In your Vercel project → **Settings → Domains**.
2. Type `hospijunction.com` and click **Add**.
3. Also add `www.hospijunction.com`.
4. Vercel will show you DNS records to set up — usually:
   - For the apex (`hospijunction.com`): an **A record** pointing to `76.76.21.21`
   - For `www`: a **CNAME** record pointing to `cname.vercel-dns.com`
5. Go to Namecheap → **Domain List → Manage** next to `hospijunction.com` → **Advanced DNS** tab.
6. Delete any existing parking/default records.
7. Add the records Vercel told you about.
8. Save. DNS propagation takes 5 minutes to a few hours.
9. Once propagated, Vercel auto-issues an SSL certificate. Your site is live at `https://hospijunction.com`.

---

## Step 5 — Verify the app's legal fetch works

Once the domain is live:

1. Open `https://hospijunction.com/legal/terms.md` in a browser — you should see the raw markdown.
2. Open your HospiJunction app → Profile → Terms & Conditions → make sure the yellow "Showing offline version" banner is **NOT** showing (means the live fetch succeeded).

If the banner still shows, the URL in `src/screens/LegalScreen.js` doesn't match:
```js
const LEGAL_BASE_URL = 'https://hospijunction.com/legal';
```
Make sure that line matches your real domain exactly (no trailing slash).

---

## Step 6 — After Pvt Ltd is registered

You'll have placeholders in the legal documents (see `LEGAL_PLACEHOLDERS_CHECKLIST.md` from the previous session). When you have all the real entity details:

1. **Edit the 6 `.md` files** in `/legal/` — find-and-replace each placeholder with the real value.
2. **Re-build the HTML pages**: open a terminal in this folder and run:
   ```bash
   python3 build_legal_html.py
   ```
   (If you don't have Python installed, skip this — just commit the updated `.md` files and send them to me. I'll regenerate the HTML and send back updated files.)
3. **Commit and push**:
   ```bash
   git add .
   git commit -m "Update legal docs with registered entity details"
   git push
   ```
4. Vercel auto-deploys within 30 seconds.
5. **Also update the app**: regenerate `src/utils/legalDocs.js` (the bundled offline copy) so installed app users see the same updated text without internet. Send me the new `.md` files and I'll regenerate `legalDocs.js` for you.

---

## Step 7 — Submit to Razorpay

When applying for Razorpay live keys, they'll ask for:

- **Business website**: `https://hospijunction.com`
- **Privacy policy URL**: `https://hospijunction.com/legal/privacy.html`
- **Terms & Conditions URL**: `https://hospijunction.com/legal/terms.html`
- **Refund policy URL**: `https://hospijunction.com/legal/refund.html`
- **Contact page URL**: `https://hospijunction.com/legal/contact.html`

Important: **all placeholders must be filled in with real entity details before submission**. Razorpay's compliance team rejects pages with `[YOUR_REGISTERED_COMPANY_NAME]` etc. visible.

---

## Editing the landing page copy

If you want to tweak headlines, copy, or links on the landing page, open `index.html` in any text editor (Notepad works, VS Code is nicer). Search for the text you want to change and replace it. Save, commit, push — Vercel re-deploys automatically.

Key sections you might want to edit:
- **Hero headline**: search for `Skip the wait.`
- **Hero card sample doctor**: search for `Dr. Ramesh Kumar`
- **Pricing**: search for `One flat fee.`
- **Footer tagline**: search for `An Indian healthcare booking platform`

---

## Editing colors

Open `styles.css` and find the `:root` block at the top — all colors are defined as CSS variables there. Change `--blue-900` (the deep brand blue) and it updates everywhere.

---

## Local preview before deploying

If you want to see the site on your computer before pushing:

1. Open a terminal in this folder.
2. Run: `python3 -m http.server 8000`
3. Open `http://localhost:8000` in your browser.
4. Stop the server when done: `Ctrl+C`.

(Or just double-click `index.html` — it'll mostly work, but some links may behave differently than on a real server.)

---

## Troubleshooting

**Site shows but legal pages 404** → Check that the `legal/` folder was uploaded to GitHub (not just the files at the root).

**Legal page styling is broken** → The `<link rel="stylesheet" href="../styles.css" />` in legal pages depends on `styles.css` sitting at the project root. Don't move it.

**App still shows "offline version" banner** → Either DNS hasn't propagated yet (give it an hour), or `LEGAL_BASE_URL` in your app doesn't match the live domain.

**Fonts look wrong** → The site uses Google Fonts (Fraunces + DM Sans). If you're behind a strict firewall, fonts may not load. They will load for normal users.

---

Built for HospiJunction. Made in India 🇮🇳
