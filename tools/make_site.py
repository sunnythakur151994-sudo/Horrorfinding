#!/usr/bin/env python3
"""
One-time surgery on site/template.html: swap the old 137-story archive for the
uploaded book ("Raat Ke Us Paar", 60 stories) + a dedicated Gaurav Tiwari section.

Run:  python3 tools/make_site.py && python3 site/build.py
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "site" / "template.html"


def load(path, name):
    src = (ROOT / "site" / path).read_text(encoding="utf-8")
    i = src.index(f"const {name} = ") + len(f"const {name} = ")
    dec = json.JSONDecoder()
    val, _ = dec.raw_decode(src[i:])
    return val


BOOK = load("data-book.js", "BOOK")
BOOK_CLUSTERS = load("data-book.js", "BOOK_CLUSTERS")
GAURAV = load("data-gaurav.js", "GAURAV")
RESEARCH = load("data-research.js", "RESEARCH")
RESEARCH_EXTRA = load("data-research2.js", "RESEARCH_EXTRA")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- hero
HERO = '''  <!-- HERO -->
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-bg" aria-hidden="true"><img src="{{IMG:book/k01.webp}}" alt=""></div>
    <div class="wrap hero-inner">
      <div class="hero-kicker"><span class="dot" aria-hidden="true"></span><span>Kitaab · 60 kahaniyan</span><span>·</span><span>Duniya bhar</span></div>
      <h1 id="hero-title">
        <span class="line">Raat ke</span>
        <span class="line"><em>us paar</em> ki kahaniyan</span>
      </h1>
      <p class="hero-sub">Mashhoor jagahen. Suni-sunaayi aahatein. Aur kahani ke peeche ka sach. Kuch jagahen isliye daraati hain kyunki wahaan koi rehta nahi — kuch isliye, kyunki kahani kehti hai ki koi ab bhi wahaan hai. Bhangarh se Japan ke kaidan, London ke Enfield se Mexico ki Llorona, Johannesburg ke Tokoloshe se Tasmania ke Port Arthur tak: <b>60 kahaniyan</b>, nau kshetra, har kahani ke saath uski asli ya saaf label ki hui tasveer, aur ant mein <em>JAANCH MEIN KYA MILA?</em> Uske baad do alag sections: <b>Research special</b> — duniya bhar ke ek jaise kisse, DMT, entity aur dimension par 23 papers ke saath; aur <b>Gaurav Tiwari</b> — zindagi, tahqiqaat aur adhoore sawaal. Sab kuch isi page par.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="#bhangarh">Pehla panna kholein <span aria-hidden="true">↓</span></a>
        <a class="btn btn-ghost" href="#stories">Saari 60 kahaniyan</a>
        <a class="btn btn-ghost" href="#gaurav">Gaurav Tiwari</a>
      </div>
      <div class="hero-facts">
        <div><strong id="stat-total">60</strong><span>Kahaniyan</span></div>
        <div><strong>09</strong><span>Kshetra</span></div>
        <div><strong>23</strong><span>Research papers</span></div>
        <div><strong>0</strong><span>Redirect / bahar ka link</span></div>
      </div>
    </div>
  </section>

  <div class="notice">
    <div class="wrap notice-inner">
      <b>Darwaaza kholne se pehle</b>
      <span>Yeh 60 verified supernatural incidents ki list nahi hai. Ismein lok-katha, urban legend, literary ghost story, historical tragedy aur disputed paranormal case sab shaamil hain. Har kahani ke neeche ka note — <b>JAANCH MEIN KYA MILA?</b> — bataata hai ki record kitni door tak saath deta hai. Jahaan "socho" ya ek scene ke andar le jaati narration mile, woh mahaul banaane ke liye rachaa gaya punarkathan hai, kisi ki personal gawahi nahi. Tasveeron mein asli jagahen, objects, historical artwork aur saaf label ki hui AI illustrations hain — koi building photo uske haunted hone ka proof nahi. Har card par credit likha hai.</span>
    </div>
  </div>
'''


def tiles():
    rows = []
    for i, c in enumerate(BOOK_CLUSTERS, 1):
        n = sum(1 for s in BOOK if s["zone"] == c["key"])
        rows.append(
            f'<a class="cat-tile" href="#zone-{c["key"]}"><span class="ct-num" id="tile-{c["key"]}">{n:02d}</span>'
            f'<h3>{esc(c["label"])}</h3><p>{esc(c["blurb"])}</p><span class="ct-go">Padhein →</span></a>')
    return "\n        ".join(rows)


TYPES = '''  <!-- STORY TYPES / MAP OF THE BOOK -->
  <section class="section" id="types">
    <div class="wrap">
      <div class="section-head">
        <div>
          <div class="eyebrow">Kahaan se shuru karein · nau kshetra · 60 files</div>
          <h2>Duniya ka naksha, ek-ek kahani</h2>
        </div>
        <p>Har kshetra apne hisse mein poora hai — kahin se bhi shuru kar sakte ho. Naam par dabaiye, grid usi jagah le jaayega.</p>
      </div>
      <div class="cat-tiles">
        ''' + tiles() + '''
      </div>
    </div>
  </section>

  <!-- STORY 01 FEATURE -->
  <section class="section section-alt" id="bhangarh">
    <div class="wrap">
      <div class="section-head">
        <div>
          <div class="eyebrow">Kahani 01 / 60 · Bharat</div>
          <h2>Bhangarh ka shraap</h2>
        </div>
        <div class="section-index">ALWAR · RAJASTHAN</div>
      </div>
      <div class="feature">
        <div class="feature-art">
          <span class="feature-badge">ASLI JAGAH KI PHOTO · CHAINWIT. · CC BY-SA 4.0</span>
          <img src="{{IMG:book/k01.webp}}" alt="Bhangarh ka khandahar" loading="lazy">
        </div>
        <div class="feature-copy">
          <div class="feature-tags"><span class="chip">Shraap</span><span class="chip">Kila</span><span class="chip">Kahani 01 / 60</span></div>
          <h3>Saamne poora shehar khada hai, aur usmein rehne waala koi nahi</h3>
          <p>Bhangarh ke khandharon mein dopahar ki dhoop bhi darwazon ke andar poori nahi utarti. Sabse mashhoor kahani Rajkumari Ratnavati ki hai — itr, ek patthar, aur marte hue diya gaya shraap. Ek doosri riwayat Baba Balau Nath ki hai, jinki tapasya par mahal ki chhaaya nahi padni chahiye thi.</p>
          <p>Dono alag lok-kathaayein hain; ek hi ghatna ka pakka itihaas nahi. Aur jaanch mein? Ek report ke mutaabik team ko haunted hone ka saboot nahi mila.</p>
          <div class="hero-actions" style="margin-top:8px">
            <button class="btn btn-primary" type="button" data-open="k01">Poori kahani padhein <span aria-hidden="true">→</span></button>
          </div>
        </div>
      </div>
    </div>
  </section>
'''


def zone_sections():
    out = []
    for i, c in enumerate(BOOK_CLUSTERS, 1):
        n = sum(1 for s in BOOK if s["zone"] == c["key"])
        alt = " section-alt" if i % 2 == 0 else ""
        out.append(f'''  <!-- ZONE {i:02d} · {c["label"].upper()} -->
  <section class="section{alt}" id="zone-{c["key"]}">
    <div class="wrap">
      <div class="section-head">
        <div>
          <div class="eyebrow">Kshetra {i:02d} · {esc(c["label"])}</div>
          <h2>{esc(c["label"])} <span class="count-pill" id="count-{c["key"]}">{n:02d}</span></h2>
        </div>
        <p>{esc(c["blurb"])}. {n} kahaniyan — har ek ke saath credit wali tasveer aur <b>JAANCH MEIN KYA MILA?</b> ka nateeja.</p>
      </div>
      <div class="grid" data-grid="{c["key"]}"></div>
    </div>
  </section>''')
    return "\n\n".join(out)


# ---------------------------------------------------------------- research special
IMG_FOR = {
    "intro": ("research/r-entity-forms.webp", "AI ART · srijanatmak chitra"),
    "c01": ("research/r-sleep-paralysis.webp", "AI ART · srijanatmak chitra"),
    "c03": ("research/r-entity-forms.webp", "AI ART · srijanatmak chitra"),
    "c04": ("research/r-brain-network.webp", "AI ART · srijanatmak chitra"),
    "c07": ("research/r-geometry.webp", "AI ART · srijanatmak chitra"),
}


def table_html(t):
    head = "".join(f"<th>{esc(h)}</th>" for h in t["head"])
    rows = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in t["rows"])
    return f'<div class="rt-scroll"><table class="rt">{("<thead><tr>" + head + "</tr></thead>") if head else ""}<tbody>{rows}</tbody></table></div>'


def research_chapter(ch):
    cid = ch["id"]
    head = ""
    if ch["kicker"]:
        head = f'<div class="rs-kicker">{esc(ch["kicker"])}</div>'
    paras = "\n".join(
        (f'<p class="lead">{esc(p)}</p>' if i == 0 else f"<p>{esc(p)}</p>")
        for i, p in enumerate(ch["paras"]))
    table = table_html(ch["table"]) if ch.get("table") else ""
    img = ""
    if cid in IMG_FOR and cid != "intro":
        f, cap = IMG_FOR[cid]
        img = (f'<figure class="rs-fig"><img src="{{{{IMG:{f}}}}}" alt="" loading="lazy">'
               f'<figcaption>{esc(cap)}</figcaption></figure>')
    return f'''      <article class="rs-ch" id="rs-{cid}">
        {head}
        <h3>{esc(ch["title"])}</h3>
        {img}
        {paras}
        {table}
        <p class="rs-page">Book page {ch["page"]} · Research special</p>
      </article>'''


def research_section():
    intro = RESEARCH["chapters"][0]
    body = [c for c in RESEARCH["chapters"] if c["id"] != "intro"]
    common = [c for c in body if c["id"] in ("c01", "c02", "c08")]
    entity = [c for c in body if c["id"] in ("c03", "c04", "c05", "c06", "c07", "c09")]
    hero_img, hero_cap = IMG_FOR["intro"]
    refs = "".join(
        f'<li><b>{esc(r["id"])}</b><span>{esc(r["text"])}'
        + (f'<em>{esc(r["url"])}</em>' if r.get("url") else "") + "</span></li>"
        for r in RESEARCH["references"])
    intro_paras = "\n".join(esc(p) for p in intro["paras"])
    return f'''  <!-- RESEARCH SPECIAL -->
  <section class="section section-alt" id="research">
    <div class="wrap">
      <div class="section-head">
        <div>
          <div class="eyebrow">Research special · 15 chapters · 46 sources · checked {RESEARCH["checked"]}</div>
          <h2>Ek jaise encounters, alag duniya?</h2>
        </div>
        <div class="section-index">WORLDWIDE · ENTITY · DIMENSION</div>
      </div>

      <div class="rs-hero">
        <figure class="rs-hero-art">
          <img src="{{{{IMG:{hero_img}}}}}" alt="" loading="lazy">
          <figcaption>{esc(hero_cap)} · ye research ka illustration hai, koi witness ki photo nahi</figcaption>
        </figure>
        <div class="rs-hero-copy">
          {intro_paras}
          <p class="rs-boundary"><b>Boundary:</b> yeh focused literature review hai, registered systematic review nahi. Scientific papers aur researchers ke institutional records ko priority di gayi; inaccessible full texts ke liye indexed abstracts use hue. Koi image ya trip report external being ka verified photograph maan kar include nahi kiya gaya.</p>
        </div>
      </div>

      <div class="rs-jump">
        <a href="#worldwide">Duniya bhar mein ek jaise kisse</a>
        <a href="#entity">DMT, entity aur doosri dimension</a>
        <a href="#more">6 naye chapters</a>
        <a href="#rs-refs">23 sources</a>
      </div>
    </div>

    <!-- WORLDWIDE COMMON PATTERNS -->
    <div class="wrap" id="worldwide">
      <div class="rs-block-head">
        <div class="eyebrow">Hissa 01 · common patterns</div>
        <h3>Duniya bhar mein ek jaise kisse — aur unke naam</h3>
        <p>Sleep paralysis se DMT tak: ek hi structure bar-bar — koi paas hai, woh aware lagta hai, body ya time badla hua lagta hai. Naam, chehra aur matlab jagah ke hisaab se badalte hain.</p>
      </div>
{ "".join(research_chapter(c) for c in common) }
    </div>

    <!-- ENTITY / DIMENSION -->
    <div class="wrap" id="entity">
      <div class="rs-block-head">
        <div class="eyebrow">Hissa 02 · DMT, entity, dimension</div>
        <h3>Woh dawa jo “sach ka darwaza” bataayi jaati hai</h3>
        <p>N,N-DMT (smoke/vapour kiya jaane wala) aur Salvia — dono alag substances hain. Yahan wahi research hai jo inke experiences, entities, “doosri zindagi” ke ehsaas aur dimensions ke claims ko test karti hai. Dawa koi truth detector nahi hai.</p>
      </div>
{ "".join(research_chapter(c) for c in entity) }


      <div class="rs-verified">
        <div class="eyebrow">Aaj ka live check · 24 October 2026</div>
        <p>Book ke numbers maine aaj original sources se milaye — teen sabse ahem:</p>
        <ul>
          <li><b>Davis et al. 2020</b> (J Psychopharmacol, 2,561 respondents): entity ne khud encounter shuru kiya — 69%; message/insight mila — 69%; future prediction — 19%; dar bhi report hua — 41%; entity ko conscious 96%, intelligent 96%, benevolent 78%, sacred 70% ne kaha. Sample wahi log the jinke paas pehle se entity encounter tha — isliye ye "sab DMT users entities dekhte hain" nahi hai.</li>
          <li><b>Mago et al. 2026</b> "Computational spirits" (Neuroscience of Consciousness, niaf069): ye <i>theoretical model</i> hai — active inference ke through samjhata hai ki psychedelic state mein brain unpredictable sensations ko "kisi aur agent" se kyun jodta hai. Ye empirical proof nahi.</li>
          <li><b>Jalal et al. 2014</b> (Transcultural Psychiatry): Egypt ke general population mein 48% ne sleep paralysis ko Jinn se joda, Denmark mein aksar log physiological wajah batate hain — matlab same biology, alag kahani.</li>
        </ul>
        <p class="rs-note">Baaki 20 references book ke apne research pages se hain; unke DOI/PubMed numbers neeche diye hain, taaki aap khud verify kar sakein.</p>
      </div>
      <div class="rs-warn">
        <b>Research ko self-experiment se replace mat karo.</b>
        DMT/Salvia “truth detector” nahi hain. Studies mein intense fear, disorientation, dissociation aur memory disturbance report hui hain; medical screening aur supervision results ke context ka hissa hain. India mein NDPS Act ke tehat aise substances rakhna, bechna ya use karna illegal hai — kanoon aur khatra dono asli hain.
      </div>
    </div>

    {research_extra_block()}

    <!-- REFERENCES -->
    <div class="wrap" id="rs-refs">
      <div class="rs-block-head">
        <div class="eyebrow">Sources · {len(RESEARCH["references"])} items</div>
        <h3>Papers jinpar ye section khada hai</h3>
        <p>Yeh wahi references hain jo book ke research pages par diye gaye hain (DOI/PubMed). Links clickable nahi rakhe — site ka rule: koi bahar ka redirect nahi. Naam copy karke search kar sakte ho.</p>
      </div>
      <ol class="rs-refs">{refs}</ol>
      <p class="rs-note">Access note: kuch publisher/PubMed full-page requests blocked ya redirected the; un cases mein indexed abstracts, DOI pages aur institutional records se factual details verify ki gayi. Theoretical papers ko empirical trial results se alag label kiya gaya.</p>
    </div>
  </section>
'''


def research_extra_chapter(ch):
    cid = ch["id"]
    img = ""
    if ch.get("img"):
        img = (f'<figure class="rs-fig"><img src="{{{{IMG:{ch["img"]}}}}}" alt="" loading="lazy">'
               f'<figcaption>AI ART · srijanatmak chitra</figcaption></figure>')
    paras = "\n".join(
        (f'<p class="lead">{p}</p>' if i == 0 else f"<p>{p}</p>") for i, p in enumerate(ch["paras"]))
    srcs = "".join(
        f'<li><span>{esc(t)}</span><em>{esc(u)}</em></li>' for t, u in ch["sources"])
    return f'''      <article class="rs-ch rs-extra" id="rs-{cid}">
        <div class="rs-kicker">{esc(ch["kicker"])}</div>
        <h3>{esc(ch["title"])}</h3>
        {img}
        {paras}
        <div class="rs-chsrc"><div class="rs-chsrc-h">Sources</div><ul>{srcs}</ul></div>
      </article>'''


def research_extra_block():
    chapters = "".join(research_extra_chapter(c) for c in RESEARCH_EXTRA["chapters"])
    return f'''
    <!-- HISSA 03 · site-written follow-ups -->
    <div class="wrap" id="more">
      <div class="rs-block-head">
        <div class="eyebrow">Hissa 03 · naye chapters · 6</div>
        <h3>Aur sawaal jo research se aage jaate hain</h3>
        <p>{esc(RESEARCH_EXTRA["intro"])}</p>
      </div>
{chapters}
    </div>
'''


# ---------------------------------------------------------------- gaurav section
def gaurav_chapter(ch, i):
    body = "\n".join(f'<p>{esc(p)}</p>' for p in ch["paras"])
    img = ""
    if ch.get("img"):
        cap = esc(ch.get("imgcap") or "")
        img = (f'<figure class="gt-fig"><img src="{{{{IMG:{ch["img"]}}}}}" alt="{esc(ch["title"])}" loading="lazy">'
               f'<figcaption>{cap}</figcaption></figure>')
    notes = "".join(f'<p class="gt-note">{esc(n)}</p>' for n in ch.get("notes", []))
    srcs = ""
    if ch.get("sources"):
        srcs = '<p class="gt-src">Sources: ' + " · ".join(esc(x) for x in ch["sources"]) + "</p>"
    return f'''      <article class="gt-ch" id="{ch["id"]}">
        <div class="gt-ch-head">
          <span class="gt-num">{i:02d}</span>
          <div>
            <div class="eyebrow">{esc(ch["kicker"])}</div>
            <h3>{esc(ch["title"])}</h3>
            {f'<p class="gt-sub">{esc(ch["sub"])}</p>' if ch.get("sub") else ''}
          </div>
        </div>
        {img}
        {body}
        {notes}
        {srcs}
      </article>'''


GAURAV_SECTION = '''  <!-- GAURAV TIWARI -->
  <section class="section section-gt" id="gaurav">
    <div class="wrap">
      <div class="section-head">
        <div>
          <div class="eyebrow">Alag section · Research narrative · 10 chapters</div>
          <h2>Gaurav Tiwari: zindagi, tahqiqaat aur adhoore sawaal</h2>
        </div>
        <div class="section-index">FLORIDA → INDIA → AUSTRALIA · 2016</div>
      </div>

      <div class="gt-hero">
        <figure class="gt-hero-art">
          <img src="{{IMG:gaurav/hero.webp}}" alt="Gaurav Tiwari — published photograph" loading="lazy">
          <figcaption>Gaurav Tiwari ki investigation ke dauraan li gayi published photograph. Source: Man's World. Photographer aur exact case/date article mein specified nahi hain.</figcaption>
        </figure>
        <div class="gt-hero-copy">
          <p class="gt-quote">"Kuch log andhere se door rehte hain. Kuch uske baare mein kahaniyaan sunaate hain. Gaurav Tiwari ne us andhere ko apne kaam ka sawaal bana liya: jo mehsoos ho raha hai, kya use samjha bhi ja sakta hai?"</p>
          <p>Unke apne bayaan, saathiyon ki yaadein, television investigations aur contemporary reporting par aadharit ek original Roman Hindi narrative. Isme AI-generated photographs nahi hain — jo tasveer published hai, wahi yahan hai, apne caption aur provenance note ke saath.</p>
          <ul class="gt-facts">
            <li><b>Shuruaat</b><span>Florida mein commercial flying training; phir 2009 mein India wapsi aur Indian Paranormal Society</span></li>
            <li><b>Kaam</b><span>G.R.I.P. lead investigator; Supernatural Indian, Bhoot Aaya, MTV, aur <i>Haunting: Australia</i></span></li>
            <li><b>Record</b><span>Old Geelong Gaol ki published full-spectrum photo — sabse seedhi provenance, phir bhi forensic verification nahi</span></li>
            <li><b>7 July 2016</b><span>Dwarka ke ghar mein dead mile; police ne available information par foul play se inkaar kiya</span></li>
          </ul>
          <p class="gt-boundary"><b>Boundary:</b> unki har private investigation ki complete case diary public mein nahi hai. Isliye ye unke poore jeevan ka public-source overview hai, unke har case ka official archive nahi. Dar ki jagah bachi rahegi, lekin record ki jagah kalpana nahi legi.</p>
        </div>
      </div>

      <nav class="gt-nav" aria-label="Gaurav Tiwari chapters">
        <span class="gt-nav-label">Chapters</span>
        ''' + "\n        ".join(f'<a href="#{c["id"]}">{i:02d} · {esc(c["title"])}</a>' for i, c in enumerate(GAURAV, 1)) + '''
      </nav>

      <div class="gt-chapters">
''' + "\n".join(gaurav_chapter(c, i) for i, c in enumerate(GAURAV, 1)) + '''
      </div>

      <div class="gt-imageprovenance">
        <div class="eyebrow">Tasveeron ka record</div>
        <ul>
          <li><b>Hero:</b> Man's World mein Gaurav ki investigation photo. Exact date, location aur photographer unspecified.</li>
          <li><b>Chapter 05:</b> Australian programme ka published cast portrait (Gaurav extreme left). Article ise IPS team kehta hai, par yeh programme ka cast portrait hai.</li>
          <li><b>Chapter 06:</b> Old Geelong Gaol ki alleged "Gaol Guard" photo — Allen Tiller ke caption/account mein Gaurav ko credited. Public copy; original capture metadata available nahi.</li>
          <li><b>Chapter 07:</b> Rayleen Kable ki kitchen still, Tiller ke published archive se. Gaurav photographer hone ka daava nahi.</li>
        </ul>
        <p>Images ko evidence badalne waale enhancement, nayi entity ya AI recreation ke bina pesh kiya gaya hai. Published image ke rights uske respective rights-holder ke paas hain.</p>
      </div>
    </div>
  </section>
'''


def main():
    h = TEMPLATE.read_text(encoding="utf-8")

    # ---- nav ----
    h = re.sub(r'<nav class="nav" id="nav" aria-label="Main">.*?</nav>',
               '''<nav class="nav" id="nav" aria-label="Main">
      <a href="#types">Naksha</a>
      <a href="#zone-india">Bharat</a>
      <a href="#zone-britain">Britain</a>
      <a href="#zone-namerica">America</a>
      <a href="#research">Research</a>
      <a href="#gaurav">Gaurav Tiwari</a>
      <a href="#video">Video</a>
    </nav>''', h, flags=re.S)

    # ---- brand tag ----
    h = h.replace('AROUND INDIA · FIELD ARCHIVE', 'RAAT KE US PAAR · FIELD ARCHIVE')
    h = h.replace('aria-label="Horror Findings Around India — home"', 'aria-label="Raat Ke Us Paar — home"')

    # ---- hero + notice ----
    start = h.index('  <!-- HERO -->')
    end = h.index('  <!-- STORY TYPES / MAP OF THE BOOK -->')
    h = h[:start] + HERO + "\n" + h[end:]

    # ---- everything from STORY TYPES up to VIDEO ----
    start = h.index('  <!-- STORY TYPES / MAP OF THE BOOK -->')
    end = h.index('  <!-- VIDEO -->')
    middle = TYPES + "\n" + zone_sections() + "\n\n" + research_section() + "\n\n" + GAURAV_SECTION + "\n\n"
    h = h[:start] + middle + h[end:]

    # ---- video section copy (Monkey Man is story 07 now) ----
    h = h.replace('<div class="eyebrow">Video · archive footage</div>', '<div class="eyebrow">Kahani 07 ka record · archive footage</div>')
    h = h.replace('<p style="margin-top:14px"><button class="btn btn-ghost" type="button" data-open="monkeyman">Poori kahani padhein</button></p>',
                  '<p style="margin-top:14px"><button class="btn btn-ghost" type="button" data-open="k07">Poori kahani padhein</button></p>')

    # ---- evidence section: keep, retitle ----
    h = h.replace('<div class="eyebrow">Aapke liye · 4 rules</div>', '<div class="eyebrow">Aapke liye · 4 rules</div>')

    # ---- footer ----
    h = re.sub(r'<footer class="site-footer">.*?</footer>', '''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h4>Raat Ke Us Paar</h4>
        <p>60 kahaniyan, Roman Hindi mein — mashhoor jagahen, suni-sunaayi aahatein, aur har kahani ke baad jaanch ka nateeja. Bhangarh se Larnach Castle tak.</p>
        <p>Sab kuch isi page par: koi redirect nahi, koi bahar ka link nahi, video bhi yahin chalta hai. Alag section mein Gaurav Tiwari ki research narrative.</p>
      </div>
      <div>
        <h4>Kahaniyan</h4>
        <p><a href="#bhangarh">Kahani 01 · Bhangarh</a><br><a href="#zone-india">Bharat (12)</a><br><a href="#zone-britain">Britain aur Ireland (9)</a><br><a href="#gaurav">Gaurav Tiwari</a></p>
      </div>
      <div>
        <h4>Tasveerein</h4>
        <p>Har card par credit likha hai — "ASLI TASVEER · &lt;photographer&gt; · &lt;license&gt;" ya "AI ILLUSTRATION". Book ke andar wahi credits hain jo original pages par diye gaye the.</p>
        <p>Koi building photo uske haunted hone ka saboot nahi hai. Gaurav section ki tasveerein published copies hain, AI recreation nahi.</p>
      </div>
    </div>
    <div class="foot-note"><span>© 2026 · RAAT KE US PAAR · 60 KAHANIYAN</span><span>FOLKLORE ≠ PROOF · SAB KAHANIYAN, EK PAGE</span></div>
  </div>
</footer>''', h, flags=re.S)

    # ---- JS: category names from clusters, cats list, sources line ----
    h = h.replace("var CAT_NAME = {village:'Gaon ki ghatna', ancient:'Puraani kahani', case:'Case file', heritage:'Heritage file', tantra:'Kala jadu file'};",
                  "var CAT_NAME = (function(){var m={};(typeof BOOK_CLUSTERS!=='undefined'?BOOK_CLUSTERS:[]).forEach(function(c){m[c.key]=c.label;});return m;})();")
    h = h.replace("var cats = ['village','ancient','case','heritage','tantra'];",
                  "var cats = (typeof BOOK_CLUSTERS !== 'undefined' ? BOOK_CLUSTERS.map(function(c){return c.key;}) : []);")
    h = h.replace("var CAT_NAME = {village:'Gaon ki ghatna'", "var CAT_NAME = {village:'Gaon ki ghatna'")  # no-op guard

    # card credits: AI vs real-photo wording comes from s.label already
    h = h.replace("var credit = s.art ? esc(s.credit || 'AI ART') : 'FILE PLATE · SRJANATMAK';",
                  "var credit = esc(s.credit || (s.isAI ? 'AI ILLUSTRATION' : 'ASLI TASVEER'));")

    # reader: append sources under the verdict box
    h = h.replace("readerVerdict.innerHTML = s.verdict || '<strong>Sach kya hai?</strong> Yeh ek kalpanik narration hai.';",
                  "readerVerdict.innerHTML = (s.verdict || '') + (s.sources && s.sources.length ? '<p class=\"src-line\">Sources: ' + s.sources.map(function(x){return esc(x);}).join(' · ') + '</p>' : '');")

    # reader eyebrow: no "tag" field in book data
    h = h.replace("readerEyebrow.textContent = 'File ' + s.no + ' · ' + s.zoneLabel + ' · ' + s.tag;",
                  "readerEyebrow.textContent = 'Kahani ' + s.no + '/60 · ' + s.zoneLabel + ' · ' + (s.isAI ? 'AI ILLUSTRATION' : 'ASLI TASVEER');")

    # ---- CSS additions ----
    css_add = '''
/* ---------- book tiles: 9 clusters ---------- */
.cat-tiles{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}

/* ---------- research special ---------- */
.rs-hero{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start;margin:6px 0 20px}
.rs-hero-art{margin:0;border:1px solid var(--line);background:#0b0d0c}
.rs-hero-art img{display:block;width:100%;height:auto;filter:saturate(.9)}
.rs-hero-art figcaption{padding:8px 11px;font:400 10.5px/1.5 var(--mono);letter-spacing:.03em;color:#8d968c;border-top:1px solid var(--line)}
.rs-hero-copy p{font-size:14px;line-height:1.72;color:#b8bfb4;margin:0 0 11px}
.rs-boundary{border:1px solid rgba(232,121,79,.3);background:rgba(232,121,79,.06);padding:12px 14px;font-size:12.5px!important;color:#cfd4ca!important}
.rs-jump{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 4px}
.rs-jump a{font:400 11.5px/1.2 var(--mono);letter-spacing:.03em;color:#cfd5ca;text-decoration:none;border:1px solid var(--line);padding:8px 11px}
.rs-jump a:hover{border-color:rgba(232,121,79,.6);color:#fff;background:rgba(232,121,79,.08)}
.rs-block-head{margin:34px 0 16px;padding-top:20px;border-top:1px solid var(--line)}
.rs-block-head h3{margin:6px 0 6px;font:400 26px/1.22 var(--serif);letter-spacing:-.01em}
.rs-block-head p{margin:0;max-width:70ch;font-size:13.5px;line-height:1.65;color:#a9b1a7}
.rs-ch{border:1px solid var(--line);background:rgba(255,255,255,.02);padding:20px 22px;margin-bottom:14px}
.rs-kicker{font:700 9.5px var(--mono);letter-spacing:.18em;text-transform:uppercase;color:var(--ember)}
.rs-ch h3{margin:8px 0 12px;font:400 22px/1.25 var(--serif);letter-spacing:-.01em}
.rs-ch p{font-size:14px;line-height:1.74;color:#c2c8bc;margin:0 0 10px}
.rs-ch p.lead{color:#dfe3d9}
.rs-fig{margin:0 0 14px;border:1px solid var(--line);background:#0b0d0c}
.rs-fig img{display:block;width:100%;height:auto;max-height:340px;object-fit:cover}
.rs-fig figcaption{padding:7px 10px;font:400 10px/1.4 var(--mono);letter-spacing:.04em;color:#8d968c;border-top:1px solid var(--line)}
.rs-page{margin:8px 0 0!important;font:400 10px var(--mono)!important;letter-spacing:.1em;text-transform:uppercase;color:#79817a!important}
.rt-scroll{overflow-x:auto;margin:6px 0 12px;border:1px solid var(--line)}
table.rt{border-collapse:collapse;width:100%;min-width:560px;font-size:12.5px;line-height:1.6}
table.rt th{text-align:left;padding:9px 11px;background:rgba(232,121,79,.1);font:700 9px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:#e6c9b4;border-bottom:1px solid var(--line)}
table.rt td{padding:9px 11px;vertical-align:top;color:#b8bfb4;border-bottom:1px solid rgba(233,228,216,.08)}
table.rt tr:last-child td{border-bottom:none}
table.rt td:first-child{color:#ece7db;font-weight:600;min-width:120px}
.rs-verified{margin:18px 0 0;border:1px solid var(--line);background:rgba(0,0,0,.25);padding:16px 18px}
.rs-verified p{margin:8px 0 10px;font-size:13px;line-height:1.68;color:#c2c8bc}
.rs-verified ul{margin:0;padding-left:18px;display:grid;gap:8px}
.rs-verified li{font-size:12.8px;line-height:1.66;color:#b8bfb4}
.rs-verified b{color:#ece7db}
.rs-warn{margin:16px 0 0;border:1px solid rgba(232,121,79,.45);background:rgba(232,121,79,.09);padding:14px 16px;font-size:13px;line-height:1.65;color:#e7ddd1}
.rs-warn b{color:#fff}
.rs-refs{list-style:none;margin:10px 0 0;padding:0;display:grid;gap:8px;counter-reset:r}
.rs-refs li{display:grid;grid-template-columns:44px 1fr;gap:10px;padding:9px 0;border-top:1px solid var(--line);font-size:12.5px;line-height:1.6;color:#b8bfb4}
.rs-refs b{font:700 10px var(--mono);letter-spacing:.08em;color:var(--ember2)}
.rs-refs em{display:block;margin-top:3px;font:400 10px/1.4 var(--mono);letter-spacing:.02em;color:#79817a;font-style:normal;word-break:break-all}
.rs-chsrc{margin:12px 0 0;padding-top:10px;border-top:1px dashed rgba(233,228,216,.14)}
.rs-chsrc-h{font:700 9px var(--mono);letter-spacing:.16em;text-transform:uppercase;color:#8d968c;margin-bottom:6px}
.rs-chsrc ul{list-style:none;margin:0;padding:0;display:grid;gap:5px}
.rs-chsrc li{font-size:12px;line-height:1.55;color:#b0b7ac}
.rs-chsrc em{display:block;font:400 9.5px/1.45 var(--mono);letter-spacing:.02em;color:#79817a;font-style:normal;word-break:break-all;margin-top:1px}
.rs-extra{border-left:2px solid rgba(232,121,79,.45)}
.rs-note{margin:14px 0 0;font-size:11.5px;line-height:1.6;color:#8d968c}
@media (max-width:900px){.rs-hero{grid-template-columns:1fr}.rs-ch{padding:17px}}
/* ---------- gaurav tiwari section ---------- */
.section-gt{background:linear-gradient(180deg,rgba(232,121,79,.05),transparent 40%);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.gt-hero{display:grid;grid-template-columns:1.05fr .95fr;gap:26px;align-items:start;margin:6px 0 26px}
.gt-hero-art{margin:0;border:1px solid var(--line);background:#0b0d0c}
.gt-hero-art img{display:block;width:100%;height:auto;filter:saturate(.85) contrast(1.05)}
.gt-hero-art figcaption{padding:9px 11px;font:400 10.5px/1.5 var(--mono);letter-spacing:.03em;color:#8d968c;border-top:1px solid var(--line)}
.gt-quote{margin:0 0 14px;padding-left:14px;border-left:2px solid var(--ember);font:400 18px/1.6 var(--serif);color:#ece7db}
.gt-hero-copy p{font-size:14px;line-height:1.7;color:#b8bfb4}
.gt-facts{list-style:none;margin:16px 0;padding:0;display:grid;gap:8px}
.gt-facts li{display:grid;grid-template-columns:104px 1fr;gap:10px;padding:9px 0;border-top:1px solid var(--line);font-size:13px;line-height:1.55;color:#b8bfb4}
.gt-facts b{font:700 9.5px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ember2)}
.gt-boundary{border:1px solid rgba(232,121,79,.3);background:rgba(232,121,79,.06);padding:12px 14px;font-size:12.5px!important;color:#cfd4ca!important}
.gt-nav{display:flex;flex-wrap:wrap;gap:7px;align-items:center;padding:14px 0 20px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-bottom:24px}
.gt-nav-label{font:700 9.5px var(--mono);letter-spacing:.16em;text-transform:uppercase;color:#8d968c;margin-right:6px}
.gt-nav a{font:400 11.5px/1.2 var(--mono);letter-spacing:.03em;color:#cfd5ca;text-decoration:none;border:1px solid var(--line);padding:6px 9px;transition:.16s}
.gt-nav a:hover{border-color:rgba(232,121,79,.6);color:#fff;background:rgba(232,121,79,.08)}
.gt-chapters{display:grid;gap:22px}
.gt-ch{border:1px solid var(--line);background:rgba(255,255,255,.02);padding:22px 24px}
.gt-ch-head{display:flex;gap:14px;align-items:flex-start;margin-bottom:12px}
.gt-num{font:400 30px/1 var(--serif);color:rgba(232,121,79,.55);min-width:42px}
.gt-ch h3{margin:4px 0 0;font:400 23px/1.25 var(--serif);letter-spacing:-.01em}
.gt-sub{margin:5px 0 0;font:400 11.5px/1.5 var(--mono);letter-spacing:.04em;color:#9aa39a}
.gt-ch p{font-size:14.5px;line-height:1.75;color:#c6ccc0;margin:0 0 11px}
.gt-ch p:first-of-type{color:#dfe3d9}
.gt-fig{margin:14px 0 16px;border:1px solid var(--line);background:#0b0d0c}
.gt-fig img{display:block;width:100%;height:auto;max-height:420px;object-fit:cover}
.gt-fig figcaption{padding:8px 11px;font:400 10.5px/1.5 var(--mono);letter-spacing:.03em;color:#8d968c;border-top:1px solid var(--line)}
.gt-note{margin:12px 0!important;padding:11px 13px;border-left:2px solid var(--ember);background:rgba(232,121,79,.06);font-size:13px!important;color:#d7dcd2!important}
.gt-src{font:400 10.5px/1.5 var(--mono)!important;letter-spacing:.06em;color:#8d968c!important;text-transform:uppercase}
.gt-imageprovenance{margin-top:26px;border:1px solid var(--line);padding:20px 22px;background:rgba(0,0,0,.25)}
.gt-imageprovenance ul{margin:10px 0 12px;padding-left:18px;display:grid;gap:7px}
.gt-imageprovenance li{font-size:12.5px;line-height:1.6;color:#b8bfb4}
.gt-imageprovenance b{color:#ece7db}
.gt-imageprovenance p{font-size:12px;line-height:1.65;color:#9aa39a;margin:0}
.src-line{margin:10px 0 0;font:400 10.5px/1.5 var(--mono);letter-spacing:.05em;color:#8d968c;text-transform:uppercase}
@media (max-width:900px){.gt-hero{grid-template-columns:1fr}.gt-ch{padding:18px}.gt-facts li{grid-template-columns:1fr;gap:3px}}
'''
    h = h.replace("@media (prefers-reduced-motion:reduce){", css_add + "@media (prefers-reduced-motion:reduce){", 1)

    TEMPLATE.write_text(h, encoding="utf-8")
    print("template rebuilt:", len(h), "bytes")


if __name__ == "__main__":
    main()
