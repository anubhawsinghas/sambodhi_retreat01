# Sambodhi Retreat — Website

The marketing website for **Sambodhi Retreat**, a resort in Bodhgaya, Bihar,
India. The site presents the property's rooms, dining, event and banquet
spaces, and photo gallery, and links out to the live booking engine.

A live reference of the property can be found at
[sambodhiretreat.org](https://www.sambodhiretreat.org).

## Overview

- **Type:** Static, multi-page HTML site (no server-side runtime, no framework)
- **Pages:** Home, Accommodations, Banquet Halls, Event Venue, Dining, Gallery,
  Blog, Contact — 8 pages in total, sharing one page shell
- **Generation:** All pages are generated from a single Python build script
  rather than hand-edited HTML, so the header, footer, nav, and shared markup
  stay consistent across every page
- **Booking:** The "Book" call-to-action across the site links to the resort's
  hosted booking engine (IPMS247); this repo does not implement booking logic

## Project structure

```
sambodhi_retreat01/
├── index.html               Home page
├── accommodations.html      Rooms & suites
├── banquet-halls.html       Banquet hall listings
├── event-venue.html         Event venue / weddings
├── dining.html               Dining & restaurant
├── gallery.html               Photo gallery
├── blog.html                    Journal / stories
├── contact.html               Contact & location
│
├── build.py                   Generates all 8 HTML pages from shared components
├── CHANGELOG.md                Version history and build notes
│
├── assets/
│   ├── css/
│   │   ├── site.css              Core stylesheet
│   │   └── site-decoration.css   Decorative/ornamental styles (watermarks, curves)
│   ├── js/
│   │   ├── site.js               Site interactivity (nav, carousel, forms, reveals)
│   │   └── images.js             Image loading / gallery behaviour
│   └── img/                       Logo and original SVG botanical watermark artwork
│
├── New_img/                   Photography used across the site
│
└── tools/
    └── make_botanicals.py     Generates the original SVG watermark artwork in assets/img/
```

## Getting started

The site is static, so no build step is required to view it. To preview
locally:

```bash
# from the project root
python3 -m http.server 8000
```

Then open `http://localhost:8000` in a browser.

### Rebuilding the pages

The HTML files are generated output — edit `build.py`, not the `.html` files
directly, so changes aren't lost on the next build:

```bash
python3 build.py
```

This regenerates all 8 pages from the shared shell, nav, header, and footer
defined in `build.py`.

### Regenerating watermark artwork

The botanical line-art watermarks in `assets/img/` (`wm-bloom.svg`,
`wm-branch.svg`, `wm-vine.svg`) are procedurally generated:

```bash
python3 tools/make_botanicals.py
```

## Tech stack

- Plain HTML5, CSS3, and vanilla JavaScript — no build tooling or package
  manager required to run the site
- Python 3 (standard library only) for page generation and watermark artwork
- Google Maps embed for the location map on Contact
- IPMS247 for the external booking engine

## Browser support notes

The site targets modern evergreen browsers and includes:
- Responsive layouts tested from 320px to 1920px viewport widths
- `prefers-reduced-motion` support (scroll reveals and marquee respect it)
- A text-stroke fallback for the outlined display type on engines that don't
  support `-webkit-text-stroke`

## Changelog

See [`CHANGELOG.md`](./CHANGELOG.md) for the detailed version history,
including design decisions and notes from each revision of the UI.

## License

All content, photography, and copy belong to Sambodhi Retreat. No license is
granted for reuse outside this project.
