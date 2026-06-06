#!/usr/bin/env python3
"""
Build script: converts each /legal/*.md file into a styled /legal/*.html page
using the editorial-medical aesthetic defined in styles.css.

Run from inside the site/ folder:  python build_legal_html.py
"""

import re
import html
import os
from pathlib import Path

# Order matches the in-app tab order
PAGES = [
    ("terms",            "terms.md",                  "Terms & Conditions"),
    ("privacy",          "privacy.md",                "Privacy Policy"),
    ("refund",           "refund-cancellation.md",    "Refund & Cancellation"),
    ("account-deletion", "account-deletion.md",       "Delete Account"),
    ("contact",          "contact.md",                "Contact Us"),
    ("about",            "about.md",                  "About"),
]

SITE_DIR  = Path(__file__).parent
LEGAL_DIR = SITE_DIR / "legal"


# ----------------------------------------------------------------------
# Tiny markdown -> HTML converter (handles the subset we actually use)
# ----------------------------------------------------------------------

def render_inline(text: str) -> str:
    """Inline-level: escape HTML, then re-apply our markdown spans."""
    text = html.escape(text, quote=False)
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text


def md_to_html(md: str) -> str:
    """Block-level markdown -> HTML. Supports h1-h3, p, ul/ol, hr, blockquote."""
    lines = md.split('\n')
    out = []
    i = 0
    n = len(lines)

    def flush_paragraph(buf):
        if buf:
            text = ' '.join(buf).strip()
            if text:
                out.append(f"<p>{render_inline(text)}</p>")
            buf.clear()

    para_buf = []

    while i < n:
        raw  = lines[i]
        line = raw.strip()

        if not line:
            flush_paragraph(para_buf)
            i += 1
            continue

        if line == '---':
            flush_paragraph(para_buf)
            out.append('<hr />')
            i += 1
            continue

        if line.startswith('### '):
            flush_paragraph(para_buf)
            out.append(f"<h3>{render_inline(line[4:])}</h3>")
            i += 1
            continue
        if line.startswith('## '):
            flush_paragraph(para_buf)
            out.append(f"<h2>{render_inline(line[3:])}</h2>")
            i += 1
            continue
        if line.startswith('# '):
            flush_paragraph(para_buf)
            out.append(f"<h1>{render_inline(line[2:])}</h1>")
            i += 1
            continue

        if line.startswith('> '):
            flush_paragraph(para_buf)
            quote_lines = []
            while i < n and lines[i].strip().startswith('> '):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            out.append(f"<blockquote>{render_inline(' '.join(quote_lines))}</blockquote>")
            continue

        if line.startswith('- ') or line.startswith('* '):
            flush_paragraph(para_buf)
            items = []
            while i < n and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ')):
                items.append(lines[i].strip()[2:])
                i += 1
            li_html = ''.join(f"<li>{render_inline(item)}</li>" for item in items)
            out.append(f"<ul>{li_html}</ul>")
            continue

        if re.match(r'^\d+\.\s', line):
            flush_paragraph(para_buf)
            items = []
            while i < n and re.match(r'^\d+\.\s', lines[i].strip()):
                items.append(re.sub(r'^\d+\.\s', '', lines[i].strip()))
                i += 1
            li_html = ''.join(f"<li>{render_inline(item)}</li>" for item in items)
            out.append(f"<ol>{li_html}</ol>")
            continue

        if line.startswith('|'):
            i += 1
            continue

        para_buf.append(line)
        i += 1

    flush_paragraph(para_buf)
    return '\n'.join(out)


# ----------------------------------------------------------------------
# HTML page template (single source of truth - every legal page uses this)
# Uses HTML entities instead of raw Unicode to survive any source encoding.
# ----------------------------------------------------------------------

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} &mdash; HospiJunction</title>
  <meta name="description" content="{title} &mdash; HospiJunction, an Indian doctor appointment booking platform." />
  <meta name="theme-color" content="#0F2E5C" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700;9..144,800&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../styles.css" />
</head>
<body class="legal-page">

  <div class="brand-line"></div>

  <header class="nav">
    <div class="container nav-inner">
      <a href="/" class="logo">
        <span class="logo-mark">HJ</span>
        <span class="logo-text">HospiJunction</span>
      </a>
      <nav class="nav-links">
        <a href="/#how">How it works</a>
        <a href="/#pricing">Pricing</a>
        <a href="/legal/">Legal</a>
      </nav>
    </div>
  </header>

  <div class="legal-page-header">
    <div class="container">
      <div class="legal-breadcrumb">
        <a href="/">Home</a> &middot; <a href="/legal/">Legal</a> &middot; {title}
      </div>
      <div class="legal-tabs">
        {tabs}
      </div>
    </div>
  </div>

  <article class="legal-article">
    {content}
  </article>

  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <div class="logo">
          <span class="logo-mark">HJ</span>
          <span class="logo-text">HospiJunction</span>
        </div>
        <p class="footer-tag">An Indian healthcare booking platform. We are a technology facilitator &mdash; not a healthcare provider. In a medical emergency, call <strong>108</strong>.</p>
      </div>
      <div class="footer-col">
        <h4>Product</h4>
        <a href="/#how">How it works</a>
        <a href="/#pricing">Pricing</a>
        <a href="/#why">Why us</a>
      </div>
      <div class="footer-col">
        <h4>Legal</h4>
        <a href="/legal/terms.html">Terms</a>
        <a href="/legal/privacy.html">Privacy</a>
        <a href="/legal/refund.html">Refund &amp; Cancellation</a>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="/legal/about.html">About</a>
        <a href="/legal/contact.html">Contact</a>
      </div>
    </div>
    <div class="container footer-bottom">
      <span>&copy; <span id="year">2026</span> HospiJunction. All rights reserved.</span>
      <span>Made in India</span>
    </div>
  </footer>

  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def build_tabs(active_key: str) -> str:
    return ''.join(
        f'<a href="{k}.html" class="{"is-active" if k == active_key else ""}">{label}</a>'
        for k, _md, label in PAGES
    )


def build_page(key: str, md_filename: str, title: str):
    md_text = (LEGAL_DIR / md_filename).read_text(encoding='utf-8')
    content_html = md_to_html(md_text)
    page = PAGE_TEMPLATE.format(
        title=title,
        tabs=build_tabs(key),
        content=content_html,
    )
    (LEGAL_DIR / f"{key}.html").write_text(page, encoding='utf-8')
    print(f"  built  legal/{key}.html  ({len(page):,} bytes)")


# ----------------------------------------------------------------------
# Legal hub page (legal/index.html)
# ----------------------------------------------------------------------

HUB_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Legal &amp; Policies &mdash; HospiJunction</title>
  <meta name="description" content="HospiJunction legal documents: Terms, Privacy, Refund, Cancellation, Contact, About." />
  <meta name="theme-color" content="#0F2E5C" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700;9..144,800&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../styles.css" />
</head>
<body class="legal-page">

  <div class="brand-line"></div>

  <header class="nav">
    <div class="container nav-inner">
      <a href="/" class="logo">
        <span class="logo-mark">HJ</span>
        <span class="logo-text">HospiJunction</span>
      </a>
      <nav class="nav-links">
        <a href="/#how">How it works</a>
        <a href="/#pricing">Pricing</a>
        <a href="/legal/">Legal</a>
      </nav>
    </div>
  </header>

  <div class="legal-page-header">
    <div class="container">
      <div class="legal-breadcrumb"><a href="/">Home</a> &middot; Legal</div>
    </div>
  </div>

  <article class="legal-article">
    <h1>Legal &amp; Policies</h1>
    <p>Everything covering your rights, our obligations, and how HospiJunction works behind the scenes. Updated whenever something material changes.</p>

    <div class="legal-hub-grid">
      <a href="terms.html" class="legal-card">
        <h3>Terms &amp; Conditions</h3>
        <p>The rules of using HospiJunction.</p>
        <span class="legal-card-arrow">&rarr;</span>
      </a>
      <a href="privacy.html" class="legal-card">
        <h3>Privacy Policy</h3>
        <p>What we collect, why, and how it's protected.</p>
        <span class="legal-card-arrow">&rarr;</span>
      </a>
      <a href="refund.html" class="legal-card">
        <h3>Refund &amp; Cancellation</h3>
        <p>Reschedule freely. Refunds when the hospital cancels.</p>
        <span class="legal-card-arrow">&rarr;</span>
      </a>
      <a href="account-deletion.html" class="legal-card">
        <h3>Delete Account</h3>
        <p>How to request account deletion and what data is removed.</p>
        <span class="legal-card-arrow">&rarr;</span>
      </a>
      <a href="contact.html" class="legal-card">
        <h3>Contact Us</h3>
        <p>Support, privacy, and grievance channels.</p>
        <span class="legal-card-arrow">&rarr;</span>
      </a>
      <a href="about.html" class="legal-card">
        <h3>About</h3>
        <p>Who we are and what we believe.</p>
        <span class="legal-card-arrow">&rarr;</span>
      </a>
    </div>
  </article>

  <footer class="footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <div class="logo">
          <span class="logo-mark">HJ</span>
          <span class="logo-text">HospiJunction</span>
        </div>
        <p class="footer-tag">An Indian healthcare booking platform. We are a technology facilitator &mdash; not a healthcare provider. In a medical emergency, call <strong>108</strong>.</p>
      </div>
      <div class="footer-col">
        <h4>Product</h4>
        <a href="/#how">How it works</a>
        <a href="/#pricing">Pricing</a>
        <a href="/#why">Why us</a>
      </div>
      <div class="footer-col">
        <h4>Legal</h4>
        <a href="terms.html">Terms</a>
        <a href="privacy.html">Privacy</a>
        <a href="refund.html">Refund &amp; Cancellation</a>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
      </div>
    </div>
    <div class="container footer-bottom">
      <span>&copy; <span id="year">2026</span> HospiJunction. All rights reserved.</span>
      <span>Made in India</span>
    </div>
  </footer>

  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>
</body>
</html>
"""


def main():
    print("Building HospiJunction legal pages...")
    print(f"  source dir: {LEGAL_DIR}")
    for key, md_filename, title in PAGES:
        build_page(key, md_filename, title)
    (LEGAL_DIR / "index.html").write_text(HUB_TEMPLATE, encoding='utf-8')
    print(f"  built  legal/index.html (hub)")
    print("Done.")


if __name__ == "__main__":
    main()
