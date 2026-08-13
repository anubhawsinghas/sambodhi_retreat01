# v11.1 — animation-check.html

No change to the site. One standalone diagnostic page added at the project
root, because "the animation isn't running" has several causes that look
identical from the outside and none of them can be told apart by eye.

`animation-check.html` loads the real `assets/css/site.css` and
`assets/js/site.js`, builds a genuine `.villa` block so the real controller
picks it up, and reports what they are actually doing in that browser:

- whether the OS is asking for reduced motion (the animation is then suppressed
  **by design** — the single most likely reason for "nothing moves")
- whether `IntersectionObserver` exists
- whether the stylesheet is the current one (transition reads `1s, 1.15s`)
- whether the parallax rule is applied to the photograph
- whether the block starts hidden
- live, as you scroll: whether the reveal fires and whether `--villa-p` tracks

Then a plain-language verdict naming the fix.

**A false negative in the first version**, caught by running the page under
`prefers-reduced-motion: reduce`: the stylesheet check and the parallax check
both reported **fail**, because reduced motion sets `transition:none` and
`transform:none` deliberately — so neither can be measured. Anyone with Reduce
Motion switched on would have been told their site.css was stale and sent to
delete their assets folder for nothing. Both now report as unmeasurable and say
why. The verdict was gated the same way.

Delete this file before deploying. It is not linked from anywhere and the site
does not reference it.

---

# v11 — Suites & Villas: replayable entrance + scroll-linked parallax

Builds on v10. The directions, the 14% overlap and the trigger-on-entry were
already in place; this pass adds what was missing and corrects the timing.

---

## Changed

| | v10 | v11 |
|---|---|---|
| Duration | 1.5s / 1.9s | **1s opacity, 1.15s transform** (brief asked 0.8–1.2s) |
| Travel | 6vw | 5vw |
| Replay on scroll back | no — one-shot | **yes** |
| Image parallax | none | **scroll-linked zoom-out + drift** |
| Mobile motion | 9vw sideways | **fade + 30px rise** |

Easing stays `--e-hero` (expo-out) — it settles rather than arrives, which is
what keeps it from reading as dramatic.

## Why these blocks needed their own attribute

Replay could not be done on the shared `[data-reveal]` system. That system is
one-shot by design — it unobserves after firing — and its scroll sweep
re-reveals anything sitting above the fold. A block that reset itself would be
re-revealed by the sweep on the very next frame, so the reset would appear to
do nothing at all.

The blocks now use `[data-villa-in]` with their own controller. The two systems
no longer share state, and the section heading above them is untouched: it
still uses the shared one-shot reveal, because a heading that replays every
time you scroll past is irritating rather than premium.

Reset is deliberately not "the moment it stops intersecting" — it waits until
the element is genuinely clear of the window (`bottom < 0` or `top > innerHeight`).
Without that hysteresis, a small scroll near the trigger line flickers the
block on and off.

## Parallax

`--villa-p` runs 0 → 1 across the block's whole passage through the window and
CSS turns it into one transform:

```
translateY (p - .5) * -3%   and   scale 1.10 -> 1.05
```

The floor of 1.05 is load-bearing. At that scale the image overflows its frame
by 2.5% on each edge while the drift only ever asks for 1.5%, so an edge can
never be exposed — verified by scanning 19 scroll positions across the passage
and asserting the image still covers the frame at every one.

No transition on that transform: it is driven by the scroll itself, and a
transition would make it lag the finger. The hover zoom that was on these
images was removed rather than left to fight the scroll transform for the same
property.

## The bug in the first version of this

`--villa-p` was only painted from the scroll handler. IntersectionObserver
callbacks are delivered *after* the scroll that caused them, so a block that
became live on a jump — restored scroll position, anchor link, deep link — kept
the default `--villa-p` until the reader happened to scroll again, then visibly
snapped. Measured directly: `--villa-p` read as unset after scrolling the block
into view and waiting 1.5s. The observer now paints on every change to the live
list; the same measurement returns 0.314.

## Verified

1600 / 1440 / 1024 / 390px — directions correct per block, overlap 14% on
desktop, transitions land at `1s, 1.15s`, transforms fully settle, no exposed
image edge at any of 19 scroll positions, no horizontal scroll.

Entrance sequence tested end to end: hidden before the block is reached →
settled on entry → **reset once scrolled well past** → **replayed and settled
again** on scrolling back up.

Mobile start transform is `matrix(1,0,0,1,0,30)` — vertical only, no sideways
travel. Reduced motion and JavaScript-off both leave the blocks fully visible
and untransformed. All eight pages: no page errors, no local asset failures.
The v8 hero still pins, the v9 story rows are unchanged.

---

# v10 — Suites & Villas: two layered blocks

Home page only. The section keeps its dark green band, its botanical artwork,
its gold accents and the floating Book button; the heading is renamed from
"Rooms & Suites" to "Suites & Villas" (one occurrence, home only — the
accommodations page is untouched).

---

## Removed

The full-width `top-slider-img11.jpg` banner with the outlined "Rooms & Suites"
lettering over it, and its `.overtitle` — gone from the section entirely. The
heading is now clean type on the green ground. The same filename still appears
twice in the overlay menu as the Accommodations thumbnail; that is a different
use and was left alone.

## Built

The two `.fcard` tiles became two alternating feature blocks, carrying their
existing photographs and copy across unchanged:

| | Picture | Copy | Enters from |
|---|---|---|---|
| Block 1 | left | right | picture ← left, copy → right |
| Block 2 | right | left | copy ← left, picture → right |

## The overlap is a ratio, not a pixel guess

The picture spans 7 of 12 grid columns and the copy panel starts on the last of
them. That puts exactly one seventh — **14%** — of the photograph behind the
panel, and it stays 14% at every width because it is a property of the grid
rather than a negative margin tuned at one breakpoint. Measured at 1600, 1440,
1280 and 1024px: 14% each time.

The panel carries its own `--green-2` background and is the upper layer, so the
overlap costs nothing in readability — no text is ever set over the photograph.

## The bug in the animation

The blocks needed a slower, longer run-in than the site default, so the start
positions were overridden per block:

```css
html.js .villa [data-reveal="left"] { transform: translate3d(-6vw,0,0); }
```

That selector has exactly the same specificity as section 15's
`html.js [data-reveal].is-in{ transform: none }` — and being later in the file,
it **wins even after the class lands**. The blocks would have received `.is-in`,
faded in, and then sat permanently 6vw off to the side.

Fixed with `:not(.is-in)` on the start-position rules, which both raises the
specificity and stops them applying once the element settles. Verified by
asserting `getComputedStyle(el).transform === 'none'` after the transition
rather than by eye — the fade alone looked plausible in a screenshot.

Motion itself: 1.5s opacity, 1.9s transform on `--e-hero` (expo-out, settles
without bounce). The wider run-in is absorbed by the `overflow-x: clip` set in
v8, so it produces no scrollbar.

## Stacked

Below 900px the picture goes first and the panel laps up over its lower edge,
inset from both sides — the layering survives the breakpoint instead of
collapsing into two plain boxes.

## Verified

1600 / 1440 / 1280 / 1024 / 900 / 390px: overlap present, panel above the
picture, slide directions correct per block, transforms fully settled, no
horizontal scroll. Reduced motion leaves both blocks at full opacity and no
transform. All eight pages: no page errors, no local asset failures. The v8
pinned hero still pins and the v9 story rows are unchanged.

Final order: hero -> Our Story (2 rows) -> Suites & Villas (2 blocks) -> Our
Accommodation.

---

# v9 — Our Story: two editorial rows

Home page only, replacing the single story band that sat under the hero. All
of the previous copy is carried over — nothing was cut.

---

## A finding worth reading first

`New_img/our_story.png` is **not a photograph**. It is a finished design comp
of an "Our Story" section: outlined "Our Story" heading, gold dot and rule,
body copy and the Sambodhi wordmark all baked into the pixels, over a mandala
watermark. Dropped into a layout as an image it renders as a picture of a web
page inside a web page — during the build a stray outlined "y" from the comp
appeared floating over the photograph, which is what led to checking it.

It has been treated as the reference it evidently is. Its clean photographic
half (x 760–1672) is cropped out to `New_img/story-grounds.jpg`, and that is
what the first row actually uses.

## Structure

```
hero  ->  · Our Story
          row 1   copy LEFT    picture RIGHT   word "SAMBODHI"
          row 2   picture LEFT copy RIGHT      word "AWAKEN"
      ->  Rooms & Suites (unchanged)
```

Both rows live in one `.section.on-white`, not two. That keeps the cream field
continuous, lets the gap between the rows be tuned independently of the section
padding, and — the practical reason — leaves the `:nth-of-type` cycle that
rotates the botanical artwork through later sections undisturbed.

## The word

Decoration on its own layer, `z-index: 1`, below both the picture and the copy.
The picture crops its lower third and its tail; nothing readable is ever under
it. `.outline--ink` is a new variant of the hero's outlined type — the hero
version is a white hairline with a stacked dark halo built for photographs, and
that halo turns to smudge on cream, so this one is a bare ink hairline with the
filter off.

"AWAKEN" is two letters shorter than "SAMBODHI", so on the mirrored row it
would only graze the picture. `--eword-tuck` nudges it toward the photograph:
both rows now take a comparable bite (28% / 23% at 1440px).

## The bug this section had at ~1024px

The row reserved only part of a word-height at the top and relied on the
picture being the tallest thing in it. It is not: between roughly 900 and
1100px the copy column narrows enough to become the taller item, drive the row
height, and push its own heading straight into the letters.

Fixed by separating the two concerns. The row reserves a **full** word height,
so the copy is clear at every width; the picture is then pulled back up into
that band with a negative margin and `align-self: start`, which is what creates
the overlap. Copy clearance and picture overlap no longer depend on each other.

## Verified

Measured at 1600, 1440, 1280, 1024, 768 and 390px: word never intersects the
copy, both images cover their frames, no horizontal scroll, and the word stays
on the page. Stacked layouts put the picture first in both rows so the word
still lands on a photograph rather than on the heading. Reduced motion leaves
every element at full opacity. All eight pages: no page errors, no local asset
failures. The v8 pinned hero still pins.

## Open item

`STORY2` points at `homePage-Villas/green-cave.jpg` from the client's own image
catalogue, chosen because the copy names the green cave cottages. It is the one
thing here that could not be previewed — the sandbox cannot reach the domain —
so its 4:5 crop is unverified.

---

# v8 — cinematic hero reveal (home)

Home page only. Content, links, images, forms and booking are unchanged, and
the inner-page banners (`.hero--page`) are untouched — every new rule is scoped
to `.hero--reveal`.

---

## The brief

The first screen was showing the cream wave curve and the top edge of the story
section straight away, so the hero never read as a full-bleed photograph. The
ask was the Kushal Palli scroll: photograph fills the first screen, a little
scroll lifts it to show the band hiding below the fold, then the next section
arrives — smoothly, and without making the hero tall.

## What was actually wrong

Two things, and the second one was the real obstacle.

**1. The wave lived inside the hero window.** `.hero__wave` was a child of
`.hero__media`, pinned to `bottom: -1px` of a `100svh` block. A cream curve at
the foot of the first viewport is unavoidable in that arrangement — there is
nowhere else for it to go.

**2. `position: sticky` was silently dead site-wide.** `html` and `body` both
carried `overflow-x: hidden`. That computes `overflow-y` to `auto` and turns
both into scroll containers, so a sticky descendant sticks inside a box that
never scrolls — i.e. it does not stick at all, with no error and no warning.
Measured before the fix: at `scrollY: 60` the pinned pane sat at
`top: -60px` instead of `0`.

## Changes

### 1. `overflow-x: clip` instead of `hidden` (site.css section 2)

`clip` trims the same horizontal overflow but does **not** create a scroll
container, so sticky works. The `hidden` declaration stays first as the
fallback for engines that do not know `clip`; `@supports not (overflow: clip)`
drops the hero back to one honest screen there.

This is the only change outside the hero. Verified: no horizontal scrollbar on
any of the eight pages, at 1440, 1280, 1920 and 390px.

### 2. The hero is now a pinned window with a taller picture inside it

```
.hero--reveal        height: 100svh + --hero-reveal   (the scroll runway)
  .hero__media       position: sticky, exactly 100svh (the window — never taller)
    .hero__frame     height: 100svh + --hero-reveal   (the picture — lifts)
      .hero__slide   x4, background-size: cover
  > .hero__wave      child of the SECTION, not the window
```

`--hero-reveal` is `max(clamp(150px, 26svh, 300px), calc(var(--curve-h) + 90px))`.
The `clamp` keeps the runway short; the `max` floor guarantees the curve is far
enough below the fold that no cream is visible on the first paint, at any
window size. Measured runway: 219px on a 390x844 phone, 240px at 1440x900,
281px at 1920x1080 — one flick of the wheel, as the brief asked.

### 3. One number drives everything

`site.js` writes `--hero-p` (0 to 1) across the pin, on `requestAnimationFrame`,
skipping repaints under a 0.0004 delta. The frame lift, the wordmark drift and
fade, and the scroll cue all read from it in CSS, so they cannot fall out of
step with each other or with the scroll.

The wave is deliberately **not** on that system. Anchoring it to the section
foot means plain document flow carries it into view exactly as the hero runs
out — no JS, and nothing to desynchronise.

### 4. Header stick threshold follows the hero

It was flipping to solid cream at `scrollY: 60`, which dropped a cream bar over
the photograph mid-reveal. It now measures the pin length on load and resize and
flips at the end of it.

### 5. Two details found by measuring, not by eye

- **A drop-shadow on the wave was spilling a grey band onto the section below.**
  Sampling pixels across the boundary showed `#F2EEE8` above and `#E5E2DD`
  below — a visible seam in the one transition this pass exists to smooth.
  Shadow removed; the boundary now runs uniform `#F2EEE8` straight through.
- **The scrim was a blanket over the photograph.** Replaced with a wide, soft
  pool under the wordmark plus a light wash at the top for the header, so the
  picture keeps its own light and the type still holds up over the bright
  umbrella on slider 4.

## Fallbacks

| Condition | Behaviour |
|---|---|
| `prefers-reduced-motion` | `.is-static` added in JS; hero returns to one 100svh screen, curve at its foot, wordmark at full opacity. Verified. |
| JavaScript off | `html:not(.js)` rule, same single-screen result. Verified. |
| No `overflow: clip` support | `@supports not` guard, same single-screen result. |

## Verified

Headless Chromium, at 1440x900, 1280x720, 1920x1080 and 390x844: pane fills the
screen, wave below the fold, next section below the fold, no horizontal scroll,
pane pinned, frame lifting mid-scroll. All eight pages load with zero local
asset failures and no page errors.

`build.py` regenerates this hero, so a rebuild reproduces the change instead of
reverting it. Previous files kept as `*.v8.*.bak`.

---

# v6 — decoration pass

Content, pages, links, images, forms and booking are unchanged. This pass is
CSS and artwork only.

---

## What was already done, and what wasn't

I audited the build before changing anything. Five of the ten brief items were
already satisfied, verified by reading the live DOM rather than by eye:

| Brief item | Finding |
|---|---|
| 5. No "MENU" text | Already done. `.menu-btn` has no text node; `aria-label="Open menu"` carries the accessible name. |
| 6. Logo only | Already done. `.brand` contains one `<img>` and nothing else. |
| 7. Cursor follower | Already done. 1px ring, 0.18 lerp, expands on hover, desktop and fine-pointer only. |
| 8. Curved transitions | Already done. 9 SVG curves on the home page, no straight separators. |
| 9. Outlined typography | Already done. `-webkit-text-stroke: 1.6px`, `color: transparent`, 6 instances. |

**Items 1–3 were the real gap, and it was measurable.** Instrumenting every
coloured band at 1440px found the tall editorial sections nearly bare:

```
section height 2056px  ->  5.5% covered by artwork
section height 1659px  -> 10.9%
section height 1375px  ->  8.2%
section height 1187px  -> 15.3%
```

The cause was a hard ceiling: `.wm` was `clamp(280px, 58vw, 660px)`. On a
1440px canvas the widest piece capped at 660px, so a 2000px-tall cream section
got one small graphic tucked in a corner and read as a flat field. That is the
"too simple and empty" in the brief.

---

## Changes

### 1. Three new botanical artworks

Original line art, drawn in the same hairline idiom as the existing pieces
(unfilled strokes, organic curves) but sized for large desktop canvases:

| file | size | role |
|---|---|---|
| `assets/img/wm-bloom.svg` | 900 x 900 | oversized open bloom, corners and right edge |
| `assets/img/wm-branch.svg` | 560 x 1000 | tall flowering branch, left and right edges |
| `assets/img/wm-vine.svg` | 1000 x 560 | trailing vine, top and bottom edges |

Generated by `tools/make_botanicals.py`, so they can be re-tuned and re-emitted
rather than hand-edited. Leaves sit on the stem tangent and petals fan on
computed rings, with small deterministic jitter so nothing looks stamped.

Two bugs found and fixed during drawing, both visible only at full opacity:

- **Leaf veins were falling outside the leaf.** The vein base points were being
  derived from a mix of midrib offset and raw stem angle, which drifted past
  the outline on curved leaves. Veins are now sampled from the real quadratic
  curves — a point on the midrib to a point further along the flank — so they
  cannot escape the leaf.
- **Flower centres were solid knots.** Every petal and stamen originated at the
  exact centre, so thirty strokes converged on one pixel. Petals and stamens
  now start on a hub radius, leaving the centre open.

### 2. A CSS-only auto-decoration layer

`site.css` section 4b. Every `.on-white` / `.on-sage` / `.on-green` band gets
two further pieces via `::before` and `::after`.

This is deliberately CSS-only rather than build-time markup:

- it needs **no HTML changes**, so it applies to any build of the markup
- it **survives `python3 build.py`** — the CSS is not generated by the build
- it touches no content, images, forms or booking code

Four compositions cycle on `:nth-of-type`, so neighbouring bands never repeat.
Corner placements stay with the existing `.wm` spans; this layer takes only the
side and bottom edges, so the two never compete for the same corner.

**Vertical pieces are sized as a percentage of section height**, not viewport
width. That is the specific fix for tall sections: a branch at `height: 76%`
grows with the band instead of capping out at a fixed pixel width.

### 3. Existing watermarks unclamped

`.wm` ceiling raised 660px -> 1040px, `.wm--sprig` 520px -> 760px,
`.wm--leafbig` 820px -> 1180px. The lower bounds are unchanged, so small
viewports are unaffected.

---

## Measured result

Coverage per section, all 8 pages, 42 coloured bands, at 1440px:

| | before | after |
|---|---|---|
| median coverage | 12.7% | **53.7%** |
| minimum coverage | 5.5% | **25.9%** |
| bands under 18% | 9 | **0** |

Opacity stays inside the brief's 5–12% band: 8.5% on cream, 11.5% on sage,
7.5% on green (whitened with `brightness(0) invert(1)`), dropping to 7% below
600px. Measured perceptual delta against the same page with the layer disabled:
peak 19–38 levels, mean 10–13 on inked pixels. Present when looked at, never
competing with the text.

---

## Tested

- **Horizontal overflow** — PASS, 8 pages x 8 widths (320, 375, 390, 768, 900,
  1024, 1440, 1920). Artwork bleeds off-canvas and is cropped by the viewport,
  as the brief asks, without adding a scrollbar.
- **Click hit-test** — 561 interactive elements across all pages. 14 report a
  different topmost element on the home page, and the **same 14 do so on the
  pre-change stylesheet**, so the decorative layer blocks nothing. (They are
  the sticky header and `<b>` children inside links, both pre-existing.)
- **z-order and pointer-events** — every pseudo-element resolves to
  `z-index: 0` and `pointer-events: none`, under the `z-index: 2` content layer
  set by `.section > .wrap`.
- **JS errors** — 0 across all 8 pages.
- **Assets** — every `url()` in the stylesheet resolves to a file that exists.

Two notes on method, since both nearly produced a false result:

- The first delta measurement reported changes of 234 levels across 27% of the
  page. That was not the artwork. `scroll-behavior: smooth` meant the two runs
  had not finished scrolling to the same place, and the hero motes are placed
  with `Math.random()` on every load. With scrolling forced instant and the
  motes frozen, the real figure is 19–38 levels.
- The hit-test is only meaningful against a baseline. Read alone, "94 blocked"
  looks alarming; read against the unchanged stylesheet, it is identical.

---

## Rollback

```
cp assets/css/site.v5.css.bak assets/css/site.css
```

The three new SVGs become unreferenced but harmless. No markup or build changes
to revert.

---
---

# v7 — matching the reference screenshot

You ran `sambodhi-retreat-v6-full` and it did not look like your earlier build.
That is expected and my fault for shipping it as a runnable option: the full zip
is built from the **v5 source you uploaded**, which is older than the build in
your screenshot. This pass brings the full build in line with that screenshot,
and — more usefully — splits the decoration out so it can be applied to any
build without carrying these layout opinions with it.

## The real bug it exposed

The hero wordmark was sized off viewport **width** only:

```
font-size: clamp(2.4rem, 14.4vw, 14rem);
```

On a wide-but-short window (1920 x ~900 of content) that gives ~276px a line.
Two lines, plus the header, ornament, tagline and map link, exceed `100svh`, so
the centred flex column overflows. The tagline slid under the wave and the
bottom-pinned scroll cue ended up **above** it — which is exactly the stacking
you saw. Three things were wrong at once:

1. **No height constraint on the wordmark.** Now
   `clamp(2.4rem, min(14.4vw, 19.5svh), 14rem)` — it shrinks on short windows.
2. **The hero stack did not reserve room for the scroll cue.** The cue is
   absolutely placed at `bottom: curve-h + …`; the stack's bottom padding now
   clears it.
3. **`--hdr-h` was 150px for a two-tier header.** With the nav rail hidden the
   header is a single tier measuring 118px, so 32px was being reserved for
   nothing.

Measured with a bounding-box intersection test across 11 viewports
(1920x1080, 1920x900, 1600x860, 1456x816, 1440x900, 1366x768, 1280x720,
1024x640, 768x1024, 390x844, 375x667): **collisions 4 -> 0**.

## Matched to the screenshot

| | change |
|---|---|
| Navigation | Nav rail hidden at >=1100px; burger-only, as your build has it. All 8 pages remain reachable from the overlay menu — verified, none dropped. |
| Hamburger | Now a 56px circle with a hairline ring, translucent over the hero, solid green once the header sticks. |
| Hero tagline | "A sanctuary of peace, luxury and inner awakening" |
| Story block | Two-column split: "THE STORY" with a trailing gold rule and "A Place to Pause, / Reconnect & Renew" left, running copy right. Collapses to one column below 900px. |
| Map link | Stands down below 880px viewport height, where it was the thing colliding with the scroll cue. One line in `build.py` removes it everywhere. |

Two notes rather than silent decisions:

- **The hero photo is not a difference.** The hero cycles four slides; your two
  screenshots caught different ones.
- **"A sanctuary of peace, luxury and inner awakening" is the design comp's
  copy, not Sambodhi's own.** The earlier build deliberately kept the verified
  line for that reason. Your build uses the comp line, so this one now does too
  — but it is worth a deliberate decision rather than an inherited one.

## Which file to use

**`site-decoration.css` is the one to prefer.** It is standalone and purely
additive — it touches only `.wm` and the `.on-*` surfaces, and nothing else.
Tested by dropping it onto an unmodified v5 build: 14 sections decorated,
median 50.6% coverage, 0 overflow, 0 JS errors, and the header left exactly as
it was (nav rail still `flex`, burger still square). It cannot disturb a build
whose markup differs from the one it was written against.

The full v7 zip carries the layout changes above as well, so use it only if you
want those too.

## Re-verified after the changes

- Horizontal overflow: PASS, 8 pages x 8 widths
- Hero collisions: 0 across 11 viewports
- Coverage: 42 sections, min 25.9%, median 53.7%, none bare
- Click hit-test on index: 14, identical to the baseline stylesheet
- Overlay menu: opens, Escape closes, all 8 links present
- JS errors: 0

---
---

# v8 — cursor, split menu, hero entrance, image typography

## 1. The buttons were the bug, not the cursor

The cursor ring was already at `z-index: 1000`, above the header at 600, so it
was never behind the button. What was actually wrong:

```css
.btn--pill:hover{ background: currentColor; }   /* resolves to the HOVER color */
.hdr:not(.is-stuck) .btn--pill:hover{ color: var(--green); }
```

`currentColor` in `background` resolves against the element's **final** `color`,
which the next rule sets to green. So the pill filled green **and** painted its
label green — a solid dark blob with no text. Same fault on the phone button.
Both now set explicit background/text pairs. Verified: hover background
`rgb(255,255,255)`, text `rgb(23,41,30)` — no longer equal.

The ring itself is raised to `z-index: 999999` as asked, and given paired
shadows (dark outside, light inside) so a gold hairline reads on both the dark
header buttons and bright photography. Confirmed above every layer:
header 600, FAB 620, overlay 700, lightbox 900, page curtain 950.

## 2. Split-screen menu

Rebuilt as a two-column grid: deep-green navigation left, a stack of eight
photographs right, one per destination, crossfaded on hover. Each link carries
`data-menu-img`; pointer, keyboard focus and touch all drive the swap, and
leaving the list restores the shot for the page you are on. Hover gives the
word a gold hairline that grows from the left, a few pixels of travel, and an
arrow. Entrance staggers on `--i`.

The inline `transitionDelay` the old JS wrote applied on the way **out** as
well, so closing staggered as slowly as opening. Delay is now CSS, scoped to
`.is-open`, so the close is a clean fast reverse.

Below 900px the image panel moves behind the navigation under a heavier scrim
and the list centres.

Verified: 8 links, 8 shots, correct image on each of four hovers, restore on
leave, X closes, 0 JS errors.

## 3. Hero wordmark floats down

`translateY(-120px)` / `opacity 0` to `0` / `1` over 1.5s on
`cubic-bezier(.16,1,.3,1)` — expo out, which settles without overshoot. Traced
frame by frame: -120px at 0ms, -25px at 600ms, -1.8px at 1200ms, settled by
1600ms. Disabled under `prefers-reduced-motion`.

## 4 & 5. Image typography — the real fix was a halo, not a heavier stroke

A white hairline over a near-white photograph cannot be rescued by stroke
width; at any weight it is white on white. Three techniques were compared
directly:

- **plain stroke** — invisible on a bright image
- **`text-shadow`** — the shadow shows through the transparent fill and the
  letters read as **solid black**, which breaks the hollow requirement
- **stacked `drop-shadow()` filters** — each filters the previous result, so a
  tight dark halo builds up hugging the glyph edge. Hollow preserved.

Four stacked drop-shadows are now on `.outline`, plus a soft radial pool of
shade under the word only (`.overtitle::before`, anchored by variant), and
stroke raised to 1.2px / 1.8px desktop at 96% alpha.

Measured on a deliberately bright, busy stand-in photograph (mean luminance
229), local contrast at the lettering:

| | bright photo | dark photo |
|---|---|---|
| before | 53.8 levels | 206.6 |
| after | **205.9 levels** | 230.1 |

**3.8x on the bright case**, which is where the failure was. The rest of the
image moved only 12 -> 17 levels (bright) and 0 -> 3 (dark), so the picture
itself is essentially untouched — the brief's "do not over-darken" holds by
measurement, not by assertion.

Because this lives on `.outline` and `.overtitle`, it applies to every image
title at once — Bodhgaya, Rooms & Suites, Dining, Wellness, Experiences and the
hero — rather than patching the one section that was reported.

`.overtitle` also moved from `z-index: 3` to `5`.

## Re-verified

- Horizontal overflow: PASS, 8 pages x 8 widths
- Hero collisions: 0 across 11 viewports
- Decoration coverage: 42 sections, min 25.9%, median 53.7%
- z-order / pointer-events: PASS
- JS errors: 0
- Cursor visible over pill, phone, burger and the open menu
- Mobile: menu single column, custom cursor not created

## A measurement note

Two of my first three attempts to measure this were wrong and would have let a
non-fix through. The first compared the page against a baseline stylesheet
injected over the live one — but the baseline declares no `filter`, so the live
halo was never overridden and "before" and "after" came out identical. The
second scored a region dominated by the scrim rather than the glyphs. The
numbers above come from an isolated baseline copy of the whole site and a
local-contrast metric (9x9 max-min) restricted to the strongest edges.
