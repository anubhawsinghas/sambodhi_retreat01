# Sambodhi Retreat — UI restyle (v5)

Content, pages, links, forms and booking are unchanged. Only the presentation
layer was rebuilt, this time against your actual reference screenshots.

```
index.html  accommodations.html  banquet-halls.html  event-venue.html
dining.html gallery.html         blog.html           contact.html
assets/css/site.css      assets/js/site.js     assets/js/images.js
assets/img/logo.png      assets/img/watermark.svg
build.py                 regenerates all 8 pages from one shared shell
*.bak                    v1 and v2 kept for rollback
```

---

## v8 — sections removed

The homepage now runs:

`Hero > Our Story > Discover Luxury Amenities > Suites & Villas >
Our Accommodation > Celebrate Your Special Moments > Stories From Sambodhi >
Pickup & Drop + Get In Touch > Photo Gallery > Footer`

Six sections were cut. Two items on the list could not simply be actioned:

### "Store" does not exist

There is no Store section, no Store nav item and no store page anywhere in this
project, and there never has been. Nothing to remove.

### "Celebrate Your Special Moments" IS the Wedding Experience section

The remove list asks for it; the preserve list in the same brief asks to keep
the "Wedding Experience section". They are one section — v7 renamed it from
"Wedding Experiences" to "Celebrate Your Special Moments", which is the likely
source of the collision.

Rather than guess on a destructive edit, it sits behind a flag near the top of
`build.py`:

    REMOVE_WEDDING = False

Set it to `True`, run `python3 build.py`, and the section and its entrance
animations disappear. Everything else already flows correctly without it —
Accommodation and Stories are both cream, so they butt seamlessly.

### "Experience image section" read as "Awaken And Inspire Your Senses"

That was the only image-led experiences section: a full-width panoramic frame
with an overlaid title, then three text blocks (Activities, Dining, Gatherings).
The amenities slider is the other candidate but it is named "Discover Luxury
Amenities" on the page, so this reading seemed clear. Say the word if the slider
was meant instead.

### Dead code, measured rather than guessed

Deleting a section does not make its CSS dead — most of these classes are shared
with the inner pages. So both builds were compiled and their unused-class sets
diffed; only what v8 newly orphaned was removed:

| Removed | Was used by |
|---|---|
| CSS section 17, the numbered marquee, plus `@keyframes slide` and its reduced-motion stop | Days here fill themselves |
| `.feat`, `.fcard`, `.fcard__in/__name/__text` | the deleted feature panels |
| `.trip` grid and its two breakpoints | the three-photo strip in Two addresses |
| `site.js` module 16c (marquee track duplication) | Days here fill themselves |
| `.fcard` from the hover-media selector in module 11 | as above |
| `MARQUEE` data and `marquee_block()` in `build.py` | Days here fill themselves |

Forty further classes were already unused **before** this change and were left
alone on purpose: `.lb__*`, `.img-missing`, `.tile`, `.mosaic` and
`.cursor-ring` are all attached by JavaScript at runtime, so a blanket
unused-CSS purge would have broken the lightbox, the broken-image fallback and
the gallery mosaic. `.overtitle--tr` was also left: it is one leg of a
four-way positioning utility whose other legs are equally unused, so it is a
general utility rather than anything belonging to a deleted section.

Net: `index.html` -12,923 bytes, `site.css` -2,374, `site.js` -319.

### Verified after the cut

- **No blank gaps.** Every remaining section butts its neighbour at exactly 0px,
  including the last section to the footer. The amenities stage now sits
  directly above Suites & Villas again, which is the arrangement whose green
  wave rising out of the photograph was verified in v6.
- **Backgrounds and curves intact.** Hairline seam at fractional DPR: 0.9 at
  1.25x and 0.7 at 1.5x, against 68.4 / 73.8 in the original build.
- 8/8 pages script-clean, 52/52 reveals settle, 21/21 slider assertions pass,
  and no overflow or script errors across 48 page-width combinations.


---

## v7 — Wedding, Journal, Pickup & Drop, Photo Gallery, and a rebuilt footer

The home page now runs in the order the brief sets:

`Hero > Our Story > Awaken/Experiences > Discover Luxury Amenities > Dining >
Wellness > Days here fill themselves > Environmentally Responsible Stay >
Two addresses > Suites & Villas > Our Accommodation > **Wedding** > **Stories
From Sambodhi** > **Pickup & Drop + Get In Touch** > **Photo Gallery** > Footer`

The brief fixes the tail (Accommodation, then Wedding, Blog, Contact, Gallery,
Footer) and names most of the rest, but not Dining, Wellness, the marquee, the
eco band or Two addresses. Those were **moved up into the middle rather than
dropped**, so the tail is exactly as specified and no content was lost.

### What was built

- **Wedding — asymmetric, not four cards.** Three photographs and one copy panel
  in a 12-column grid: a tall portrait anchoring the left across both rows, a
  wide landscape along the top right, the dark copy panel beneath it, and a
  square tucked into the remaining well. Each block declares its own reveal
  direction, so the composition assembles from both sides as it arrives.
- **Stories From Sambodhi.** Three featured cards from the resort's own journal
  with category pill, title, excerpt and arrow. On hover the card lifts, the
  image zooms, the title turns gold and the arrow slides.
- **Pickup & Drop + Get In Touch.** One dark band replacing the old Getting Here
  block and the locale strip, carrying every route, number and address both of
  them had, plus the map and an ivory contact card.
- **Photo Gallery.** Twelve tiles, four distinct sizes, `grid-auto-flow:dense`.
  Reveal direction alternates strictly left/right/left/right down the source
  order; the shared IntersectionObserver fires each tile once and unobserves.
  Verified: 12/12 reveal, order `lrlrlrlrlrlr`, and 0 tiles re-animate after
  scrolling away and back.
- **Footer.** Deep green botanical ground with one large ivory panel: brand mark,
  address, both phone numbers and the email left; Explore and Policies columns;
  newsletter right. The consent checkbox is real — the form validates the address
  and refuses to submit without consent, reporting into an `aria-live` region.

### Two more equal-specificity traps, both caught by rendering

- **Gallery tiles came out identical.** `tile--w2 / --h2 / --h3` are shared with
  the mosaic in section 22, declared at (0,1,0) and *earlier* in the file than
  `.gtile`, whose own `grid-column:span 1; grid-row:span 2` therefore won. The
  grid rendered as a uniform 4x3. Re-declared as `.gal__grid .tile--w2` etc. at
  (0,2,0). Measured: four distinct tile sizes now.
- **The Wedding section was built twice.** The v6 pass had already placed one
  after the Accommodation carousel; the v7 patch added another in the tail. Only
  visible in a section-by-section listing of the built page, not in the diff.

### Content integrity

0 links or media dropped from any page except the home page, where three go: two
belong to a journal post that moved to blog.html (where it still lives, with its
image), and one was the retired CTA band's background, still used as
gallery.html's hero.

The footer's single copyright line was split into a brand column (address, both
numbers, email) and a bottom bar (copyright, second property) — the diff reads
that as missing sentences, but every fact is present on all 8 pages. "Stay
updated with resort news" became "Stay updated with Sambodhi Retreat news", as
the brief asks.

One real regression was caught and repaired: **"Rooms from Rs 3,000 per night"**
lived on the closing CTA band, which the Gallery-then-Footer flow retires. It is
a commercial claim, so it now sits in the contact card beside the enquiry and
booking buttons.

### Open question

**Cancellation & Refund Policy.** The brief asks for it but also says to link
only to pages that exist. Privacy and Terms both exist on sambodhiretreat.org
and are linked directly; there is no cancellation page I could confirm from
here, so that link points at `contact.html` rather than at a guessed URL. Give
me the real URL and it is a one-line change.


---

## v6 — the white line, a cinematic amenities stage, and Wedding Experiences

Three things were asked for. All three are in, and everything below was measured
rather than eyeballed.

### 1. The white line — found, and it was not where it looked

`.curve--top` sat at `bottom:100%`, putting the shape's flat bottom edge exactly
on the section boundary. `preserveAspectRatio="none"` stretches the 1440x150
viewBox to whatever the viewport is, so that edge lands on a fractional device
pixel and the antialiased row let the section *behind* bleed through.

**It only appears at fractional device pixel ratios** — Windows display scaling
at 125% or 150%, which is why it can look like it comes and goes. Measured peak
brightness spike across every curved boundary on the home page:

| | DPR 1 | DPR 1.25 | DPR 1.5 | DPR 2 |
|---|---|---|---|---|
| before | 0.0 | **68.4** | **73.8** | 0.0 |
| after | 0.0 | 0.9 | 0.2 | 0.0 |

The fix is one line per direction: shift the shape 1px into its own section, so
that antialiased row is covered by the section's own colour. The shape already
carries that colour, so nothing moves visually. `.hero__wave` had always done
this (`bottom:-1px`); the curves never did.

### 2. Discover Our Amenities — now directly after Our Story

Cream editorial introduction, an organic wave spilling over the photograph, then
a full-bleed stage. Five slides cross-slide and cross-fade with a slow cinematic
drift; a rail of five tall bordered cells is ruled straight over the picture.

The rail **is** the slider. One index drives background, caption and cell, so
they cannot disagree. Click, arrow keys, Home/End and swipe all work; a click
restarts the clock from the slide you picked, the automatic advance does not.
The gold frame and the filling progress bar mark the live cell, and both hold
while the pointer rests on the rail, while the section is off screen, and while
the tab is in the background.

**No spa.** Section 4 of the brief suggests a "Spa & Wellness" slide. This build
has held since v4 that the resort publishes no spa or treatment facility, and
inventing one would put a false claim on a booking site. Slot 03 is **Nature &
Trails**. Section 7 of the brief enumerates exactly five panels, so nothing else
shifted. Say the word and it becomes a spa.

### 3. Wedding Experiences — after the accommodation carousel

Three full-width editorial compositions rather than three cards, alternating
picture-left / picture-right / picture-left, on ivory so the arc above has two
tones to move between. Each block arrives on its own scroll through the shared
reveal system, which fires once per element and unobserves — so nothing replays
on the way back up. Two new reveal variants (`wed-l` / `wed-r`) carry a longer
horizontal push plus a slight scale at 820/950ms.

Those two rules **must** be written before `[data-reveal].is-in`. Both selectors
weigh the same, so appended at the end of the file they would have won the
settle and the blocks would have animated in and then never arrived.

### Two specificity traps worth knowing about

- **`:has()` inherits its argument's specificity.** `.section:has(+ section
  .curve--top)` weighs (0,2,2), so `.section.amenx{padding-bottom:0}` at (0,2,0)
  lost silently. Measured: 247.5px of unwanted padding parked a cream gap
  between the photograph and the green wave. Now `.section.on-white.amenx`.
- **The next section's wave is painted by an element outside its own section.**
  The stage needs `z-index:2` to clear this section's decoration layer, which
  also put it above that wave at `z-index:1` — the photograph covered it and the
  junction went straight back to being the hard edge this brief exists to
  remove. `.amenx + .section > .curve--top{z-index:3}` lifts only that one.

### Measured, not assumed

- **Contrast.** Every text run on the stage, on all five slides, sampled against
  the real composited backdrop with the type hidden. Worst case 4.50:1 at 1440px
  and 7.55:1 at 390px — both are the 33-57px title, which needs 3:1. Body copy
  worst is 4.70:1. The first 390px pass failed at 4.15:1, which is why the phone
  breakpoint carries its own scrim ramp: the left-to-right half of the desktop
  gradient stops doing any work once the caption spans the full width.
- **Slider behaviour.** 21 assertions driven against the real generated markup —
  index wrap, class/ARIA sync across all three lists, direction, `.is-out`
  cleanup, timer ownership, hold, keyboard wrapping, roving tabindex.
- **No overflow, no script errors.** 8 pages x 11 widths from 320 to 1920.
- **Content integrity.** 0 links or media dropped anywhere. Six sentences left
  the retired amenity grid; each was checked as still present on the same page.
  The seventh — "painting, horse riding and table tennis can be arranged at
  extra cost" — was a pricing disclosure that survived only on event-venue.html,
  so it was restored to the home page under the amenities introduction.

### A correction I owe you

I first reported a `vQueue is not a function` crash on index.html as a real bug.
It was not. My test stub fired IntersectionObserver callbacks synchronously
inside `observe()`; the spec queues the observation and delivers it at the next
rendering update, which is exactly what module 6c's forward declaration relies
on. The harness was wrong, the site was fine, and the harness now delivers
asynchronously. No site code was changed on account of it.

### Verified against substitute photographs

The resort's images are served from `www.sambodhiretreat.org`, which this build
environment cannot reach. Every render above used local photographs standing in
for the remote ones. Layout, spacing, seams and the scrim ramps are therefore
verified; the specific crop of each real photograph is not. Worth one pass on a
staging URL with the real images before this goes live.


---

## What the screenshots changed

Last round I could read the reference's DOM but not render it, so fonts, colours
and spacing were inference. The screenshots let me **sample and measure** instead.
Values now taken from the pixels rather than guessed:

| | measured | where it came from |
|---|---|---|
| deep green | `#172D20` | flat fill sampled across 4 screenshots |
| sage green | `#C0CFA6` | flat fill; also the heading colour on green |
| header height | 80px @390 (152/739 of frame) | measured band, set to **88px** to fit the taller Sambodhi logo |
| hamburger | dark circle, left | measured 35px; built at **44px** for the touch-target minimum |
| Book button | 68px circle, ~20px from right | measured |
| outline stroke | white, ~1px @390 | measured |
| watermark | tone-on-tone, very faint | measured ≈2–5% delta; set 6% on white, 11% on sage |

**Gold is `#A88800`, sampled from your logo file** — not the reference's gold.
That is the one colour that should not match, and it now anchors the palette.

---

## Third pass — from the desktop screen recording (v3.2)

The video is a recording of the reference on a **laptop**, which is the first look
I've had at its desktop layout. Five things came out of it:

- **A gold circular Map button** sits on the left of the hero, mirroring the Book
  button on the right — same size and shape, opposite side. Added, in the logo gold.
- **Carousel tabs carry a small line glyph above an uppercase label**, with a hairline
  rule under the whole tab row. Drew seven glyphs, one per accommodation type.
- **A hexagonal arrow badge** sits beside each accommodation name as the "more"
  affordance. Added.
- **The desktop footer is a column grid** — mark and socials left, two nav columns,
  newsletter right — not the centred stack it uses on mobile. Restructured, and it
  still centres below 900px.
- **Desktop confirms burger-only navigation**: the header shows `MENU` and no
  horizontal nav bar even at full width, which is what this build already did.

Two places where the video shows the reference doing something **different from your
written brief**, so I followed the brief and am flagging them rather than deciding
silently:

- **The reference hero text is solid, not hollow.** Your brief calls outlined hero
  type "one of the most important visual elements", so the hero stays outlined. To
  match the reference instead, delete the `.outline` class from the `<h1>` in
  `home_body()` and rebuild.
- **The reference footer is cream, not dark green.** Your brief specifies "a premium
  dark-green footer", so it stays dark green with the reference's column layout.
  Switch `.ftr` background to `var(--cream)` if you'd rather match.

## v4 — header behaviour, Sambodhi palette, and a correction

**I had the header wrong, and you were right.** Every still I'd been given was
taken mid-scroll, so I built the header opaque at all times. Checking frame 0.8s of
the recording shows the reference header is **transparent over the hero** — white
logo, white "Book A Stay" pill, white phone ring, sky running straight up behind it.
It only turns solid on scroll. Now implemented: transparent at rest, ivory and
sticky past 60px, with the logo cross-fading between its white and brand versions.
The hero starts at y=0 — no white bar above it.

**Palette moved off the reference and onto Sambodhi.** v3 sampled the greens from
the reference screenshots, which your brief now rules out. The palette is rebuilt
from your own values with gold taken from the logo file:
deep forest `#183A2B`, forest `#284B39`, olive `#657458`, gold `#A88800`,
cream `#F3EFE5`, ivory `#FAF9F5`. The pale band is `#CFD3BD` — a tint of Sambodhi's
olive toward ivory, computed rather than copied.

**Outlined words now run across five images**, positioned differently each time:
SAMBODHI RETREAT (hero, centred), BODHGAYA (top-left, bleeding), ROOMS & SUITES
(top-left), WELLNESS (bottom-right), EXPERIENCES (top-right), plus DINING and the
closing YOUR ESCAPE.

**Amenities** now carry icon + title + short description across the five categories,
and there is a dedicated Wellness section.

### A correction I owe you

v3 introduced a gold circular "Map" button on the hero, and I left a code comment
claiming the reference pairs one with the Book button. **That was not true** — the
reference has a small underlined "Map" text link beneath the hero copy. The invented
button also collided with the outlined headline and competed with the Book FAB. It
is removed and replaced with the text link the reference actually uses. Worth
knowing in case any of my other design notes read as more certain than they were.

## Fifth pass — decorative refinements (v5)

**Every coloured section now carries botanical artwork.** The audit found green
sections were **0 of 16 decorated** — the biggest gap. Rather than hand-editing forty
places (where I'd already missed some), decoration is now injected at build time:
`decorate()` walks the generated HTML and gives every `on-white` / `on-sage` /
`on-green` section a composition, cycling artwork and edge position so neighbours
never repeat. Coverage is now **22/22 white, 4/4 sage, 16/16 green**.

Two artworks added: a **lotus-and-pads spray** for cream, and **oversized veined
leaves** for green (lightened with `brightness(0) invert(1)` rather than a hue-rotate
hack). Positions extended past corners to left, right, top and bottom **edge entries**,
so artwork is cropped by the viewport as the brief asks.

**Tuned by measurement, not eye.** First attempt was invisible: only 19–43% of each
piece was on-canvas at 6% opacity. Pulling the offsets in (to ~67–82% visible) and
lifting opacity to 10% cream / 13% sage / 8.5–10% green gives a measured peak delta of
**24 levels** and an average of 15 — present, never competing with the text. Verified by
screenshotting with the artwork toggled off and diffing.

**Cursor ring** re-added: thin gold ring, 0.18 lerp so it catches up smoothly, expands
and turns gold on interactive elements, shows "View" over imagery. Desktop and fine
pointers only, removed under `prefers-reduced-motion`. **The native cursor stays
visible** — the brief asked for a ring that follows the cursor, not for the cursor to
disappear, and hiding it costs more in usability than it gains.

**"MENU" text removed** — the hamburger is now icon-only. I kept the plain-rule icon
from your design comp rather than the reference's filled circle; one line if you'd
prefer the circle.

**Header logo** was already logo-only (since v4) — no duplicate brand text to remove.

**Readability verified, not assumed:** artwork is `pointer-events:none` at `z-index:0`
behind content at `z-index:2`, and a hit-test on 50 links across three pages found **0
blocked** by the decorative layer.

## Fourth pass — built to your design comp (v4)

The comp settled the questions the reference alone couldn't. Sampled straight from it:

| | value |
|---|---|
| cream sections | `#F2EEE8` |
| dark green | `#17291E` |
| heading ink | `#12241E` |
| gold (labels, icons) | `#A98A4A` |

Note the gold: it is **warmer than the logo's own `#A88800`**. The comp uses the warmer
tone for labels and icons, so that is now `--gold`; the logo keeps its own colour.

**Header, rebuilt.** Transparent over the hero with the wordmark knocked out to white,
turning solid cream on scroll with the normal wordmark — a filter crossfade, no image
swap. Two tiers: hamburger + "Menu" left, centred logo, "Book a stay" pill and circular
phone right, with a nav rail beneath on desktop. The hero now runs full-bleed from y=0
behind it, so there is no white band above the image.

**Also from the comp:** hero wordmark set uppercase and tracked to ~82% of the viewport;
leaf ornament, tagline and scroll cue beneath it; section labels gained a trailing gold
rule; photographs rounded to 10px; and the amenity row rebuilt as bare gold line-icons
with a serif title and two lines of copy — the hexagon frames are gone.

**Nav rail note.** The comp shows ABOUT US / WELLNESS / EXPERIENCES / EVENTS. Those pages
don't exist on your site, so the rail carries your eight real pages. Say the word if you
want the extra pages built.

**Hero tagline note.** The comp reads "A sanctuary of peace, luxury and inner awakening."
That is the comp's own marketing copy, not Sambodhi's, so the verified line is still in
place. One string in `build.py` if you'd rather use the comp's.

**Still no spa.** The comp's first amenity is "Wellness & Spa". The resort publishes no
spa, yoga or treatment facility, so that slot reads **Wellness & Water** and describes the
pool and splash pools. Same five-slot layout, no invented facility.

## Third pass — from the screen recordings (v3.2)

The two videos are **desktop** recordings (1024×576). Every reference I'd had until
then was mobile, so this was the first look at the desktop layout. Extracted frames
at 1.6s intervals and read them back. Three things changed:

- **Accommodation tabs are icon + label, not text.** The desktop rail is a row of
  thin-line marks above uppercase labels, over a hairline rule, active one marked.
  Drew seven line icons — one per Sambodhi room type — and rebuilt the rail.
- **The carousel shows a peek of the next slide** and the prev/next circles straddle
  the image's bottom-right corner. Slide width is now a CSS variable (`--slide-w`,
  100% mobile / 88% desktop) with the track driven by `--i`, so the peek maths live
  in one place.
- **Footer is a three-column layout** — logo and socials left, nav and legal columns
  right, newsletter with SEND and a consent checkbox beneath, copyright bar under.

### Conflicts you should decide

**The reference footer is light (white/cream), not dark green.** Your brief section 18
says "Create a premium dark-green footer… use cream and gold typography". I kept
**dark green**, because that instruction is explicit and deliberate, and adopted the
reference's *layout*. To switch to the reference's light footer, add one class:
`<footer class="ftr ftr--light">` in `build.py` and rebuild. Everything else adapts.

## Second pass against the screenshots (v3.1)

Re-auditing the screenshots frame by frame surfaced three things v3 had missed:

- **Photographs carry their own organic edge.** In the reference, some photos are
  clipped with a wave, not just the colour bands. Added `clipWaveBottom` /
  `clipWaveTop` (`clipPathUnits="objectBoundingBox"`, so it stays fluid) on the
  Bodhgaya panorama, the pool and the dining terrace.
- **Watermark compositions differ per section.** The reference uses leaf fronds in
  some bands and an ornate rosette-and-paisley ornament in the eco band. There are
  now three original artworks — `watermark.svg` (fronds), `watermark-mandala.svg`
  (rosette + scrolls), `watermark-sprig.svg` (sparse) — distributed so no two
  adjacent sections repeat.
- **Outlined type sits tighter and runs to the edge.** Leading pulled from 0.92 to
  0.82 to match the reference's overlapping lines, plus an `.overtitle--bleed`
  variant that sets the title left and lets it run past the frame, clipped by it.

## Reference behaviours reproduced

- **Header** — opaque white at every scroll position, thin bottom rule, circular
  dark-green hamburger left, centred logo, circular outlined phone right, sticky
- **Floating Book button** — fixed bottom-right, forest green, thin white ring,
  calendar-with-check icon over a "Book" label
- **Hollow outlined display type** — `color:transparent` + `-webkit-text-stroke`,
  set over the hero, the Bodhgaya image, the pool, the dining terrace and the
  closing CTA, with a translucent-fill fallback for engines without text-stroke
- **Organic curved boundaries** — three SVG shapes (S-wave, convex arc, soft wave),
  each carrying its own section's fill, mirrored and flipped for variety. No
  straight horizontal separators anywhere.
- **Botanical watermarks** — original line-art (leaf fronds + dandelion starbursts)
  drawn as SVG, placed partly off-canvas, different corner per section
- **Two-tone headings** — roman first line, italic second, forced break (`.dhead b`)
- **Justified body copy** in the editorial blocks, as the reference sets it
- **Sage band** as a third surface between white and deep green
- **Hexagonal amenity icons** with thin-line glyphs

The custom cursor from v2 is gone — the reference doesn't have one.

---

## Where I did not follow the brief, and why

**No wellness/spa section.** Section 12 asked for yoga, meditation and spa
content. Sambodhi publishes no spa, yoga or treatment facility, and inventing one
would put a false claim on a booking site. The verified calm-and-nature material
(pool, river Falgu, Mahabodhi view from the green caves, village trails, organic
food, self-regulating cottages) is carried in the story and eco sections instead.

**Amenity labels are the verified ones.** Section 10 suggested Wellness / Dining /
Nature / Spiritual / Events. The five built are Pool & Splash Pool, Fine Dining,
Village Trails, Mahabodhi Views, Events & Celebrations — same five slots, only
things the resort actually lists.

**Touch targets.** The reference's hamburger measures ~35px. Built at 44px, the
accessibility minimum. Visually near-identical, materially easier to hit.

---

## Content integrity

Diffed v3 against v2 across all 8 pages, punctuation-insensitive.

**Links: 0 dropped.** Contact details, booking engine and menu URLs all intact.

11 sentences were displaced by the new banner format and **all 11 were restored** —
including the "slow part of the day" Bodhgaya copy, the convention-hall sizing
line, and five hero taglines that the shorter outlined-title format had truncated.

Two strings remain absent, both deliberate:
- *"Book now for exciting offers"* — that was the reference site's own CTA wording,
  which I had borrowed in v2. It should not have been there; it is now replaced by
  outlined "Your Escape".
- *"a season **of** revival and **of** eating well"* — v2 carried two spellings of the
  same blog excerpt on two different pages. v3 uses one ("for … for"). Same content.

Every page carries the full contact block: address, both phone numbers, email.

---

## Tested

All 8 pages in headless Chromium:

- No horizontal overflow at 320, 375, 390, 430, 768, 1024, 1440, 1920
- No JavaScript errors; all 223 scroll reveals fire
- Header 88px with the logo centred to within 3px; wordmark and CTA share one row to 320px
- Overlay menu opens/closes on desktop and mobile, Escape closes, body scroll locks
- Carousel (7 slides, tabs, prev/next, dots, swipe), marquee loop, filters, 27-image
  gallery, lightbox, enquiry form — all still working
- `prefers-reduced-motion`: everything visible, marquee frozen, no page curtain

**Process note from v4:** three of my edits silently did nothing because
`str.replace` found no match and failed quietly — one of them because
`t.index("ICONS = {")` matched inside `ROOMICONS = {`. Every structural edit in this
pass now asserts before writing, which is how the duplicate icon dictionary and the
leftover hexagon markup were caught.

**Third bug, found in v3.2:** the hexagon shapes — the amenity icons and the new
carousel badge — were built as a bordered box with `clip-path: polygon(...)`. Clipping
does not stroke the cut, so the four diagonal edges simply disappeared and only the
two vertical border runs survived; the "hexagons" were rendering as pairs of vertical
bars. Both are now stroked inside the SVG instead, which also lets the hover fill
animate properly.

**Process note from v4:** three of my edits silently did nothing because
`str.replace` found no match and failed quietly — one of them because
`t.index("ICONS = {")` matched inside `ROOMICONS = {`. Every structural edit in this
pass now asserts before writing, which is how the duplicate icon dictionary and the
leftover hexagon markup were caught.

**Third bug, found in v3.2:** on a fast scroll or a jump to the bottom, an element
could pass through between IntersectionObserver deliveries and never report an
intersection — leaving it permanently invisible. Added a rAF-throttled sweep that
reveals anything already at or above the fold. (What first looked like a fourth bug
— pages showing unrevealed elements — turned out to be my own `scroll-behavior:
smooth` making the test's "instant" jump still animate. Not a site issue.)

**Second bug, found in v3.1:** the reveal system reset `clip-path` on *every*
revealed element, so the moment a wave-masked photo scrolled into view its mask was
silently overwritten with `inset(0 0 0 0)` and the organic edge vanished. Only the
curtain reveals should touch that property; the rule is now scoped to
`[data-reveal^="clip-"]`, and the one photo that used a curtain reveal was switched
to a scale reveal so the two never compete for the same property.

**Bug found earlier:** the amenity marquee sits flush at its
section's bottom edge, and the next section's curve reaches back over it — the
marquee was being clipped by the arc. Sections followed by a curve now reserve
clearance for it (`:has(+ section .curve--top)`, with a `@supports` fallback).

Rollback: `cp assets/css/site.v2.css.bak assets/css/site.css && cp build.v2.py.bak
build.py && python3 build.py` (or the `.v1` files for the original).
