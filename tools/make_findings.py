#!/usr/bin/env python3
"""Build horror-finding.html: the research / findings section as a standalone site.

Source of truth = the built index.html. We lift (a) the shared <style> block and
(b) the whole #research <section> verbatim, then wrap them in a small standalone
document with its own header, footer and nav. No content is rewritten here, so
the findings site always matches the live stories site.

Usage: python3 tools/make_findings.py
Out:   horror-finding.html
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "horror-finding.html"
STORIES_URL = "https://raat-ke-us-paar-sunnythakur151994-sudos-projects.vercel.app/"

h = SRC.read_text(encoding="utf-8")

# ---- 1. shared stylesheet -------------------------------------------------
m = re.search(r"<style[\s\S]*?</style>", h)
assert m, "style block not found"
style = m.group(0)

# ---- 2. the #research section, verbatim ----------------------------------
start = h.index('<section class="section section-alt" id="research"')
stop = h.index("<!-- GAURAV TIWARI -->", start)
stop = h.rindex("</section>", start, stop) + len("</section>")
research = h[start:stop].strip()
assert 'id="rs-refs"' in research and 'id="worldwide"' in research

page = f"""<!DOCTYPE html>
<html lang="hi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Horror Findings — Raat Ke Us Paar · Research Archive</title>
<meta name="description" content="Raat Ke Us Paar ka research archive: duniya bhar mein dohrne wali ghatnayein, sleep paralysis, DMT aur entity reports, 2026 ke naye studies, NDPS law, aur Gaurav Tiwari ke case ki jaanch. Har chapter ke saath sources.">
<meta name="robots" content="index, follow">
<meta property="og:title" content="Horror Findings — Raat Ke Us Paar">
<meta property="og:description" content="15 research chapters: worldwide repeating incidents, entities, DMT, law, aur evidence ka honest summary.">
<style>{style[len('<style>'):]}</style>
</head>
<body>
<div class="grain" aria-hidden="true"></div>
<div class="vignette" aria-hidden="true"></div>

<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="#top" aria-label="Horror Findings — home">
      <span class="brand-mark" aria-hidden="true">HF</span>
      <span class="brand-text"><strong>HORROR FINDINGS</strong><small>RAAT KE US PAAR · RESEARCH ARCHIVE</small></span>
    </a>
    <nav class="nav" id="nav" aria-label="Main">
      <a href="#worldwide">Duniya bhar</a>
      <a href="#entity">Entity &amp; DMT</a>
      <a href="#more">Naye chapters</a>
      <a href="#rs-refs">Sources</a>
    </nav>
    <a class="header-cta" href="{STORIES_URL}">60 kahaniyan padhein</a>
    <button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Menu kholein">☰</button>
  </div>
</header>

<main id="top">
{research}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h4>Horror Findings</h4>
        <p>Yeh “Raat Ke Us Paar” ka research hissa hai — 15 chapters, 46 sources. Kahaniyan alag site par hain: duniya bhar ki 60 kahaniyan, Roman Hindi mein, har kahani ke baad jaanch ka nateeja.</p>
        <p><a href="{STORIES_URL}">→ Raat Ke Us Paar · 60 kahaniyan</a></p>
      </div>
      <div>
        <h4>Chapters</h4>
        <p><a href="#worldwide">Duniya bhar mein dohrne wali ghatnayein</a><br><a href="#entity">Entity, DMT aur doosri zindagi</a><br><a href="#more">Naye research chapters (6)</a><br><a href="#rs-refs">References (R1–R23)</a></p>
      </div>
      <div>
        <h4>Kaise padhein</h4>
        <p>Har chapter ke neeche us ke sources diye hain — publisher, journal, DOI ya PubMed ID, plain text mein. Jo baat sabit nahi hai use sabit nahi kaha gaya: patterns documented hain, “same entity ek hi waqt duniya bhar mein” — yeh claim verified nahi hai.</p>
        <p>Health note: koi dosing, koi self-experiment instruction nahi. Drug-related law aur risks sirf information ke liye hain.</p>
      </div>
    </div>
    <div class="foot-note"><span>© 2026 · RAAT KE US PAAR · HORROR FINDINGS</span></div>
  </div>
</footer>

<script>
(function(){{
  'use strict';
  var btn = document.getElementById('menu-btn');
  var nav = document.getElementById('nav');
  if(!btn || !nav) return;
  btn.addEventListener('click', function(){{
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }});
  nav.addEventListener('click', function(e){{
    if(e.target && e.target.tagName === 'A'){{ nav.classList.remove('open'); btn.setAttribute('aria-expanded','false'); }}
  }});
  /* smooth in-page jumps + keep the header from covering the heading */
  document.querySelectorAll('a[href^="#"]').forEach(function(a){{
    a.addEventListener('click', function(e){{
      var id = a.getAttribute('href').slice(1);
      var el = document.getElementById(id);
      if(!el) return;
      e.preventDefault();
      var y = el.getBoundingClientRect().top + window.pageYOffset - 78;
      window.scrollTo({{ top: y, behavior: 'smooth' }});
      history.replaceState(null, '', '#' + id);
    }});
  }});
}})();
</script>
</body>
</html>
"""

OUT.write_text(page, encoding="utf-8")
imgs = page.count("data:image")
print("wrote", OUT, len(page), "bytes ·", imgs, "inline images ·",
      page.count("<section"), "sections")
