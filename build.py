#!/usr/bin/env python3
"""Generates all 8 pages from one shared shell (v3 UI).

Layout language follows the supplied reference screenshots: opaque white header
with centred logo and circular buttons, curved organic section boundaries,
botanical watermarks, hollow outlined display type, floating Book button.
All Sambodhi copy, links, images and functionality carry over unchanged.
"""
import pathlib

OUT  = pathlib.Path(__file__).parent
BOOK = "https://live.ipms247.com/booking/book-rooms-sambodhiretreat"
IMG  = "https://www.sambodhiretreat.org/images/"
# Home hero slides. Local files: the reveal is the first thing a visitor sees,
# so the first screen must not wait on a remote host.
HERO_SLIDES = ["New_img/slider4.png", "New_img/slider3.png",
               "New_img/slider2.png", "New_img/slider1.png"]
# Our Story imagery. Both are cropped to a tall 3:4 frame by CSS, so pick
# photographs whose subject sits centre-frame.
# Cropped from the clean photographic half of the client's New_img/our_story.png
# mockup — that file is a design comp with type and the logo baked in, so it
# cannot be dropped in as a photograph.
STORY1 = "New_img/story-grounds.jpg"
STORY2 = IMG + "homePage-Villas/green-cave.jpg"
MAPQ = "https://www.google.com/maps/place/Sambodhi+Retreat"
MAPEMBED = ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3625.427143317658"
            "!2d84.99642021499922!3d24.677839184140325!2m3!1f0!2f0!3f0!3m2!1i1024!2i768"
            "!4f13.1!3m3!1m2!1s0x39f32c5b581fca2b%3A0x7ffce0110e9335bb!2sSambodhi%20Retreat"
            "!5e0!3m2!1sen!2sin!4v1605515197115!5m2!1sen!2sin")

ARROW  = ('<svg class="btn__arrow" viewBox="0 0 15 9" fill="none" aria-hidden="true">'
          '<path d="M10 1l4 3.5L10 8M0 4.5h14" stroke="currentColor" stroke-width="1"/></svg>')
ARROW_L = ('<svg viewBox="0 0 34 11" fill="none" aria-hidden="true">'
           '<path d="M27 1l6 4.5L27 10M0 5.5h32" stroke="currentColor" stroke-width="1.1"/></svg>')
ARROW_S = ('<svg viewBox="0 0 26 10" fill="none" aria-hidden="true">'
           '<path d="M20 1l5 4L20 9M0 5h24" stroke="currentColor" stroke-width="1.1"/></svg>')
PIN = ('<svg viewBox="0 0 11 14" fill="none" aria-hidden="true">'
       '<path d="M5.5 13S10 8.6 10 5.2A4.5 4.5 0 1 0 1 5.2C1 8.6 5.5 13 5.5 13Z" stroke="currentColor" stroke-width="1"/>'
       '<circle cx="5.5" cy="5.2" r="1.6" stroke="currentColor" stroke-width="1"/></svg>')
VAN = ('<svg viewBox="0 0 30 18" fill="none" aria-hidden="true">'
       '<path d="M3 12h1a2.4 2.4 0 004.8 0h9.4a2.4 2.4 0 004.8 0H27V7.5L23.5 4H16V2H6" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>'
       '<path d="M0 6h7M1 9h5" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/></svg>')

# --- curved section boundaries -------------------------------------------
def curve(kind, colour, where="top", extra=""):
    paths = {
        "wave": "M0,150 H1440 V28 C1230,22 1040,16 760,40 C480,64 300,150 0,150 Z",
        "arc":  "M0,150 H1440 V44 C1120,146 320,146 0,44 Z",
        "soft": "M0,150 H1440 V56 C1180,20 980,86 700,66 C420,46 220,96 0,74 Z",
    }
    cls = f"curve curve--{where}{(' ' + extra) if extra else ''}"
    return (f'<div class="{cls}" style="--c:{colour}" aria-hidden="true">'
            f'<svg viewBox="0 0 1440 150" preserveAspectRatio="none">'
            f'<path d="{paths[kind]}"/></svg></div>')

def wm(pos, kind=""):
    k = f" wm--{kind}" if kind else ""
    return f'<span class="wm{k} wm--{pos}" aria-hidden="true"></span>'

NAV = [("index.html","Home"),("accommodations.html","Accommodations"),
       ("banquet-halls.html","Banquet Halls"),("event-venue.html","Event Venue"),
       ("dining.html","Dining"),("gallery.html","Gallery"),
       ("blog.html","Blog"),("contact.html","Contact")]

def nav_html(cur, lower=False):
    out=[]
    for h,l in NAV:
        a = ' aria-current="page"' if h==cur else ""
        out.append(f'<a href="{h}"{a}>{l.lower() if lower else l}</a>')
    return "\n      ".join(out)

# One photograph per destination for the menu's image panel.
MENUIMG = {
 "index.html":           IMG+"Homepage_Resort_INDEX/top-slider-img8.jpg",
 "accommodations.html":  IMG+"Homepage_Resort_INDEX/top-slider-img11.jpg",
 "banquet-halls.html":   IMG+"promotions/1.jpg",
 "event-venue.html":     IMG+"Gallery/top-post-img3.jpg",
 "dining.html":          IMG+"dining/restaurant1.jpg",
 "gallery.html":         IMG+"Homepage_Resort_INDEX/top-slider-img10.jpg",
 "blog.html":            IMG+"Gallery/Top-5-Places-in-Bodh-Gaya.jpg",
 "contact.html":         IMG+"Homepage_Resort_INDEX/top-slider-img5.jpg",
}

def menu_nav(cur):
    """Left-hand navigation. Each link names the panel image it reveals."""
    out=[]
    for i,(h,l) in enumerate(NAV):
        a = ' aria-current="page"' if h==cur else ""
        out.append(
          f'<a href="{h}"{a} data-menu-img="{MENUIMG[h]}" style="--i:{i}">'
          f'<span class="ovl__num">{i+1:02d}</span>'
          f'<span class="ovl__word">{l}</span>'
          f'<span class="ovl__arrow" aria-hidden="true">'
          f'<svg viewBox="0 0 28 8" fill="none"><path d="M0 4h25M21 1l4 3-4 3" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"/></svg>'
          f'</span></a>')
    return "\n        ".join(out)

def menu_panel(cur):
    """Right-hand image panel: one layer per destination, crossfaded on hover."""
    layers=[]
    for i,(h,l) in enumerate(NAV):
        act = " is-active" if h==cur else ""
        layers.append(f'<div class="ovl__shot{act}" data-for="{MENUIMG[h]}" '
                      f'style="background-image:url(\'{MENUIMG[h]}\')"></div>')
    return "\n      ".join(layers)

# --- shared shell ---------------------------------------------------------
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="icon" href="assets/img/logo.png">
<script>document.documentElement.className += ' js';</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://www.sambodhiretreat.org">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>

<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
  <clipPath id="clipWaveBottom" clipPathUnits="objectBoundingBox">
    <path d="M0,0 H1 V0.915 C0.74,1.005 0.42,0.875 0,0.945 Z"/>
  </clipPath>
  <clipPath id="clipWaveTop" clipPathUnits="objectBoundingBox">
    <path d="M0,0.07 C0.33,-0.015 0.66,0.105 1,0.03 V1 H0 Z"/>
  </clipPath>
</defs></svg>

<div class="page-fade" aria-hidden="true"><img src="assets/img/logo.png" alt=""></div>

<header class="hdr">
  <div class="hdr__top">
    <button class="menu-btn" aria-expanded="false" aria-controls="ovl" aria-label="Open menu">
      <span class="burger-i" aria-hidden="true"><span></span><span></span><span></span></span>
    </button>

    <a class="brand" href="index.html" aria-label="Sambodhi Retreat, home">
      <img src="assets/img/logo.png" alt="Sambodhi Retreat">
    </a>

    <div class="hdr__right">
      <a class="btn--pill" href="{BOOK}" target="_blank" rel="noopener">Book a stay</a>
      <a class="iconbtn" href="tel:+917488535210" aria-label="Call Sambodhi Retreat">
        <svg viewBox="0 0 17 17" fill="none" aria-hidden="true"><path d="M15.5 12.3v2.2a1.4 1.4 0 01-1.6 1.4A14 14 0 011.1 3.1 1.4 1.4 0 012.5 1.5h2.2a1.4 1.4 0 011.4 1.2c.1.7.3 1.4.5 2a1.4 1.4 0 01-.3 1.5l-.9.9a11.4 11.4 0 004.3 4.3l.9-.9a1.4 1.4 0 011.5-.3c.6.2 1.3.4 2 .5a1.4 1.4 0 011.4 1.6z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>
      </a>
    </div>
  </div>

  <nav class="hdr__nav" aria-label="Primary">
    {TOPNAV}
  </nav>
</header>

<div class="ovl" id="ovl" aria-hidden="true">
  <button class="ovl__close" aria-label="Close menu">
    <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="1.3"/></svg>
  </button>

  <div class="ovl__left">
    <span class="wm wm--branch wm--l" aria-hidden="true"></span>
    <p class="ovl__mark"><img src="assets/img/logo.png" alt="Sambodhi Retreat"></p>
    <a class="ovl__tel" href="tel:+917488535210">+91 74885 35210</a>
    <nav class="ovl__nav" aria-label="Primary">
        {MENUNAV}
    </nav>
    <div class="ovl__foot">
      <a class="btn btn--gold" href="{BOOK}" target="_blank" rel="noopener">book a stay</a>
    </div>
  </div>

  <div class="ovl__right" aria-hidden="true">
      {MENUPANEL}
    <span class="ovl__shot-scrim"></span>
  </div>
</div>

<a class="fab" href="{BOOK}" target="_blank" rel="noopener" aria-label="Book your stay">
  <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
    <rect x="3" y="5" width="18" height="16" rx="2.5" stroke="currentColor" stroke-width="1.5"/>
    <path d="M3 10h18M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
    <path d="M9 15.5l2.2 2.2L16 13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  <span>Book</span>
</a>

<main id="main">
"""

FOOT = """
</main>

<!-- Footer. A dark botanical ground with a single large ivory panel lifted off
     it — the brand mark and socials left, two navigation columns, the
     newsletter right, and a hairline bar beneath. Every link, number and
     address carried over from the previous footer unchanged.
     Styles: site.css section 36. -->
<footer class="ftr ftr--panel">
  <span class="wm wm--leafbig wm--bl" aria-hidden="true"></span>
  <span class="wm wm--branch wm--tr" aria-hidden="true"></span>

  <div class="wrap">
    <div class="ftr__panel">
      <div class="ftr__grid">
        <div class="ftr__brandcol">
          <p class="ftr__mark"><img src="assets/img/logo.png" alt="Sambodhi Retreat"></p>
          <p class="ftr__blurb">Hathiyar, Bodhgaya, Gaya, Bihar &mdash; 824231, India</p>
          <p class="ftr__blurb"><a href="tel:+917488535210">+91 74885 35210</a> &middot; <a href="tel:+917488535208">+91 74885 35208</a><br><a href="mailto:info@sambodhiretreat.com">info@sambodhiretreat.com</a></p>
          <div class="ftr__social">
            <a href="https://www.instagram.com/sambodhiretreat/" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg></a>
            <a href="https://www.facebook.com/SambodhiRetreatBodhgaya/" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-8h2.7l.4-3.1h-3.1V7.9c0-.9.25-1.5 1.55-1.5H16.7V3.6c-.29-.04-1.3-.13-2.47-.13-2.45 0-4.13 1.5-4.13 4.24V9.9H7.4V13h2.7v8h3.4z"/></svg></a>
            <a href="https://twitter.com/sambodhiretreat" target="_blank" rel="noopener" aria-label="X"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 3h3l-6.6 7.5L21.7 21h-5.9l-4.3-5.6L6.4 21H3.4l7-8L2.6 3h6l3.9 5.2L17.5 3zm-1.05 16.2h1.65L7.6 4.7H5.85l10.6 14.5z"/></svg></a>
            <a href="https://www.linkedin.com/company/sambodhi-retreat/" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.94 8.5H4.1V20h2.84V8.5zM5.52 4a1.65 1.65 0 100 3.3 1.65 1.65 0 000-3.3zM20 13.7c0-3.1-1.66-4.55-3.87-4.55-1.79 0-2.59.98-3.03 1.67V8.5H10.3V20h2.83v-6.4c0-.34.02-.68.13-.92.28-.67.9-1.37 1.94-1.37 1.37 0 1.92 1.04 1.92 2.57V20H20v-6.3z"/></svg></a>
          </div>
        </div>

        <nav class="ftr__col" aria-label="Footer">
          <h4 class="ftr__ch">Explore</h4>
          {FOOTNAV}
        </nav>

        <nav class="ftr__col" aria-label="Policies">
          <h4 class="ftr__ch">Policies</h4>
          <a href="https://www.sambodhiretreat.org/privacypolicy.aspx" target="_blank" rel="noopener">Privacy &amp; Policy</a>
          <a href="https://www.sambodhiretreat.org/termsandconditions.aspx" target="_blank" rel="noopener">Terms &amp; Conditions</a>
          <a href="contact.html">Cancellation &amp; Refunds</a>
          <a href="{BOOK}" target="_blank" rel="noopener">Book a Stay</a>
        </nav>

        <div class="ftr__newscol">
          <div class="news">
            <h4>Subscribe to the Newsletter</h4>
            <p>Stay updated with Sambodhi Retreat news</p>
            <form class="news__row" id="newsletter" novalidate>
              <input type="email" name="email" id="news-email" aria-label="Email address" placeholder="Enter your email address" required>
              <button type="submit">send</button>
            </form>
            <label class="news__consent"><input type="checkbox" id="news-consent" required> I have read and accept the <a href="https://www.sambodhiretreat.org/privacypolicy.aspx" target="_blank" rel="noopener">Privacy Policy</a></label>
            <p class="news__note" role="status" aria-live="polite"></p>
          </div>
        </div>
      </div>

      <div class="ftr__bottom">
        <p>Copyright &copy; <span data-year>2026</span>, Sambodhi Retreat | All Rights Reserved</p>
        <p class="ftr__alt">Also at Jealgora, Govindpur Uttrayan NH-2, Dhanbad, Jharkhand &mdash; 828109</p>
      </div>
    </div>
  </div>
</footer>

<script src="assets/js/images.js"></script>
<script src="assets/js/site.js"></script>
</body>
</html>
"""


# --- shared blocks --------------------------------------------------------
def locale_block(curved=False):
    """curved=True when the preceding section is light, so the boundary stays organic."""
    top = curve('wave','var(--green)','top','curve--mirror') if curved else ''
    return f"""
<section class="section section--tight on-green">
  {top}
  <div class="wrap locale">
    <div data-reveal="up"><p class="locale__place">Resort<br>Bodhgaya<br>Gaya<br>Bihar</p></div>
    <div data-reveal="up">
      <h4>get in touch</h4>
      <p>Sambodhi Retreat</p>
      <p>Hathiyar, Bodhgaya, Gaya, Bihar &mdash; 824231, India</p>
    </div>
    <div data-reveal="up">
      <h4>contact us</h4>
      <ul>
        <li><a href="tel:+917488535210">+91 74885 35210</a></li>
        <li><a href="tel:+917488535208">+91 74885 35208</a></li>
        <li><a href="mailto:info@sambodhiretreat.com">info@sambodhiretreat.com</a></li>
      </ul>
    </div>
    <div data-reveal="up">
      <h4>discover</h4>
      <ul>
        <li><a href="gallery.html">photo gallery</a></li>
        <li><a href="blog.html">stories from sambodhi</a></li>
        <li><a href="dining.html">dining</a></li>
      </ul>
    </div>
  </div>
</section>
"""

def cta_band(img, line1, line2):
    return f"""
<section class="cta-band">
  <div class="cta-band__bg"><img src="{img}" alt="" aria-hidden="true" loading="lazy" decoding="async"></div>
  <div class="cta-band__in">
    <p class="outline" data-reveal="up"><b>{line1}</b><b><em>{line2}</em></b></p>
    <p class="lede" style="color:rgba(255,255,255,.86);margin:1.6rem auto 0;max-width:44ch;" data-reveal="up" data-reveal-delay="110">Rooms from &#8377;3,000 per night. Discover Sambodhi Retreat.</p>
    <div class="btn-row btn-row--center" data-reveal="up" data-reveal-delay="200">
      <a class="btn btn--gold" href="{BOOK}" target="_blank" rel="noopener">book your stay {ARROW}</a>
      <a class="btn btn--light" href="contact.html">make an enquiry</a>
    </div>
  </div>
</section>
"""

# The v8 brief lists "Celebrate Your Special Moments" for removal, but its own
# preserve list says to keep the "Wedding Experience section". They are the same
# section — v7 renamed it. Set this to True and rebuild to remove it.
REMOVE_WEDDING = False

# ======================================================================= DATA
ROOMS = [
 dict(id="green-cave", name="Green Cave Cottages", price="&#8377;7,000", type="cottage",
      guests="4 guests", bed="king", sub="cottage", tab="green cave",
      img=IMG+"rooms-col1/sambodhi-retreat-bodhgaya-green-caves-1.jpg",
      url="https://www.sambodhiretreat.org/sambodhi-retreat-bodhgaya-green-cave-cottages.aspx",
      desc="Facing the swimming pool with the river Falgu on the other side, these grass-clad cottages "
           "give a clear view of the Mahabodhi temple. The design conditions the room to the weather "
           "outside. Four beds mean two couples share the cottage with privacy intact."),
 dict(id="pyramid", name="Pyramid Cottage", price="&#8377;6,500", type="cottage",
      guests="2&ndash;4 guests", bed="king", sub="cottage", tab="pyramid",
      img=IMG+"rooms-col1/sambodhi-retreat-bodhgaya-pyramid-cottages-1.jpg",
      url="https://www.sambodhiretreat.org/sambodhi-retreat-bodhgaya-pyramid-cottage.aspx",
      desc="A pyramid-shaped cluster of rooms panelled in pine milled from waste packaging wood. "
           "Brick corbelled walls, a slant roof and wood rendering inside make these among the most "
           "energy-efficient cottages on the property."),
 dict(id="igloo", name="Igloo House", price="&#8377;4,500", type="cottage",
      guests="2 guests", bed="king", sub="cottage", tab="igloo house",
      img=IMG+"rooms-col1/sambodhi-retreat-bodhgaya-igloo-1.jpg",
      url="https://www.sambodhiretreat.org/sambodhi-retreat-bodhgaya-igloo-house.aspx",
      desc="An igloo-shaped cottage with a private splash pool &mdash; cold water, a cup of tea and warm "
           "snacks. The shell is built so the interior sits up to ten degrees below the outside temperature."),
 dict(id="woodland", name="Woodland Cottage", price="&#8377;4,000", type="cottage",
      guests="2 guests", bed="king", sub="cottage", tab="woodland",
      img=IMG+"rooms-col1/sambodhi-retreat-bodhgaya-woodland-cottages-1.jpg",
      url="https://www.sambodhiretreat.org/sambodhi-retreat-bodhgaya-woodland-cottages.aspx",
      desc="Semi-timber cottages with the look and feel of western living, overlooking a small pond "
           "with ducks on it and surrounded by palms."),
 dict(id="timber", name="Timber Cottage", price="&#8377;4,000", type="cottage",
      guests="2 guests", bed="king", sub="cottage", tab="timber",
      img=IMG+"rooms-col1/sambodhi-retreat-bodhgaya-timber-cottages-1.jpg",
      url="https://www.sambodhiretreat.org/sambodhi-retreat-bodhgaya-timber-cottages.aspx",
      desc="Built on stilts in the Thai style of riverside architecture, clad in split bamboo and "
           "finished with cane brought from the north-east of India."),
 dict(id="lotus", name="Lotus Studios", price="&#8377;3,500&ndash;5,000", type="room",
      guests="2&ndash;4 guests", bed="king", sub="room", tab="lotus studios",
      img=IMG+"rooms-col1/sambodhi-retreat-bodhgaya-lotus-1.jpg", url="",
      desc="Studio-styled rooms with splendid interiors and grand bathrooms, sleeping up to four. "
           "Three of the nine studios double as honeymoon cottages."),
 dict(id="buddha-facing", name="Buddha Facing Rooms", price="On request", type="room",
      guests="enquire", bed="king", sub="room", tab="buddha facing",
      img=IMG+"homePage-Villas/riverside.jpg",
      url="https://www.sambodhiretreat.org/sambodhi-retreat-bodhgaya-buddha-facing.aspx",
      desc="A contemporary building in a modern Indian architectural idiom, drawn from the natural "
           "habitats around it."),
]

ROOM_AMENITIES = ["King-sized bed with blanket","Wardrobe and closet inside the room",
 "TV with a large selection of channels","Work desk and a pair of chairs",
 "Complimentary mineral water","Eco-friendly premium toiletries",
 "Tea and coffee maker with milk, sugar and tea","Bathrobe and bath slippers",
 "24-hour room service","Laundry and dry-cleaning service"]


ICONS = {
 "lotus":  '<path d="M30 40c-10 0-17-6-17-13 6-3 12 0 14 5 0-8 1-15 3-20 2 5 3 12 3 20 2-5 8-8 14-5 0 7-7 13-17 13Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M30 40c-14 0-24-5-24-11 7-3 15-1 19 4M30 40c14 0 24-5 24-11-7-3-15-1-19 4" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>',
 "cloche": '<path d="M8 40a22 22 0 0144 0Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M4 44h52M30 18v-4M30 14a2.5 2.5 0 100-5 2.5 2.5 0 000 5Z" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>',
 "trees":  '<path d="M20 44V30M40 44V34" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M20 32 8 32l12-18 12 18H20Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M40 36 30 36l10-14 10 14H40Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M4 46h52" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>',
 "seated": '<circle cx="30" cy="13" r="5" stroke="currentColor" stroke-width="1.4"/><path d="M30 20c-5 0-8 4-8 9l-9 6c-2 1-1 4 1 4h32c2 0 3-3 1-4l-9-6c0-5-3-9-8-9Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/><path d="M13 45h34" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>',
 "events": '<rect x="8" y="12" width="44" height="36" rx="3" stroke="currentColor" stroke-width="1.4"/><path d="M8 22h44M20 7v9M40 7v9" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M30 41c-4-3-7-5-7-8a3.4 3.4 0 016-2 3.4 3.4 0 016 2c0 3-3 5-5 8Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>',
}


ROOMICONS = {
 "green-cave":  '<path d="M4 26c0-9 5-15 12-15s12 6 12 15" stroke="currentColor" stroke-width="1.1"/><path d="M4 26h24" stroke="currentColor" stroke-width="1.1"/><path d="M9 12c0-3 1-5 2-6M16 9c0-3 0-5 0-6M23 12c0-3-1-5-2-6" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>',
 "pyramid":     '<path d="M16 4L29 26H3L16 4Z" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/><path d="M16 4v22M9.5 15h13" stroke="currentColor" stroke-width="1.1"/>',
 "igloo":       '<path d="M3 26a13 13 0 0126 0Z" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/><path d="M12 26v-6a4 4 0 018 0v6M4.5 18h23M9 12.5h14" stroke="currentColor" stroke-width="1.1"/>',
 "woodland":    '<path d="M16 27v-8" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/><path d="M16 20c-6 0-9-4-9-9 5-1 9 2 9 9Zm0-3c6 0 9-4 9-9-5-1-9 2-9 9Z" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>',
 "timber":      '<path d="M6 14L16 6l10 8" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/><path d="M8.5 14v6h15v-6" stroke="currentColor" stroke-width="1.1"/><path d="M10 20v7M22 20v7M16 20v7" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>',
 "lotus":       '<path d="M16 25c-7 0-12-4-12-9 4-2 8 0 9 3 0-5 1-9 3-12 2 3 3 7 3 12 1-3 5-5 9-3 0 5-5 9-12 9Z" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>',
 "buddha-facing":'<path d="M16 3l7 7H9l7-7Z" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/><path d="M11 10v16M21 10v16M6 26h20M14 26v-6a2 2 0 014 0v6" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>',
}

AMENITIES = [
 ("lotus","Wellness &amp; Water","Rejuvenate by the swimming pool, with splash pools at the igloo cottages"),
 ("cloche","Gourmet Dining","A culinary journey inspired by organic produce and a decade in the kitchen"),
 ("trees","Nature &amp; Trails","Explore village trails and planned excursions into the country around Hathiyar"),
 ("seated","Spiritual Experiences","Bodhgaya, and a clear view of the Mahabodhi temple from the green caves"),
 ("events","Events &amp; Celebrations","Perfect destination for weddings, receptions and conferences"),
]

EVENT_TYPES = [
 ("Weddings","gallery/3.jpg","Two people taking vows, with the convention centre or the lawns behind them."),
 ("Catered dinners","gallery/20.jpg","Menus built with the chef, down to the dish you had in mind."),
 ("Receptions","gallery/7.jpg","A grand reception area and a ballroom sized for the whole guest list."),
 ("Business conferences","promotions/5.jpg","A fully soundproof, fully air-conditioned hall for 100 to 400."),
 ("Birthdays","gallery/14.jpg","Family gatherings on the grounds, planned to the smallest detail."),
 ("City attraction tours","gallery/17.jpg","Planned excursions out into Bodhgaya and the country around it."),
]

POSTS = [
 ("Top 7 organic foods to relish in luxury resorts in Bodhgaya this spring","Spring is a season for revival and for eating well. Seven organic dishes worth ordering while you are here.","Gallery/Top-7-Organic-Foods-in-Sambodhi-Retreat.jpg","https://www.sambodhiretreat.org/Top-7-Organic-Foods-in-Sambodhi-Retreat.aspx"),
 ("Top 5 places to visit this spring in Bodh Gaya","The city where Gautama Buddha attained enlightenment draws millions each year. Five places to start with.","Gallery/Top-5-Places-in-Bodh-Gaya.jpg","https://www.sambodhiretreat.org/Top-5-Places-to-Visit-this-Spring-in-Bodh-Gaya.aspx"),
 ("5 reasons to celebrate Holi with family at a top hotel in Bodhgaya","Traditional festivity and modern amenities, and why the two together make for a good family gathering.","Gallery/blog-4sam.jpg","https://www.sambodhiretreat.org/Hotels-in-Bodhgaya-Bihar-Bodh-gayasambodhi-resort.aspx"),
 ("Top 3 family events organised in the best luxury family hotels in Bodhgaya","A pilgrimage city that has also become a place families come to celebrate. Three events it does well.","Gallery/Top-Family-Events-Organized-in-the-Best-Luxury-Family-Hotels-in-Bodhgaya-Bihar.PNG","https://www.sambodhiretreat.org/Top-3-Family-Events-Organized-in-the-Best-Luxury-Family-Hotels-in-Bodhgaya-Bihar.aspx"),
 ("What kind of activities can guests enjoy in top luxury resorts in Bodh Gaya?","Beyond the history and the temples, what there actually is to do between check-in and check-out.","Gallery/What-Kind-of-Activities-Can-Guests-Enjoy-in-Top-Luxury-Resorts-in-Bodh-Gaya-Bihar.PNG","https://www.sambodhiretreat.org/What-Kind-of-Activities-Can-Guests-Enjoy-in-Top-Luxury-Resorts-in-Bodh-Gaya-Bihar.aspx"),
 ("One-night stay in a luxury hotel in Bodh Gaya: 5 amenities couples can enjoy","Five things worth knowing about before booking a single night for two.","Gallery/One-Night-Stay-in-A-Luxury-Hotel-in-Bodh-Gaya-Bihar.PNG","https://www.sambodhiretreat.org/One-Night-Stay-in-A-Luxury-Hotel-in-Bodh-Gaya-Bihar-5-Useful-Amenities-Couples-Can-Enjoy.aspx"),
 ("What kind of rooms are available for a one-night stay for couples near Bodhgaya?","The room types on offer around Bodhgaya, and which suit a short romantic stay.","Gallery/blog1-19-feb.jpg","https://www.sambodhiretreat.org/What-Kind-Of-Rooms-Are-Available-for-One-Night-Stay-for-Couples-Near-Bodhgaya-Bihar.aspx"),
 ("Top facilities to look for in the best luxury resort for a wedding anniversary in Bihar","An anniversary calls for a venue that raises the occasion rather than just hosting it.","Gallery/blog3-19-feb.jpg","https://www.sambodhiretreat.org/Top-Facilities-to-avail-in-the-Best-Luxury-Resort-for-Wedding-Anniversary-in-Bihar.aspx"),
 ("What to expect at the top luxury hotels for couples in Bodhgaya","Where you stay shapes a romantic trip more than anything else on the itinerary.","Gallery/blog4-19feb.jpg","https://www.sambodhiretreat.org/What-Can-You-Expect-At-The-Top-Luxury-Hotels-For-Couples-In-Bodhgaya-Bihar.aspx"),
 ("Top destinations to explore during luxury romantic trips near Bodhgaya","From ancient caves to the grandeur of a palace, the places worth the drive.","Gallery/blog2-19-feb.jpg","https://www.sambodhiretreat.org/Top-Destinations-You-Can-Explore-during-Luxury-Romantic-Trips-near-Bodhgaya-Bihar.aspx"),
 ("Unveiling gastronomic delights: the best cuisines at luxury hotels near Bodhgaya","Spiritual association and serene landscape draw the crowds. The food is why some of them stay.","Gallery/Unveiling.jpg","https://www.sambodhiretreat.org/Unveiling-Gastronomic-Delights.aspx"),
 ("Discover unparalleled luxury: the best hotels for an anniversary near Bodhgaya","Marking a milestone calls for a venue that matches the weight of the occasion.","Gallery/unspral.jpg","https://www.sambodhiretreat.org/Discover-Unparalleled-Luxury.aspx"),
 ("Recreational and relaxation activities to enjoy in a luxury resort in Bodhgaya","What there is to do between the pool, the grounds and the excursions.","Gallery/blog-3sam.jpg","https://www.sambodhiretreat.org/Recreational-and-Relaxation-Activities.aspx"),
 ("How luxury resorts in Bodhgaya make your stay more comfortable","Past the rooms and the restaurant, the smaller facilities that decide how a stay feels.","Gallery/blog-4sam.jpg","https://www.sambodhiretreat.org/How-Luxury-Resorts-in-Bodhgaya.aspx"),
]

# ==================================================================== PARTIALS
def room_card(r, reveal):
    detail = f'<a href="{r["url"]}" target="_blank" rel="noopener">full details</a>' if r["url"] else ""
    return f"""
      <article class="rcard" id="{r['id']}" data-type="{r['type']}" data-reveal="{reveal}">
        <div class="rcard__media">
          <img src="{r['img']}" alt="{r['name']} at Sambodhi Retreat" loading="lazy" decoding="async">
          <span class="rcard__veil"></span>
          <div class="rcard__over">
            <h3 class="rcard__name">{r['name']}</h3>
            <ul class="rcard__specs"><li>{r['guests']}</li><li>{r['bed']}</li></ul>
          </div>
        </div>
        <div class="rcard__body">
          <p class="rcard__desc">{r['desc']}</p>
          <div class="rcard__foot">
            <p class="rcard__price"><b>{r['price']}</b><span>from / night</span></p>
            <div class="rcard__links">{detail}<a href="{BOOK}" target="_blank" rel="noopener">book now</a></div>
          </div>
        </div>
      </article>"""

def carousel(dark=True):
    tabs = "".join(
      f'<button class="carousel__tab" role="tab" aria-selected="{"true" if i==0 else "false"}">'
      f'<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">{ROOMICONS[r["id"]]}</svg>'
      f'<b>{r["tab"]}</b></button>' for i,r in enumerate(ROOMS))
    dots = "".join(f'<button aria-current="{"true" if i==0 else "false"}" '
                   f'aria-label="Go to accommodation {i+1}"></button>' for i in range(len(ROOMS)))
    btn = "btn--light" if dark else "btn--ghost"
    slides = "".join(f"""
          <article class="slide"><div class="slide__grid">
            <div class="slide__media"><img src="{r['img']}" alt="{r['name']}" loading="lazy" decoding="async"></div>
            <div>
              <p class="slide__sub">{r['sub']}</p>
              <h3 class="slide__name">{r['name']}</h3>
              <p class="slide__text lede">{r['desc']}</p>
              <ul class="slide__specs"><li><b>{r['price']}</b> from / night</li><li>{r['guests']}</li><li>{r['bed']}</li></ul>
              <div class="slide__links">
                <a class="tlink" href="accommodations.html#{r['id']}">full details {ARROW_S}</a>
                <a class="btn {btn}" href="{BOOK}" target="_blank" rel="noopener">book now</a>
              </div>
            </div>
          </div></article>""" for r in ROOMS)
    return f"""
    <div class="carousel" data-reveal="fade">
      <div class="carousel__rail" role="tablist" aria-label="Accommodation types">{tabs}</div>
      <div class="carousel__viewport"><div class="carousel__track">{slides}
        </div></div>
      <div class="carousel__arrows">
        <button class="carousel__nav carousel__prev" aria-label="Previous accommodation">
          <svg width="15" height="11" viewBox="0 0 16 12" fill="none" aria-hidden="true"><path d="M6 1L1 6l5 5M1 6h15" stroke="currentColor" stroke-width="1.3"/></svg>
        </button>
        <button class="carousel__nav carousel__next" aria-label="Next accommodation">
          <svg width="15" height="11" viewBox="0 0 16 12" fill="none" aria-hidden="true"><path d="M10 1l5 5-5 5M15 6H0" stroke="currentColor" stroke-width="1.3"/></svg>
        </button>
      </div>
      <div class="carousel__dots">{dots}</div>
    </div>"""

# Retired at v6: the five-card grid became the bordered rail inside
# amenities_stage(). Kept because accommodations/event pages may want it back.
def amenity_grid():
    items = "".join(f"""
        <article class="amen__item" data-reveal="up">
          <span class="amen__ring"><svg viewBox="0 0 60 52" fill="none" aria-hidden="true">{ICONS[k]}</svg></span>
          <h3>{label}</h3>
          <p>{desc}</p>
        </article>""" for k,label,desc in AMENITIES)
    return f'<div class="amen" data-stagger="90">{items}\n      </div>'

# ================================================== DISCOVER OUR AMENITIES
# A cinematic, self-driving amenity slider. The photograph is the section; the
# navigation is a rail of tall bordered cells ruled straight over it, so the
# borders read as part of the composition rather than as a row of cards.
#
# Data shape, one tuple per slide — panel and slide are 1:1, so the rail IS the
# slider state. Nothing here is invented: every line is drawn from copy already
# published on the site.
#   (key, rail label, rail sub-line, slide title, slide copy, image, href)
AMENX_ICONS = {
 "water": ('<path d="M16 4.4c4.4 5.4 6.7 9.2 6.7 12.4a6.7 6.7 0 1 1-13.4 0c0-3.2 2.3-7 6.7-12.4Z" '
           'stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>'
           '<path d="M3 26.6c2.6 0 2.6-2.1 5.2-2.1s2.6 2.1 5.2 2.1 2.6-2.1 5.2-2.1 2.6 2.1 5.2 2.1 2.6-2.1 5.2-2.1" '
           'stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>'),
 "bed":   ('<path d="M4.4 26.5V11.5M27.6 26.5v-7.8" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>'
           '<path d="M4.4 18.7h23.2v6.1H4.4Z" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>'
           '<path d="M8.6 18.7v-2.5a1.7 1.7 0 0 1 1.7-1.7h4.4a1.7 1.7 0 0 1 1.7 1.7v2.5" '
           'stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>'),
 "trees": ('<path d="M11 27.4v-5.2M21.6 27.4v-4.2" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>'
           '<path d="M11 22.2H4.6L11 11.1l6.4 11.1H11Z" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>'
           '<path d="M21.6 23.2h-6.1l6.1-8.8 6.1 8.8h-6.1Z" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>'
           '<path d="M2.6 28.6h26.8" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>'),
 "dine":  ('<path d="M5 24.1a11 11 0 0 1 22 0Z" stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>'
           '<path d="M2.6 27h26.8M16 13.1v-2.3" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>'
           '<path d="M16 10.8a1.6 1.6 0 1 0 0-3.2 1.6 1.6 0 0 0 0 3.2Z" stroke="currentColor" stroke-width="1.1"/>'),
 "event": ('<rect x="4.2" y="7.4" width="23.6" height="20.2" rx="2.2" stroke="currentColor" stroke-width="1.1"/>'
           '<path d="M4.2 13.4h23.6M10.6 4.4v5.2M21.4 4.4v5.2" stroke="currentColor" stroke-width="1.1" stroke-linecap="round"/>'
           '<path d="M16 24.2c-2.5-1.9-4.3-3.1-4.3-4.9a2.1 2.1 0 0 1 3.7-1.3 2.1 2.1 0 0 1 3.7 1.3c0 1.8-1.8 3-3.1 4.9Z" '
           'stroke="currentColor" stroke-width="1.1" stroke-linejoin="round"/>'),
}

AMENX = [
 ("water", "Wellness", "pool &amp; splash pools",
  "Wellness &amp; Water",
  "A swimming pool on one side of the grounds and the river Falgu on the other, with private splash pools at the igloo cottages &mdash; cold water, a cup of tea and warm snacks brought out to you.",
  "Homepage_Resort_INDEX/top-slider-img11.jpg", "accommodations.html"),

 ("bed", "Accommodation", "sixty rooms, seven forms",
  "Luxury Accommodation",
  "Grass-clad caves, igloos, timber cottages raised on stilts and a pyramid of reclaimed pine. Sixty rooms in all &mdash; twelve large suites and four family rooms, each built to hold its own temperature.",
  "rooms-col1/sambodhi-retreat-bodhgaya-green-caves-1.jpg", "accommodations.html"),

 ("trees", "Nature", "village trails &amp; excursions",
  "Nature &amp; Trails",
  "Village trails run out from the grounds into the country around Hathiyar, with planned excursions further afield. Racquetball, tennis, cricket and volleyball are all on the property.",
  "gallery/9.jpg", "event-venue.html"),

 ("dine", "Dining", "organic produce, one kitchen",
  "Fine Dining",
  "More than ten years of food and beverage experience sit behind this kitchen, in a room that stays professional without tipping into formality. Organic produce runs through the whole menu.",
  "dining/restaurant1.jpg", "dining.html"),

 ("event", "Experiences", "weddings &amp; celebrations",
  "Events &amp; Celebrations",
  "Fifty thousand square feet under a ceiling above fifty feet, seating up to 5,000 guests, with a fully soundproof conference hall for 100 to 400 alongside it.",
  "promotions/1.jpg", "event-venue.html"),
]

# The rail's small "discover" chevron. Deliberately lighter than ARROW_S — it
# marks the cell, it does not compete with the caption's link.
AMENX_TICK = ('<svg viewBox="0 0 22 8" fill="none" aria-hidden="true">'
              '<path d="M0 4h19M15.6 1 19 4l-3.4 3" stroke="currentColor" '
              'stroke-width="1" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def amenx_slides():
    """One background layer per amenity. Layer 0 eager, the rest lazy."""
    out = []
    for i, (k, lab, sub, title, copy, img, href) in enumerate(AMENX):
        act = " is-active" if i == 0 else ""
        eager = "eager" if i == 0 else "lazy"
        out.append(
          f'        <div class="amenx__slide{act}" data-i="{i}">'
          f'<img src="{IMG}{img}" alt="{title} at Sambodhi Retreat" '
          f'loading="{eager}" decoding="async"></div>')
    return "\n".join(out)


def amenx_caps():
    """Captions stack in one grid cell, so the block is as tall as the longest."""
    out = []
    for i, (k, lab, sub, title, copy, img, href) in enumerate(AMENX):
        act = " is-active" if i == 0 else ""
        out.append(f"""        <div class="amenx__cap{act}" data-i="{i}" role="tabpanel"
             id="amenx-panel-{i}" aria-labelledby="amenx-tab-{i}">
          <p class="amenx__num"><b>{i+1:02d}</b><i></i><span>{len(AMENX):02d}</span></p>
          <h3 class="amenx__title">{title}</h3>
          <p class="amenx__text">{copy}</p>
          <a class="alink amenx__go" href="{href}">discover {ARROW_L}</a>
        </div>""")
    return "\n".join(out)


def amenx_cells():
    """The rail. Each cell is the slider control for its own slide."""
    out = []
    for i, (k, lab, sub, title, copy, img, href) in enumerate(AMENX):
        act = " is-active" if i == 0 else ""
        out.append(f"""        <button class="amenx__cell{act}" type="button" role="tab"
                id="amenx-tab-{i}" aria-controls="amenx-panel-{i}"
                aria-selected="{'true' if i==0 else 'false'}" tabindex="{0 if i==0 else -1}" data-i="{i}">
          <span class="amenx__prog" aria-hidden="true"></span>
          <span class="amenx__ico" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none">{AMENX_ICONS[k]}</svg></span>
          <span class="amenx__cellbody">
            <b class="amenx__name">{lab}</b>
            <span class="amenx__sub">{sub}</span>
          </span>
          <span class="amenx__tick" aria-hidden="true">{AMENX_TICK}</span>
        </button>""")
    return "\n".join(out)


def amenities_stage():
    """Discover Our Amenities — intro on cream, then the cinematic stage.

    The stage is a direct child of the section rather than of .wrap, so the
    photograph runs the full width of the viewport while the introduction above
    it keeps the editorial measure.
    """
    return f"""
<!-- Discover Our Amenities. Two halves: a calm cream introduction, then a
     full-bleed photographic stage whose rail of bordered cells IS the slider
     navigation — panel N drives slide N, both ways. The organic wave at the
     top of the stage is the cream band spilling over the photograph, so the
     boundary between the two halves is a curve, never a rule.
     Styles: site.css section 31. Behaviour: site.js module 18. -->
<section class="section section--flush-bottom on-white amenx" id="amenities">
  {wm('tl')}{wm('tr','sprig')}

  <div class="wrap amenx__intro">
    <p class="label label--center" data-reveal="up">Amenities &amp; Experiences</p>
    <h2 class="dhead center amenx__head" data-reveal="up" data-reveal-delay="80"><b>Discover Luxury</b><b><em>Amenities</em></b></h2>
    <p class="lede amenx__lede" data-reveal="up" data-reveal-delay="150">Five ways to spend a day here &mdash; water, rest, the country around us, the table, and the occasions worth gathering for. Choose one and the view changes with it.</p>
    <p class="amenx__note" data-reveal="up" data-reveal-delay="200">Painting, horse riding and table tennis can be arranged at extra cost.</p>
  </div>

  <div class="amenx__stage" data-amenx data-amenx-interval="6400">
    <div class="amenx__media" aria-hidden="true">
{amenx_slides()}
      <span class="amenx__scrim"></span>
    </div>

    <div class="amenx__wave" aria-hidden="true">
      <svg viewBox="0 0 1440 150" preserveAspectRatio="none"><path d="M0,0 H1440 V44 C1120,146 320,146 0,44 Z"/></svg>
    </div>

    <div class="amenx__body">
      <div class="amenx__caps" data-reveal="fade">
{amenx_caps()}
      </div>

      <div class="amenx__cells" role="tablist" aria-label="Resort amenities">
{amenx_cells()}
      </div>
    </div>
  </div>
</section>
"""


# ==================================================== WEDDING EXPERIENCE
# Asymmetric editorial composition: three photographs and one copy panel in a
# 12-column grid, deliberately unequal so it never reads as a card row. On
# desktop the tall portrait anchors the left, a wide landscape sits top-right,
# the copy panel drops beneath it, and a square tucks into the remaining well.
#   (key, alt, image, grid area class, reveal direction)
WED_SHOTS = [
 ("tall",  "Wedding ceremony on the lawns at Sambodhi Retreat",
  "Gallery/Make-Wedding-Special-at-Sambodhi-Retreat.jpg", "wedg__a", "wed-l"),
 ("wide",  "Reception set for a celebration at Sambodhi Retreat",
  "gallery/7.jpg", "wedg__b", "wed-r"),
 ("square","An intimate celebration dinner at Sambodhi Retreat",
  "Gallery/top-post-img2.jpg", "wedg__d", "wed-l"),
]

WED_POINTS = [
 ("Destination weddings", "the lawns, the convention centre, and sixty rooms for your guests"),
 ("Receptions &amp; sangeet", "a ballroom sized for the whole list, and a soundproof hall alongside"),
 ("Intimate celebrations", "engagements, anniversaries and family gatherings at one long table"),
 ("Planned around you", "menus built with the chef, and a team that handles what nobody planned for"),
]


def wedding_section():
    shots = "".join(f"""
      <figure class="wedg__shot {cls}" data-reveal="{rev}">
        <img src="{IMG}{img}" alt="{alt}" loading="lazy" decoding="async">
      </figure>""" for key, alt, img, cls, rev in WED_SHOTS)

    points = "".join(f"""
          <li><b>{t}</b><span>{d}</span></li>""" for t, d in WED_POINTS)

    return f"""
<!-- Wedding Experience. Three photographs and one copy panel in an asymmetric
     12-column grid — never four equal cards. Each block carries its own reveal
     direction so the composition assembles from both sides as it arrives.
     Styles: site.css section 32. -->
<section class="section on-white wedg" id="weddings">
  {wm('tr','mandala')}{wm('bl','sprig')}
  {curve('arc','var(--ivory)','top')}

  <div class="wrap wedg__intro">
    <p class="label label--center" data-reveal="up">Weddings &amp; Celebrations</p>
    <h2 class="dhead center wedg__head" data-reveal="up" data-reveal-delay="80"><b>Celebrate Your</b><b><em>Special Moments</em></b></h2>
  </div>

  <div class="wrap wedg__grid">{shots}

    <div class="wedg__panel wedg__c" data-reveal="wed-r" data-reveal-delay="120">
      <p class="wedg__eyebrow">destination weddings</p>
      <h3 class="wedg__title">A day the whole estate turns out for</h3>
      <p class="wedg__text">Sixty rooms, open lawns, and fifty thousand square feet under a ceiling above fifty feet &mdash; Sambodhi Retreat can hold a guest list of five thousand or a table of twelve, in the landscape where the Buddha attained enlightenment.</p>
      <ul class="wedg__list">{points}
      </ul>
      <a class="alink" href="event-venue.html">plan your celebration {ARROW_L}</a>
    </div>
  </div>
</section>
"""


# ================================================ STORIES FROM SAMBODHI
# Three featured cards drawn from the resort's own journal. Category, title,
# excerpt, arrow. Categories are assigned here rather than invented per card so
# the same post always files under the same heading across the site.
FEATURED = [
 ("Weddings", 0,
  "How the best luxury resorts in Bodhgaya make wedding events special",
  "Spiritual weight and open landscape both work in favour of a wedding held here. A look at how venue and service come together on the day.",
  "Gallery/Make-Wedding-Special-at-Sambodhi-Retreat.jpg",
  "https://www.sambodhiretreat.org/How-the-Best-Luxury-Resorts-in-Bodhgaya-Make-Wedding-Events-Special.aspx"),
 ("Food", 1,
  "Top 7 organic foods to relish in luxury resorts in Bodhgaya this spring",
  "Spring is a season for revival and for eating well. Seven organic dishes worth ordering while you are here.",
  "Gallery/Top-7-Organic-Foods-in-Sambodhi-Retreat.jpg",
  "https://www.sambodhiretreat.org/Top-7-Organic-Foods-in-Sambodhi-Retreat.aspx"),
 ("Bodhgaya", 2,
  "Top 5 places to visit this spring in Bodh Gaya",
  "The city where Gautama Buddha attained enlightenment draws millions each year. Five places worth starting with.",
  "Gallery/Top-5-Places-in-Bodh-Gaya.jpg",
  "https://www.sambodhiretreat.org/Top-5-Places-to-Visit-this-Spring-in-Bodh-Gaya.aspx"),
]


def blog_section():
    cards = "".join(f"""
      <article class="jrn__card" data-reveal="up">
        <a class="jrn__link" href="{url}" target="_blank" rel="noopener">
          <span class="jrn__media">
            <img src="{IMG}{img}" alt="{title}" loading="lazy" decoding="async">
            <span class="jrn__cat">{cat}</span>
          </span>
          <span class="jrn__body">
            <h3 class="jrn__title">{title}</h3>
            <span class="jrn__excerpt">{excerpt}</span>
            <span class="jrn__more">read more {ARROW_S}</span>
          </span>
        </a>
      </article>""" for cat, i, title, excerpt, img, url in FEATURED)

    return f"""
<!-- Stories from Sambodhi. Three featured posts from the resort's own journal;
     the full run stays on blog.html. Styles: site.css section 33. -->
<section class="section on-white jrn" id="stories">
  {wm('tl','lotus')}
  <div class="wrap">
    <div class="shead shead--center">
      <p class="label label--center" data-reveal="up">journal</p>
      <h2 class="dhead center jrn__head" data-reveal="up" data-reveal-delay="80"><b>Stories From</b><b><em>Sambodhi</em></b></h2>
      <p class="lede shead__lede" data-reveal="up" data-reveal-delay="140">Weddings, food, the city around us, and the things guests ask before they arrive.</p>
    </div>

    <div class="jrn__grid" data-stagger="120">{cards}
    </div>

    <div class="btn-row btn-row--center" style="margin-top:clamp(2rem,4.5vw,3.2rem);">
      <a class="btn btn--ghost" href="blog.html">all stories {ARROW}</a>
    </div>
  </div>
</section>
"""


# ======================================== PICKUP &amp; DROP + GET IN TOUCH
def pickup_contact():
    """One dark band carrying two jobs: transfers on the left with the map,
    the contact card on the right. Replaces the old Getting Here + locale pair,
    and keeps every phone number, address line and route fact from both."""
    return f"""
<!-- Pickup &amp; Drop + Get In Touch. The old 'Getting Here' map block and the
     locale strip merged into one dark band — same routes, same numbers, same
     addresses, one composition. Styles: site.css section 34. -->
<section class="section on-green pdg" id="contact">
  {curve('wave','var(--green)','top','curve--mirror')}
  {wm('r','leafbig')}

  <div class="wrap pdg__grid">
    <div class="pdg__left">
      <p class="label" data-reveal="up">transfers</p>
      <h2 class="dhead" data-reveal="up" data-reveal-delay="60"><b>Pickup And Drop</b><b><em>Service Available</em></b></h2>
      <p class="lede" style="margin-top:1.3rem;max-width:46ch;" data-reveal="up" data-reveal-delay="110">Comfortable pickup and drop can be arranged for guests arriving by train or by air. Tell us your arrival time when you book and a car will be waiting.</p>

      <ul class="pdg__routes" data-reveal="up" data-reveal-delay="160">
        <li>
          <span class="pdg__ico" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none"><rect x="6" y="6" width="20" height="16" rx="3" stroke="currentColor" stroke-width="1.2"/><path d="M6 13h20M10.5 26l2-4M21.5 26l-2-4" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/><circle cx="11" cy="18" r="1.3" fill="currentColor"/><circle cx="21" cy="18" r="1.3" fill="currentColor"/></svg></span>
          <span><b>Gaya Junction</b>about 16.4 km &mdash; roughly 40 minutes via the Gaya&ndash;Bodhgaya Road</span>
        </li>
        <li>
          <span class="pdg__ico" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none"><path d="M16 4c1.1 0 2 1.5 2 3.4v4.2l9 5.2v2.6l-9-2.6v5.1l3 2.3v2l-5-1.4-5 1.4v-2l3-2.3v-5.1l-9 2.6v-2.6l9-5.2V7.4C14 5.5 14.9 4 16 4Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg></span>
          <span><b>Gaya Airport</b>about 15.0 km from the terminal to the gate</span>
        </li>
        <li>
          <span class="pdg__ico" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none"><path d="M16 28s9-8.2 9-14.4A9 9 0 1 0 7 13.6C7 19.8 16 28 16 28Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/><circle cx="16" cy="13.4" r="3.2" stroke="currentColor" stroke-width="1.2"/></svg></span>
          <span><b>Hathiyar, Bodhgaya</b>Gaya, Bihar &mdash; 824231, India</span>
        </li>
      </ul>

      <figure class="pdg__map" data-reveal="scale" data-reveal-delay="120">
        <iframe src="{MAPEMBED}" title="Map showing Sambodhi Retreat, Hathiyar, Bodhgaya" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
      </figure>
    </div>

    <aside class="pdg__card" data-reveal="right" data-reveal-delay="140">
      <p class="label">get in touch</p>
      <h3 class="pdg__name">Sambodhi Retreat</h3>

      <ul class="pdg__contact">
        <li>
          <span class="pdg__ico" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none"><path d="M16 28s9-8.2 9-14.4A9 9 0 1 0 7 13.6C7 19.8 16 28 16 28Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/><circle cx="16" cy="13.4" r="3.2" stroke="currentColor" stroke-width="1.2"/></svg></span>
          <span>Hathiyar, Bodhgaya, Gaya,<br>Bihar &mdash; 824231, India</span>
        </li>
        <li>
          <span class="pdg__ico" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none"><path d="M27 22.3v3.2a2 2 0 0 1-2.3 2A24.6 24.6 0 0 1 4.5 7.3 2 2 0 0 1 6.5 5h3.2a2 2 0 0 1 2 1.7c.14 1 .4 2 .76 2.9a2 2 0 0 1-.45 2.1l-1.35 1.35a19.6 19.6 0 0 0 7.34 7.34l1.35-1.35a2 2 0 0 1 2.1-.45c.94.36 1.92.62 2.9.76a2 2 0 0 1 1.7 2.05Z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg></span>
          <span><a href="tel:+917488535210">+91 74885 35210</a><br><a href="tel:+917488535208">+91 74885 35208</a></span>
        </li>
        <li>
          <span class="pdg__ico" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none"><rect x="4" y="7" width="24" height="18" rx="2.5" stroke="currentColor" stroke-width="1.2"/><path d="m4.8 8.8 11.2 8 11.2-8" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/></svg></span>
          <span><a href="mailto:info@sambodhiretreat.com">info@sambodhiretreat.com</a></span>
        </li>
      </ul>

      <p class="pdg__rate">Rooms from <b>&#8377;3,000</b> per night</p>

      <div class="pdg__cta">
        <a class="btn btn--gold" href="contact.html">make an enquiry {ARROW}</a>
        <a class="btn btn--light" href="{BOOK}" target="_blank" rel="noopener">book a stay</a>
      </div>

      <p class="pdg__alt">Also at Jealgora, Govindpur Uttrayan NH-2, Dhanbad, Jharkhand &mdash; 828109</p>
    </aside>
  </div>
</section>
"""


# ============================================================ PHOTO GALLERY
# Asymmetric masonry. Every tile names its own span so the rhythm is composed
# rather than uniform, and the reveal direction alternates strictly
# left / right / left / right down the list, as the brief asks.
GALLERY_TILES = [
 ("gallery/2.jpg",  "The resort grounds at Sambodhi Retreat",            "tile--w2 tile--h3"),
 ("rooms-col1/sambodhi-retreat-bodhgaya-green-caves-1.jpg", "Green Cave Cottages", "tile--h3"),
 ("Homepage_Resort_INDEX/top-slider-img11.jpg", "The swimming pool",     "tile--h3"),
 ("rooms-col1/sambodhi-retreat-bodhgaya-pyramid-cottages-1.jpg", "Pyramid Cottages", "tile--h2"),
 ("dining/restaurant1.jpg", "The restaurant at Sambodhi Retreat",        "tile--w2 tile--h2"),
 ("rooms-col1/sambodhi-retreat-bodhgaya-igloo-1.jpg", "Igloo Houses",    "tile--h2"),
 ("rooms-col1/sambodhi-retreat-bodhgaya-timber-cottages-1.jpg", "Timber Cottages on stilts", "tile--h3"),
 ("gallery/7.jpg",  "A celebration set up in the reception area",        "tile--w2 tile--h3"),
 ("gallery/9.jpg",  "The quiet grounds and village trails",              "tile--h3"),
 ("Gallery/top-post-img3.jpg", "A wedding at Sambodhi Retreat",          "tile--h2"),
 ("promotions/1.jpg", "The International Convention Centre",             "tile--w2 tile--h2"),
 ("Homepage_Resort_INDEX/learn-img1.jpg", "Buddha and the heritage landscape around Bodhgaya", "tile--h2"),
]


def photo_gallery():
    tiles = "".join(f"""
      <a class="gtile {span}" href="{IMG}{src}" data-lightbox data-reveal="{'gal-l' if i % 2 == 0 else 'gal-r'}"
         aria-label="Open gallery image {i+1}: {alt}">
        <img src="{IMG}{src}" alt="{alt}" loading="lazy" decoding="async">
        <span class="gtile__veil" aria-hidden="true"></span>
        <span class="gtile__zoom" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none"><circle cx="10.5" cy="10.5" r="6.5" stroke="currentColor" stroke-width="1.4"/><path d="M15.4 15.4 21 21M10.5 7.6v5.8M7.6 10.5h5.8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg></span>
      </a>""" for i, (src, alt, span) in enumerate(GALLERY_TILES))

    return f"""
<!-- Photo Gallery. Asymmetric masonry, not an equal grid: each tile declares
     its own column and row span. Reveal direction alternates strictly
     left/right down the source order (site.css section 15 defines gal-l and
     gal-r; the shared IntersectionObserver fires each tile once and unobserves,
     so nothing re-animates on the way back up). Styles: site.css section 35. -->
<section class="section on-white gal" id="gallery">
  {wm('tr','sprig')}
  {curve('arc','var(--white)','top')}
  <div class="wrap">
    <div class="shead shead--center">
      <p class="label label--center" data-reveal="up">gallery</p>
      <h2 class="dhead center gal__head" data-reveal="up" data-reveal-delay="80"><b>Photo</b><b><em>Gallery</em></b></h2>
      <p class="lede shead__lede" data-reveal="up" data-reveal-delay="140">Cottages, the pool, the restaurant, the convention centre and the country around Hathiyar.</p>
    </div>

    <div class="gal__grid">{tiles}
    </div>

    <div class="btn-row btn-row--center" style="margin-top:clamp(2rem,4.5vw,3.2rem);">
      <a class="btn btn--ghost" href="gallery.html">view full gallery {ARROW}</a>
    </div>
  </div>
</section>
"""


# ==================================================================== HOME
def hero_slides():
    """Hero slides for the home page. The first one carries .is-active."""
    return "\n".join(
        f'      <div class="hero__slide{" is-active" if i == 0 else ""}"'
        f' style="background-image:url(\'{src}\')"></div>'
        for i, src in enumerate(HERO_SLIDES))

def home_body():
    return f"""
<!-- Home hero runs in reveal mode: the picture is cut taller than the window,
     so the first screen is photograph only and the curve waits below the fold.
     .hero__frame is the part that lifts as you scroll; the wave is a child of
     the SECTION, not of the pinned window, so it climbs into view by itself as
     the hero runs out. Styles: site.css section 28. --hero-p: site.js. -->
<section class="hero hero--reveal" data-hero-reveal>
  <div class="hero__media">
    <div class="hero__frame">
{hero_slides()}
    </div>
    <div class="hero__scrim"></div>

    <div class="hero__center">
      <h1 class="outline"><b>Sambodhi</b><b>Retreat</b></h1>
      <span class="hero__orn"><svg viewBox="0 0 40 58" fill="none" aria-hidden="true"><path d="M20 54C13 44 4 37 3.5 27 3 17 10 11 15 14c2.2 1.4 3.8 3.6 5 6 1.2-2.4 2.8-4.6 5-6 5-3 12 3 11.5 13-.5 10-9.5 17-16.5 27Z" stroke="currentColor" stroke-width="1.6"/><path d="M20 4v50" stroke="currentColor" stroke-width="1.6"/></svg></span>
      <p class="hero__tag">A sanctuary of peace, luxury and inner awakening</p>
      <a class="hero__map" href="{MAPQ}" target="_blank" rel="noopener">{PIN} map</a>
    </div>

    <span class="hero__scroll" aria-hidden="true"><i></i></span>
  </div>

  <div class="hero__wave" aria-hidden="true"><svg viewBox="0 0 1440 150" preserveAspectRatio="none"><path d="M0,150 H1440 V28 C1230,22 1040,16 760,40 C480,64 300,150 0,150 Z"/></svg></div>
</section>

<!-- Our Story — two alternating editorial compositions. Row 1 reads copy left
     / picture right; row 2 mirrors it. The oversized outlined word in each row
     is decoration on its own layer ABOVE the photograph (site.css 29), so the
     letters run across the top of the picture rather than being cropped. -->
<section class="section on-white estory">
  {wm('tr','sprig')}

  <div class="wrap estory__lead">
    <p class="label label--dot" data-reveal="up">Our Story</p>
  </div>

  <div class="wrap estory__row">
    <span class="estory__word estory__word--right" aria-hidden="true"
          data-reveal="fade" data-reveal-delay="120">
      <span class="outline outline--ink">Sambodhi</span>
    </span>

    <div class="estory__copy" data-reveal="left" data-reveal-delay="60">
      <h2 class="dhead" style="max-width:15ch;"><b>A Place to Pause,</b><b><em>Reconnect &amp; Renew</em></b></h2>
      <p class="lede">Every building here is a different argument about how to stay cool, stay warm, and stay quiet.</p>
      <p class="body-copy">Grass-clad caves, cottages raised on stilts and a pyramid of pine &mdash; arranged between a swimming pool and the river Falgu. The cave cottages temper the room to the weather outside. The igloos hold an interior up to ten degrees below the air around them.</p>
      <p class="body-copy" style="margin-top:1.1rem;">The pyramid cottages are panelled in pine milled from waste packaging timber, with brick corbelled walls and a slant roof that make them energy efficient. Around them: exquisitely designed rooms, organic food, village trails, a swimming pool and a splash pool.</p>
    </div>

    <figure class="estory__media frame frame--plx" data-reveal="clip-u" data-reveal-delay="140">
      <img src="{STORY1}" alt="The grounds and cottages at Sambodhi Retreat, Bodhgaya"
           data-parallax="0.15" loading="lazy" decoding="async">
    </figure>
  </div>

  <div class="wrap estory__row estory__row--rev">
    <span class="estory__word estory__word--left" aria-hidden="true"
          data-reveal="fade" data-reveal-delay="120">
      <span class="outline outline--ink">Awaken</span>
    </span>

    <figure class="estory__media frame frame--plx" data-reveal="clip-u" data-reveal-delay="140">
      <img src="{STORY2}" alt="Green cave cottages facing the Mahabodhi temple, Sambodhi Retreat"
           data-parallax="0.15" loading="lazy" decoding="async">
    </figure>

    <div class="estory__copy" data-reveal="right" data-reveal-delay="60">
      <h2 class="dhead" style="max-width:13ch;"><b>The Slow Part</b><b><em>of the Day</em></b></h2>
      <p class="lede">Bodhgaya is where the Buddha attained enlightenment. The retreat sits in that landscape rather than commenting on it.</p>
      <p class="body-copy">On one side, the swimming pool. On the other, the river Falgu. From the green cave cottages, a clear view of the Mahabodhi temple. Between them: village trails, organic food, and rooms built to hold their own temperature so the air conditioning has less to argue with.</p>
      <p><a class="alink" href="accommodations.html">See the rooms {ARROW_L}</a></p>
    </div>
  </div>
</section>

{amenities_stage()}

<section class="section on-green villas">
  {curve('wave','var(--green)','top')}
  <div class="wrap">
    <h2 class="dhead" data-reveal="left"><b><em>Suites &amp; Villas</em></b></h2>
    <p class="lede" style="margin-top:1.2rem;max-width:52ch;" data-reveal="left" data-reveal-delay="80">Sambodhi Retreat is a boutique hotel of sixty rooms &mdash; twelve of them large suites, four of them family rooms.</p>
    <p style="margin-top:1.4rem;" data-reveal="left" data-reveal-delay="140">
      <a class="alink" href="accommodations.html">View rooms {ARROW_L}</a>
    </p>
  </div>

  <div class="wrap" style="margin-top:clamp(2.6rem,6vw,4.6rem);">
    <article class="villa villa--a">
      <figure class="villa__media" data-villa-in="left">
        <img src="{IMG}rooms-col1/sambodhi-retreat-bodhgaya-green-caves-1.jpg" alt="Green Cave Cottages at Sambodhi Retreat" loading="lazy" decoding="async">
      </figure>
      <div class="villa__copy" data-villa-in="right" data-villa-delay="120">
        <h3 class="villa__name">Green Cave Cottages</h3>
        <p class="villa__text">Grass-clad, facing the swimming pool with the river Falgu behind, and a clear view of the Mahabodhi temple. Four beds give two couples privacy without dropping the luxury.</p>
        <a class="tlink tlink--light" href="accommodations.html#green-cave">full details {ARROW_S}</a>
      </div>
    </article>

    <article class="villa villa--b">
      <div class="villa__copy" data-villa-in="left" data-villa-delay="120">
        <h3 class="villa__name">Pyramid Cottage</h3>
        <p class="villa__text">A pyramid-shaped cluster panelled in pine reclaimed from packaging timber. Brick corbelled walls, a slant roof and wood rendering inside make it an energy-efficient unit.</p>
        <a class="tlink tlink--light" href="accommodations.html#pyramid">full details {ARROW_S}</a>
      </div>
      <figure class="villa__media" data-villa-in="right">
        <img src="{IMG}rooms-col1/sambodhi-retreat-bodhgaya-pyramid-cottages-1.jpg" alt="Pyramid Cottage at Sambodhi Retreat" loading="lazy" decoding="async">
      </figure>
    </article>
  </div>
</section>

<section class="section on-white">
  {curve('arc','var(--white)','top')}
  {wm('tr')}{wm('bl')}
  <div class="wrap">
    <div class="shead">
      <h2 class="dhead" data-reveal="up"><b>Our</b><b><em>Accommodation</em></b></h2>
      <p class="lede shead__lede justify" data-reveal="up" data-reveal-delay="90">Each accommodation type is a different response to the same climate. Starting rates are published by the resort and vary by date, occupancy and season.</p>
      <p style="margin-top:1.2rem;" data-reveal="up" data-reveal-delay="150"><a class="alink" href="accommodations.html">View all {ARROW_L}</a></p>
    </div>
    {carousel(dark=False)}
  </div>
</section>

{wedding_section() if not REMOVE_WEDDING else ''}

{blog_section()}
{pickup_contact()}
{photo_gallery()}
"""

# =============================================================== INNER BODIES
def banner(img, crumb, title_a, title_b, tag):
    return f"""
<section class="hero hero--page">
  <div class="hero__media">
    <div class="hero__slide is-active" style="background-image:url('{img}')"></div>
    <div class="hero__scrim"></div>
    <div class="hero__center">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>{crumb}</nav>
      <h1 class="outline"><b>{title_a}</b><b><em>{title_b}</em></b></h1>
      <p class="hero__tag">{tag}</p>
      <a class="hero__map" href="{MAPQ}" target="_blank" rel="noopener">{PIN} map</a>
    </div>
    <div class="hero__wave" aria-hidden="true"><svg viewBox="0 0 1440 150" preserveAspectRatio="none"><path d="M0,150 H1440 V28 C1230,22 1040,16 760,40 C480,64 300,150 0,150 Z"/></svg></div>
  </div>
</section>"""

def accommodations_body():
    cards = "".join(room_card(r, ["left","up","right"][i%3]) for i,r in enumerate(ROOMS))
    am = "".join(f"<li>{a}</li>" for a in ROOM_AMENITIES)
    return f"""
<section class="section on-white">
  {wm('tr','sprig')}
  <div class="wrap">
    <div class="shead">
      <p class="label" data-reveal="up">rooms &amp; suites</p>
      <h2 class="dhead" data-reveal="up" data-reveal-delay="80"><b>Seven ways to sleep</b><b><em>on one estate</em></b></h2>
      <p class="lede" style="margin-top:1rem;" data-reveal="up" data-reveal-delay="110">Stay surrounded by river, garden and quiet.</p>
      <p class="lede shead__lede justify" data-reveal="up" data-reveal-delay="150">Sambodhi Retreat is a boutique hotel of sixty rooms &mdash; twelve of them large suites, four of them family rooms. Each accommodation type is a different response to the same climate.</p>
    </div>
    <div class="filters" data-filters role="group" aria-label="Filter accommodation">
      <button data-filter="all" aria-pressed="true">all</button>
      <button data-filter="cottage" aria-pressed="false">cottages</button>
      <button data-filter="room" aria-pressed="false">rooms &amp; studios</button>
    </div>
    <div class="rooms">{cards}
    </div>
  </div>
</section>

<section class="section section--flush-top on-white">
  <div class="wrap">
    <figure class="frame frame--pano frame--wave" style="margin:0" data-reveal="scale">
      <img src="{IMG}Homepage_Resort_INDEX/top-slider-img11.jpg" alt="The pool at Sambodhi Retreat" loading="lazy" decoding="async">
      <span class="overtitle overtitle--br overtitle--bleed"><span class="outline"><b>Rooms &amp;</b><b><em>Suites</em></b></span></span>
    </figure>
  </div>
</section>

<section class="section on-green">
  {curve('wave','var(--green)','top')}
  <div class="wrap split">
    <div class="col-5" data-reveal="left">
      <p class="label">in every room</p>
      <h2 class="dhead"><b>The same ten things,</b><b><em>everywhere</em></b></h2>
      <p class="lede" style="margin-top:1.3rem;">Whichever cottage or studio you book, these come as standard.</p>
    </div>
    <div class="col-7" data-reveal="right"><ul class="facts">{am}</ul></div>
  </div>
</section>

<section class="section section--tight on-white">
  {curve('arc','var(--white)','top')}
  {wm('bl')}
  <div class="wrap center">
    <p class="notice measure" style="text-align:left;" data-reveal="up">Rates shown are starting rates published by the resort and vary by date, occupancy and season. Live availability and current pricing are handled on the official reservations system.</p>
    <div class="btn-row btn-row--center" style="margin-top:1.8rem;" data-reveal="up" data-reveal-delay="110">
      <a class="btn" href="{BOOK}" target="_blank" rel="noopener">check availability {ARROW}</a>
      <a class="btn btn--ghost" href="contact.html">ask a question</a>
    </div>
  </div>
</section>"""

def banquet_body():
    return f"""
<section class="section on-white">
  {wm('tr','sprig')}
  <div class="wrap split">
    <div class="col-7 bleed-l" data-reveal="clip-l">
      <figure class="frame frame--plx frame--wide" style="margin:0">
        <img src="{IMG}promotions/1.jpg" alt="International Convention Centre, Sambodhi Retreat" data-parallax="0.26" loading="lazy" decoding="async">
      </figure>
    </div>
    <div class="col-5" data-reveal="right">
      <p class="label">banquet halls &amp; venues</p>
      <h2 class="dhead"><b>International</b><b><em>Convention Centre</em></b></h2>
      <p class="lede" style="margin-top:1.3rem;">A hall sized for a wedding, a family milestone or a corporate year-end &mdash; and for all three on the same weekend.</p>
      <p class="body-copy justify" style="margin-top:1rem;">Fifty thousand square feet under a ceiling that rises past fifty feet, with a grand ballroom and a grand reception area. The resort describes it as the first and only international convention centre in Bodhgaya.</p>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(2rem,4vw,3.2rem);">
    <dl class="specsheet" data-reveal="up">
      <div><dt>area</dt><dd>50,000 sq. ft.</dd></div>
      <div><dt>capacity</dt><dd>Up to 5,000</dd></div>
      <div><dt>ceiling height</dt><dd>Over 50 ft.</dd></div>
      <div><dt>parking</dt><dd>Approx. 800 vehicles</dd></div>
    </dl>
    <ul class="facts" style="margin-top:2rem;" data-reveal="up" data-reveal-delay="100">
      <li>Seating for 2,000, dining for 2,000, standing for 1,000</li>
      <li>Fully air conditioned</li><li>A grand ballroom</li><li>A grand reception area</li>
      <li>Professional and friendly service staff</li><li>Rates vary &mdash; enquire for a quotation</li>
    </ul>
  </div>
</section>

<section class="section on-sage">
  {curve('arc','var(--sage)','top')}
  {wm('tr','mandala')}
  <div class="wrap split">
    <div class="col-7 bleed-r m-order-first" data-reveal="clip-r">
      <figure class="frame frame--plx frame--wide" style="margin:0">
        <img src="{IMG}promotions/5.jpg" alt="Conference hall at Sambodhi Retreat" data-parallax="0.26" loading="lazy" decoding="async">
      </figure>
    </div>
    <div class="col-5" style="order:-1;" data-reveal="left">
      <p class="label">the smaller room</p>
      <h2 class="dhead"><b>Conference</b><b><em>Hall</em></b></h2>
      <p class="lede justify" style="margin-top:1.3rem;">Fully soundproof and fully air conditioned &mdash; a versatile space for a hundred people or four hundred. Three and a half thousand square feet of built-up space under a roof more than twenty feet high, in a convenient location on the estate.</p>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(2rem,4vw,3.2rem);">
    <dl class="specsheet" data-reveal="up">
      <div><dt>area</dt><dd>3,500 sq. ft.</dd></div>
      <div><dt>capacity</dt><dd>100&ndash;400 guests</dd></div>
      <div><dt>roof height</dt><dd>Over 20 ft.</dd></div>
      <div><dt>acoustics</dt><dd>Fully soundproof</dd></div>
    </dl>
  </div>
</section>

<section class="section on-white">
  {curve('arc','var(--white)','top')}
  <div class="wrap duo">
    <figure class="frame frame--plx frame--wide" style="margin:0" data-reveal="clip-u">
      <img src="{IMG}promotions/2.jpg" alt="Convention centre interior" data-parallax="0.2" loading="lazy" decoding="async"></figure>
    <figure class="frame frame--plx frame--wide" style="margin:0" data-reveal="clip-d">
      <img src="{IMG}promotions/6.jpg" alt="Conference hall interior" data-parallax="0.2" loading="lazy" decoding="async"></figure>
  </div>
  <div class="wrap center" style="margin-top:clamp(2.2rem,5vw,3.6rem);">
    <h2 class="dhead center" style="margin-inline:auto;max-width:18ch;" data-reveal="up"><b>Rates vary by date</b><b><em>and by scale</em></b></h2>
    <p class="lede measure" style="margin-top:1.2rem;" data-reveal="up" data-reveal-delay="100">Tell us the date, the headcount and the shape of the day, and the events team will come back with a quotation.</p>
    <div class="btn-row btn-row--center" data-reveal="up" data-reveal-delay="180">
      <a class="btn" href="contact.html">enquire now {ARROW}</a>
      <a class="btn btn--ghost" href="event-venue.html">see the event venue</a>
    </div>
  </div>
</section>"""

def event_body():
    panels = "".join(f"""
      <article class="tblock" data-reveal="up">
        <div class="tblock__media"><img src="{IMG}{i}" alt="{n}" loading="lazy" decoding="async"></div>
        <h3 class="tblock__title">{n}</h3><p class="tblock__text body-copy">{d}</p>
      </article>""" for n,i,d in EVENT_TYPES)
    return f"""
<section class="section on-white">
  {wm('tr','sprig')}
  <div class="wrap">
    <div class="shead">
      <p class="label" data-reveal="up">events</p>
      <h2 class="dhead" data-reveal="up" data-reveal-delay="80"><b>The perfect place to escape</b><b><em>&mdash; and to gather</em></b></h2>
      <p class="lede shead__lede justify" data-reveal="up" data-reveal-delay="150">An event, a business meet, a family get-together, a sales review or a product launch: a dedicated team here handles it down to the minutest detail &mdash; a particular dish, a particular wardrobe, a particular brand of paper napkin.</p>
    </div>
    <div class="threeup" data-stagger="90">{panels}
    </div>
  </div>
</section>

<section class="section on-green">
  {curve('wave','var(--green)','top')}
  <div class="wrap split">
    <div class="col-6 bleed-l" data-reveal="clip-l">
      <figure class="frame frame--plx frame--portrait" style="margin:0">
        <img src="{IMG}Gallery/main-blog-img9.jpg" alt="Candle-light dinner setting" data-parallax="0.28" loading="lazy" decoding="async">
      </figure>
    </div>
    <div class="col-6" data-reveal="right">
      <p class="label">an evening</p>
      <h2 class="dhead"><b>Candle-light</b><b><em>dinner</em></b></h2>
      <p class="lede" style="margin-top:1.3rem;">Among the better ways to spend real time with someone. A heart full of love shows affection one way or another, and time spent together is the simplest of them. The resort sets the table for it.</p>
    </div>
  </div>
</section>

<section class="section on-sage">
  {curve('arc','var(--sage)','top')}
  {wm('tr','mandala')}
  <div class="wrap split">
    <div class="col-6 bleed-r m-order-first" data-reveal="clip-r">
      <figure class="frame frame--plx frame--portrait" style="margin:0">
        <img src="{IMG}Gallery/main-blog-img1.jpg" alt="Floating breakfast in a private pool" data-parallax="0.28" loading="lazy" decoding="async">
      </figure>
    </div>
    <div class="col-6" style="order:-1;" data-reveal="left">
      <p class="label">a morning</p>
      <h2 class="dhead"><b>Floating</b><b><em>breakfast</em></b></h2>
      <p class="lede" style="margin-top:1.3rem;">Fruit, coffee, toast or a non-alcoholic cocktail, arranged on a tray and floated in the private pool. Delicious and, as the last few years have proved, entirely photogenic.</p>
    </div>
  </div>
</section>

<section class="section on-white">
  {curve('arc','var(--white)','top')}
  {wm('bl')}
  <div class="wrap split">
    <div class="col-6" data-reveal="up">
      <p class="label">ambience</p>
      <h2 class="dhead"><b>The venue sets the mood</b><b><em>before anyone speaks</em></b></h2>
      <p class="lede justify" style="margin-top:1.3rem;">A simple garden party, a birthday or anniversary get-together, or a lavish wedding reception: attention to detail and the ability to cater for the unexpected are what leave guests with the day they hoped for.</p>
      <div class="btn-row"><a class="btn" href="contact.html">plan an event {ARROW}</a></div>
    </div>
    <div class="col-6 bleed-r" data-reveal="clip-r">
      <figure class="frame frame--plx frame--wide" style="margin:0">
        <img src="{IMG}Gallery/main-blog-img2.jpg" alt="Event setting at Sambodhi Retreat" data-parallax="0.24" loading="lazy" decoding="async">
      </figure>
    </div>
  </div>
  <div class="wrap split" style="margin-top:clamp(2.4rem,5vw,4rem);">
    <div class="col-5" data-reveal="left">
      <p class="label">alongside</p>
      <h2 class="dhead"><b>Activities</b><b><em>on the estate</em></b></h2>
    </div>
    <div class="col-7" data-reveal="right">
      <ul class="facts">
        <li>Swimming</li><li>Racquetball</li><li>Tennis</li><li>Cricket</li>
        <li>Volleyball</li><li>Planned excursions</li><li>Rain dance with DJ</li>
        <li>Painting, horse riding and table tennis at extra cost</li>
      </ul>
    </div>
  </div>
</section>"""

def dining_body():
    return f"""
<section class="section on-white">
  {wm('tr','sprig')}
  <div class="wrap split">
    <div class="col-6 bleed-l" data-reveal="clip-l">
      <figure class="frame frame--plx frame--portrait" style="margin:0">
        <img src="{IMG}dining/restaurant1.jpg" alt="The restaurant at Sambodhi Retreat" data-parallax="0.3" loading="lazy" decoding="async">
      </figure>
    </div>
    <div class="col-6" data-reveal="right">
      <p class="label">the restaurant</p>
      <h2 class="dhead"><b>The freshest ingredients,</b><b><em>expertly prepared</em></b></h2>
      <p class="lede" style="margin-top:1rem;">An experience for the senses.</p>
      <p class="lede justify" style="margin-top:1.3rem;">More than ten years of food and beverage experience sit behind this kitchen, in a room that stays professional without ever tipping into formality.</p>
      <p class="body-copy justify" style="margin-top:1rem;">The chef and his team built a menu unlike any other on the property. Eating here runs as a sequence of carefully executed dishes rather than a list of options &mdash; curiosity, discovery and a little adventure, in that order.</p>
    </div>
  </div>
</section>

<section class="section section--flush-top on-white">
  <div class="wrap duo" data-stagger="120">
    <figure class="frame frame--plx frame--wide" style="margin:0" data-reveal="clip-r">
      <img src="{IMG}dining/restaurant2.jpg" alt="Dining room at the resort" data-parallax="0.22" loading="lazy" decoding="async"></figure>
    <figure class="frame frame--plx frame--wide" style="margin:0" data-reveal="clip-l">
      <img src="{IMG}dining/restaurant3.jpg" alt="Table setting at the restaurant" data-parallax="0.22" loading="lazy" decoding="async"></figure>
  </div>
</section>

<section class="section on-green">
  {curve('wave','var(--green)','top')}
  <div class="wrap split">
    <div class="col-6" data-reveal="up">
      <p class="label">fine dining choices</p>
      <h2 class="dhead"><b>Nothing warmer than</b><b><em>a long family dinner</em></b></h2>
      <p class="lede justify" style="margin-top:1.3rem;">A wide range of dishes, cooked well and served in a room worth sitting in. Organic produce runs through the menu, as it does through the rest of the estate.</p>
      <div class="notice" style="margin-top:1.7rem;">Sample menus are marked as coming soon by the resort. The live menu is published separately and is the authoritative list of dishes and prices.</div>
      <div class="btn-row"><a class="btn btn--light" href="https://sambodhi-retreat-men-n1bw.glide.page/" target="_blank" rel="noopener">view the live menu {ARROW}</a></div>
    </div>
    <div class="col-6 bleed-r" data-reveal="clip-d">
      <figure class="frame frame--plx frame--tall" style="margin:0">
        <img src="{IMG}Homepage_Resort_INDEX/home-gal-img6.jpg" alt="Dining at Sambodhi Retreat" data-parallax="0.28" loading="lazy" decoding="async">
      </figure>
    </div>
  </div>
</section>

<section class="section section--tight on-white">
  {curve('arc','var(--white)','top')}
  <div class="wrap">
    <figure class="frame frame--pano frame--wave-top" style="margin:0" data-reveal="scale">
      <img src="{IMG}gallery/20.jpg" alt="The dining terrace" loading="lazy" decoding="async">
      <span class="overtitle overtitle--bl overtitle--bleed"><span class="outline"><b>Dining</b></span></span>
    </figure>
  </div>
</section>"""

def gallery_body():
    return f"""
<section class="section on-white">
  {wm('tr','sprig')}{wm('bl')}
  <div class="wrap">
    <div class="shead shead--center">
      <p class="label label--center" data-reveal="up">gallery</p>
      <h2 class="dhead center" style="margin-inline:auto;" data-reveal="up" data-reveal-delay="80"><b>Twenty-seven</b><b><em>frames</em></b></h2>
      <p class="lede shead__lede" data-reveal="up" data-reveal-delay="150">Cottages, restaurant, reception and the natural attractions next door. Select any image to open it full size.</p>
    </div>
    <div class="masonry" id="galleryGrid"></div>
    <noscript><p class="notice" style="margin-top:2rem;">The gallery viewer needs JavaScript. The full set of photographs is also published on the official Sambodhi Retreat gallery page.</p></noscript>
  </div>
</section>

<section class="section section--tight on-green">
  {curve('wave','var(--green)','top')}
  <div class="wrap center">
    <h2 class="dhead center" style="margin-inline:auto;max-width:16ch;" data-reveal="up"><b>Seen enough to</b><b><em>want a room?</em></b></h2>
    <div class="btn-row btn-row--center" data-reveal="up" data-reveal-delay="110">
      <a class="btn btn--light" href="accommodations.html">browse accommodation {ARROW}</a>
      <a class="btn btn--gold" href="{BOOK}" target="_blank" rel="noopener">book now</a>
    </div>
  </div>
</section>"""

def blog_body():
    cards = "".join(f"""
      <a class="jcard" href="{u}" target="_blank" rel="noopener" data-reveal="up">
        <div class="jcard__media"><img src="{IMG}{i}" alt="{t}" loading="lazy" decoding="async"></div>
        <h3 class="jcard__title">{t}</h3><p class="jcard__excerpt">{e}</p>
      </a>""" for t,e,i,u in POSTS)
    return f"""
<section class="section on-white">
  {wm('tr','sprig')}
  <div class="wrap">
    <article class="jfeature" style="margin-bottom:clamp(2.6rem,6vw,4.6rem);">
      <div data-reveal="clip-l">
        <figure class="frame frame--plx frame--wide" style="margin:0">
          <img src="{IMG}Gallery/Make-Wedding-Special-at-Sambodhi-Retreat.jpg" alt="Weddings at Sambodhi Retreat" data-parallax="0.22" loading="lazy" decoding="async">
        </figure>
      </div>
      <div data-reveal="right">
        <p class="meta" style="margin-bottom:.9rem;">featured</p>
        <h2 class="dhead" style="font-size:clamp(1.6rem,5.6vw,2.4rem);margin-bottom:1.1rem;">How the best luxury resorts in Bodhgaya make wedding events special</h2>
        <p class="body-copy justify">Bodhgaya is known for its spiritual weight and its landscape, and both work in favour of a wedding held here. A look at how venues and service in the city come together for the day.</p>
        <p style="margin-top:1.5rem;"><a class="alink" href="https://www.sambodhiretreat.org/How-the-Best-Luxury-Resorts-in-Bodhgaya-Make-Wedding-Events-Special.aspx" target="_blank" rel="noopener">Read more {ARROW_L}</a></p>
      </div>
    </article>
    <hr class="rule" style="margin-bottom:clamp(2.4rem,5vw,3.6rem);">
    <div class="jgrid" data-stagger="90">{cards}
    </div>
    <p class="form-note center" style="margin-top:clamp(2.2rem,5vw,3.4rem);">Articles open on the official Sambodhi Retreat blog.</p>
  </div>
</section>"""

def contact_body():
    return f"""
<section class="section on-white">
  {wm('tr','sprig')}
  <div class="wrap contact-grid">
    <div data-reveal="left">
      <p class="label">direct enquiries</p>
      <h2 class="dhead"><b>Tell us</b><b><em>what you need</em></b></h2>
      <p class="lede" style="margin:1.2rem 0 2rem;">Rooms, a venue, a menu, a date &mdash; whichever it is, the reservations desk will pick it up.</p>
      <form id="enquiry" novalidate>
        <div class="field-row">
          <div class="field"><label for="first">first name</label><input id="first" name="first" type="text" autocomplete="given-name" required></div>
          <div class="field"><label for="last">last name</label><input id="last" name="last" type="text" autocomplete="family-name" required></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="email">email address</label><input id="email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="phone">phone</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
        </div>
        <div class="field"><label for="subject">subject</label><input id="subject" name="subject" type="text"></div>
        <div class="field"><label for="message">message</label><textarea id="message" name="message" rows="5"></textarea></div>
        <button class="btn" type="submit">send enquiry {ARROW}</button>
        <p class="form-note" id="enquiryNote">This opens your mail app with the enquiry addressed to the reservations desk, so nothing is stored on this page.</p>
      </form>
    </div>
    <div data-reveal="right">
      <ul class="infolist">
        <li><span class="k">phone</span><span class="v"><a href="tel:+917488535210">+91 74885 35210</a><br><a href="tel:+917488535208">+91 74885 35208</a></span></li>
        <li><span class="k">concierge</span><span class="v"><a href="tel:+917488535210">+91 74885 35210</a></span></li>
        <li><span class="k">email</span><span class="v"><a href="mailto:info@sambodhiretreat.com">info@sambodhiretreat.com</a></span></li>
        <li><span class="k">address</span><span class="v">Hathiyar, Bodhgaya, Gaya, Bihar &mdash; 824231, India</span></li>
        <li><span class="k">rates from</span><span class="v">&#8377;3,000 per night</span></li>
      </ul>
      <div class="btn-row"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">check availability {ARROW}</a></div>
    </div>
  </div>
  <div class="wrap" style="margin-top:clamp(2.4rem,5vw,3.8rem);">
    <div data-reveal="clip-l">
      <iframe class="mapframe" src="{MAPEMBED}" title="Map showing Sambodhi Retreat, Bodhgaya" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
    </div>
  </div>
</section>

<section class="section on-green">
  {curve('wave','var(--green)','top')}
  <div class="wrap split">
    <div class="col-5" data-reveal="left">
      <p class="label">getting here</p>
      <h2 class="dhead"><b>From the station</b><b><em>and the airport</em></b></h2>
    </div>
    <div class="col-7" data-reveal="right">
      <ul class="routes">
        <li>{VAN} Sambodhi Retreat Bodhgaya sits about 16.4 km from Gaya Junction &mdash; roughly 40 minutes via the Gaya&ndash;Bodhgaya Road.</li>
        <li>{VAN} Gaya Airport is an international airport serving Gaya, 12 km south-west of the city and 5 km from Bodhgaya. The retreat is about 15.0 km from the airport.</li>
      </ul>
    </div>
  </div>
</section>

<section class="section section--tight on-white">
  {curve('arc','var(--white)','top')}
  {wm('bl')}
  <div class="wrap split">
    <div class="col-6" data-reveal="up">
      <p class="label">our other property</p>
      <h2 class="dhead"><b>Sambodhi Retreat,</b><b><em>Dhanbad</em></b></h2>
      <ul class="infolist" style="margin-top:1.5rem;">
        <li><span class="k">address</span><span class="v">Jealgora, Govindpur Uttrayan NH-2, Dhanbad, Jharkhand &mdash; 828109</span></li>
        <li><span class="k">phone</span><span class="v"><a href="tel:+917280023024">+91 72800 23024</a> / 16</span></li>
        <li><span class="k">email</span><span class="v"><a href="mailto:infodhanbad@sambodhiretreat.com">infodhanbad@sambodhiretreat.com</a></span></li>
      </ul>
    </div>
    <div class="col-6 bleed-r" data-reveal="clip-r">
      <figure class="frame frame--plx frame--wide" style="margin:0">
        <img src="{IMG}HomePage-Villas/budhha-heights.jpg" alt="Sambodhi Retreat Dhanbad" data-parallax="0.22" loading="lazy" decoding="async">
      </figure>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- DECORATION
# Every coloured section gets botanical line-art, cycling through artworks and
# edge positions so no two neighbouring sections share a composition. Applied as
# a build step rather than by hand, so a section can never be missed.
LIGHT_DECOR = [
    [("", "tl"), ("sprig", "r")],
    [("lotus", "tr")],
    [("sprig", "bl"), ("mandala", "tr")],
    [("lotus", "l")],
    [("", "br")],
    [("mandala", "r")],
    [("sprig", "t")],
    [("lotus", "bl"), ("", "tr")],
]
GREEN_DECOR = [
    [("leafbig", "r")],
    [("leafbig", "bl")],
    [("leafbig", "l")],
    [("leafbig", "br"), ("sprig", "tr")],
]

def decorate(html):
    """Inject a decorative layer into every on-white / on-sage / on-green section."""
    out, pos, li, gi = [], 0, 0, 0
    while True:
        i = html.find('<section', pos)
        if i == -1:
            out.append(html[pos:]); break
        j = html.index('>', i)
        tag = html[i:j + 1]
        out.append(html[pos:j + 1])
        pos = j + 1
        if 'class="wm' in html[j:j + 400]:      # already carries artwork
            continue
        if 'on-green' in tag:
            combo = GREEN_DECOR[gi % len(GREEN_DECOR)]; gi += 1
        elif 'on-white' in tag or 'on-sage' in tag:
            combo = LIGHT_DECOR[li % len(LIGHT_DECOR)]; li += 1
        else:
            continue
        out.append("\n  " + "".join(wm(p, k) for k, p in combo))
    return "".join(out)

# ==================================================================== PAGES
PAGES = [
 dict(file="index.html", title="Sambodhi Retreat &mdash; Luxury Resort in Bodhgaya, Bihar",
      desc="Sambodhi Retreat, Bodhgaya. Sixty rooms across grass-clad cave cottages, igloos, timber cottages on stilts and pyramid cottages, set beside a swimming pool and the river Falgu.",
      body=None),
 dict(file="accommodations.html", title="Accommodations &mdash; Sambodhi Retreat, Bodhgaya",
      desc="Sixty rooms at Sambodhi Retreat Bodhgaya: green cave cottages, igloo houses, timber and pyramid cottages, woodland cottages, lotus studios and Buddha facing rooms.",
      hero=IMG+"Homepage_Resort_INDEX/top-slider-img11.jpg", crumb="accommodations",
      ta="Rooms &amp;", tb="Suites", tag="sixty rooms, twelve large suites and four family rooms &mdash; each built for the weather it sits in",
      cta=(IMG+"gallery/9.jpg","Your","Escape"), body=accommodations_body),
 dict(file="banquet-halls.html", title="Banquet Halls &mdash; Sambodhi Retreat, Bodhgaya",
      desc="The International Convention Centre and Conference Hall at Sambodhi Retreat, Bodhgaya: 50,000 sq ft for up to 5,000 guests, plus a 3,500 sq ft soundproof conference hall.",
      hero=IMG+"promotions/1.jpg", crumb="banquet halls",
      ta="Gather", tb="Beautifully", tag="an international convention centre and a soundproof conference hall on one estate",
      cta=(IMG+"promotions/2.jpg","Plan Your","Event"), body=banquet_body),
 dict(file="event-venue.html", title="Event Venue &mdash; Sambodhi Retreat, Bodhgaya",
      desc="Weddings, catered dinners, receptions, business conferences and family celebrations at Sambodhi Retreat, Bodhgaya.",
      hero=IMG+"Gallery/top-post-img3.jpg", crumb="event venue",
      ta="Moments Worth", tb="Celebrating", tag="a dedicated team plans the day down to the smallest detail &mdash; and then handles the unexpected",
      cta=(IMG+"Gallery/top-post-img2.jpg","Plan Your","Event"), body=event_body),
 dict(file="dining.html", title="Dining &mdash; Sambodhi Retreat, Bodhgaya",
      desc="The restaurant at Sambodhi Retreat, Bodhgaya: more than ten years of food and beverage experience behind a menu built by the chef and his team.",
      hero=IMG+"dining/restaurant1.jpg", crumb="dining",
      ta="A Taste of", tb="Sambodhi", tag="a menu unlike any other on the property, served in a room that never tips into formality",
      cta=(IMG+"dining/restaurant2.jpg","Your","Escape"), body=dining_body),
 dict(file="gallery.html", title="Gallery &mdash; Sambodhi Retreat, Bodhgaya",
      desc="Photographs of Sambodhi Retreat Bodhgaya: cottages, restaurant, reception and the surrounding natural attractions.",
      hero=IMG+"Homepage_Resort_INDEX/top-slider-img10.jpg", crumb="gallery",
      ta="Take a", tb="Look Around", tag="cottages, restaurant, reception and the grounds",
      cta=(IMG+"gallery/14.jpg","Your","Escape"), body=gallery_body),
 dict(file="blog.html", title="Blog &mdash; Sambodhi Retreat, Bodhgaya",
      desc="Stories from Sambodhi Retreat: weddings in Bodhgaya, organic food, places to visit, and what to expect from a luxury stay in Bihar.",
      hero=IMG+"Gallery/Top-5-Places-in-Bodh-Gaya.jpg", crumb="blog",
      ta="Stories from", tb="Sambodhi", tag="weddings, food, the city around us, and the things guests ask before they arrive",
      cta=(IMG+"gallery/24.jpg","Your","Escape"), body=blog_body),
 dict(file="contact.html", title="Contact &mdash; Sambodhi Retreat, Bodhgaya",
      desc="Contact Sambodhi Retreat, Hathiyar, Bodhgaya, Gaya, Bihar 824231. About 16.4 km from Gaya Junction and 15.0 km from Gaya Airport.",
      hero=IMG+"Homepage_Resort_INDEX/top-slider-img5.jpg", crumb="contact",
      ta="Begin Your", tb="Journey", tag="hathiyar, bodhgaya &mdash; about 40 minutes from gaya junction",
      cta=(IMG+"Homepage_Resort_INDEX/top-slider-img8.jpg","Your","Escape"), body=contact_body),
]

def build():
    for p in PAGES:
        if p["file"] == "index.html":
            inner = home_body()
        else:
            inner = (banner(p["hero"], p["crumb"], p["ta"], p["tb"], p["tag"])
                     + p["body"]() + locale_block(p["file"] not in ("gallery.html",)) + cta_band(*p["cta"]))
        html = (HEAD.replace("{TITLE}", p["title"]).replace("{DESC}", p["desc"])
                    .replace("{MENUNAV}", menu_nav(p["file"]))
                    .replace("{MENUPANEL}", menu_panel(p["file"]))
                    .replace("{TOPNAV}", nav_html(p["file"]))
                    .replace("{BOOK}", BOOK)
                + inner
                + FOOT.replace("{FOOTNAV}", nav_html(p["file"])).replace("{BOOK}", BOOK))
        (OUT / p["file"]).write_text(decorate(html), encoding="utf-8")
        print("wrote", p["file"], f"{len(html):,} bytes")

if __name__ == "__main__":
    build()
