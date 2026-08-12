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
