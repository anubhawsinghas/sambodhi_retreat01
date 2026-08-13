/* ==========================================================================
   SAMBODHI RETREAT — site.js
   All motion is opt-in via data attributes and every effect is gated on
   (a) prefers-reduced-motion and (b) a fine pointer, so touch devices get a
   calm, fast, fully functional site.
   ========================================================================== */
(function () {
  'use strict';

  var doc  = document;
  var html = doc.documentElement;
  var body = doc.body;

  var REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FINE    = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var DESKTOP = FINE && window.innerWidth > 1024 && !REDUCED;

  var $  = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };
  var lerp  = function (a, b, n) { return a + (b - a) * n; };

  /* ---------------------------------------------------------------- 1. LOAD */
  function markLoaded() {
    body.classList.add('is-loaded');
  }
  if (doc.readyState === 'complete') {
    setTimeout(markLoaded, 60);
  } else {
    window.addEventListener('load', function () { setTimeout(markLoaded, 60); });
    setTimeout(markLoaded, 1400); // never let a slow image hold the hero hostage
  }

  /* ------------------------------------------------- 2. IMAGE FALLBACKS */
  // A remote photo that 404s becomes a labelled, obviously-replaceable tile.
  doc.addEventListener('error', function (e) {
    var el = e.target;
    if (!el || el.tagName !== 'IMG') return;
    var host = el.parentElement;
    if (!host) return;
    host.classList.add('img-missing');
    if (!host.getAttribute('data-label')) {
      host.setAttribute('data-label', el.getAttribute('alt') || 'Image unavailable');
    }
  }, true);

  /* ------------------------------------------------------- 3. HEADER / MENU */
  var hdr    = $('.hdr');
  var menuBtn = $('.menu-btn');
  var ovl    = $('.ovl');

  // Transparent over the hero, solid once the page moves — the reference flips
  // at roughly the first fold, not immediately, so it doesn't flicker on nudge.
  if (hdr) {
    // On the home page the hero is pinned and taller than the window, so the
    // header has to stay transparent for the whole of that pin — flipping at
    // 60px would drop a cream bar over the photograph mid-reveal.
    var pinnedHero = $('[data-hero-reveal]');
    var stickAt = 60;
    var measureStick = function () {
      if (!pinnedHero) { stickAt = 60; return; }
      var pane = $('.hero__media', pinnedHero);
      var run  = pinnedHero.offsetHeight - (pane ? pane.offsetHeight : window.innerHeight);
      stickAt = Math.max(60, run - 6);
    };
    var onStick = function () {
      hdr.classList.toggle('is-stuck', window.scrollY > stickAt);
    };
    measureStick();
    onStick();
    window.addEventListener('scroll', onStick, { passive: true });
    window.addEventListener('resize', function () { measureStick(); onStick(); }, { passive: true });
    window.addEventListener('load', function () { measureStick(); onStick(); });
  }

  // The reference uses one overlay menu at EVERY breakpoint — no desktop navbar.
  if (menuBtn && ovl) {
    var ovlLinks = $$('.ovl__nav a', ovl);
    var ovlClose = $('.ovl__close', ovl);
    var setMenu = function (open) {
      ovl.classList.toggle('is-open', open);
      if (hdr) hdr.classList.toggle('is-stuck', open || window.scrollY > 60);
      body.classList.toggle('is-locked', open);
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      ovl.setAttribute('aria-hidden', open ? 'false' : 'true');
      if (open) {
        ovl.dispatchEvent(new CustomEvent('menu:open'));
        setTimeout(function () { ovlClose && ovlClose.focus(); }, 420);
      } else menuBtn.focus();
    };

    menuBtn.addEventListener('click', function () { setMenu(!ovl.classList.contains('is-open')); });
    if (ovlClose) ovlClose.addEventListener('click', function () { setMenu(false); });
    ovl.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && ovl.classList.contains('is-open')) setMenu(false);
    });
  }

  /* ------------------------------------------------ 4a. GALLERY INJECTION
     Runs before the reveal observer so injected tiles are observed too. */
  var IMG = window.SAMBODHI_IMAGES;

  // Homepage mosaic — a curated cut of the official gallery
  var mosaic = $('#homeMosaic');
  if (mosaic && IMG) {
    var pick = [0, 4, 9, 13, 6, 18, 21, 24];
    var mods = ['tile--h3', '', 'tile--w2 tile--h2', '', '', 'tile--h3', 'tile--w2 tile--h2', ''];
    mosaic.innerHTML = pick.map(function (n, i) {
      var src = IMG.gallery[n % IMG.gallery.length];
      return '<a class="tile ' + mods[i] + '" href="' + src + '" data-lightbox ' +
             'data-reveal="scale" aria-label="Open gallery image ' + (i + 1) + '">' +
             '<img src="' + src + '" alt="Sambodhi Retreat, Bodhgaya" loading="lazy" decoding="async"></a>';
    }).join('');
  }

  // Full gallery page
  var grid = $('#galleryGrid');
  if (grid && IMG) {
    grid.innerHTML = IMG.gallery.map(function (src, i) {
      return '<a class="tile" href="' + src + '" data-lightbox data-reveal="zoom" ' +
             'style="--d:' + ((i % 4) * 0.07) + 's" ' +
             'aria-label="Open image ' + (i + 1) + ' of ' + IMG.gallery.length + '">' +
             '<img src="' + src + '" alt="Sambodhi Retreat Bodhgaya — cottages, restaurant, reception and grounds" ' +
             'loading="lazy" decoding="async"></a>';
    }).join('');
  }

  /* -------------------------------------------------------- 4. REVEAL SYSTEM */
  var revealTargets = $$('[data-reveal], .eyebrow');

  if (!REDUCED && 'IntersectionObserver' in window) {
    // threshold MUST stay at 0: a clip-path'd element reports an
    // intersectionRatio of 0 even when fully on screen, so any threshold
    // above zero would leave every curtain reveal permanently hidden.
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0 });

    revealTargets.forEach(function (el) {
      var d = el.getAttribute('data-reveal-delay');
      if (d) el.style.setProperty('--d', (parseFloat(d) / 1000) + 's');
      io.observe(el);
    });

    // Safety net: if the viewport jumps (End key, anchor jump, restored scroll
    // position, or a starved main thread) an element can pass through between
    // observer deliveries and never report an intersection. Sweep anything that
    // is already at or above the fold and reveal it.
    var sweep = function () {
      var fold = window.innerHeight * 0.88;
      $$('[data-reveal]:not(.is-in)').forEach(function (el) {
        if (el.getBoundingClientRect().top < fold) {
          el.classList.add('is-in');
          io.unobserve(el);
        }
      });
    };
    var sweepQueued = false;
    var queueSweep = function () {
      if (sweepQueued) return;
      sweepQueued = true;
      requestAnimationFrame(function () { sweepQueued = false; sweep(); });
    };
    window.addEventListener('scroll', queueSweep, { passive: true });
    window.addEventListener('resize', queueSweep, { passive: true });
    window.addEventListener('load', queueSweep);

    // stagger children of any [data-stagger] container
    $$('[data-stagger]').forEach(function (group) {
      var step = parseFloat(group.getAttribute('data-stagger')) || 90;
      $$('[data-reveal]', group).forEach(function (child, i) {
        child.style.setProperty('--d', ((i * step) / 1000) + 's');
      });
    });
  } else {
    revealTargets.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ------------------------------------------------------ 5. SCROLL PARALLAX */
  var plx = $$('[data-parallax]');
  if (plx.length && !REDUCED) {
    var live = [];

    var measure = function () {
      plx.forEach(function (el) {
        var r = el.getBoundingClientRect();
        el._top = r.top + window.scrollY;
        el._h   = r.height;
        el._sp  = parseFloat(el.getAttribute('data-parallax')) || 0.3;
      });
    };

    var pio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          if (live.indexOf(en.target) === -1) live.push(en.target);
        } else {
          var i = live.indexOf(en.target);
          if (i > -1) live.splice(i, 1);
        }
      });
    }, { rootMargin: '18% 0px 18% 0px' });

    plx.forEach(function (el) { pio.observe(el); });

    var ticking = false;
    var run = function () {
      var vh = window.innerHeight;
      var sy = window.scrollY;
      for (var i = 0; i < live.length; i++) {
        var el  = live[i];
        var mid = el._top + el._h / 2 - sy;
        var rel = clamp((mid - vh / 2) / vh, -1.2, 1.2);
        // capped travel keeps the image inside its 118%-tall frame
        var y   = clamp(rel * el._sp * 100, -44, 44);
        el.style.transform = 'translate3d(0,' + y.toFixed(2) + 'px,0)';
      }
      ticking = false;
    };
    var request = function () {
      if (!ticking) { ticking = true; requestAnimationFrame(run); }
    };

    measure();
    request();
    window.addEventListener('scroll', request, { passive: true });
    window.addEventListener('resize', function () { measure(); request(); }, { passive: true });
    window.addEventListener('load', function () { measure(); request(); });
  }

  /* --------------------------------------------------- 6. HERO SCROLL REVEAL */
  // One number, --hero-p, running 0 -> 1 across the distance the pinned hero
  // stays stuck. The picture, the wordmark and the scroll cue all read from it
  // in CSS, so they can never fall out of step with one another or the scroll.
  var heroPin = $('[data-hero-reveal]');
  if (heroPin) {
    if (REDUCED) {
      heroPin.classList.add('is-static');
    } else {
      var hPane  = $('.hero__media', heroPin);
      var hRun   = 1;
      var hTop   = 0;
      var hRaf   = null;
      var hLast  = -1;

      var measureHero = function () {
        hTop = heroPin.getBoundingClientRect().top + window.scrollY;
        hRun = Math.max(1, heroPin.offsetHeight - (hPane ? hPane.offsetHeight : window.innerHeight));
      };
      var paintHero = function () {
        hRaf = null;
        var p = clamp((window.scrollY - hTop) / hRun, 0, 1);
        if (Math.abs(p - hLast) < 0.0004) return;
        hLast = p;
        heroPin.style.setProperty('--hero-p', p.toFixed(4));
      };
      var queueHero = function () {
        if (!hRaf) hRaf = requestAnimationFrame(paintHero);
      };

      measureHero();
      paintHero();
      window.addEventListener('scroll', queueHero, { passive: true });
      window.addEventListener('resize', function () { measureHero(); paintHero(); }, { passive: true });
      window.addEventListener('load',   function () { measureHero(); paintHero(); });
    }
  }

  /* ------------------------------------------------------- 6b. HERO SLIDESHOW */
  var slides = $$('.hero__slide');
  if (slides.length > 1 && !REDUCED) {
    var idx = 0;
    setInterval(function () {
      slides[idx].classList.remove('is-active');
      idx = (idx + 1) % slides.length;
      slides[idx].classList.add('is-active');
    }, 6400);
  }

  /* ------------------------------------------- 6c. SUITES & VILLAS BLOCKS */
  // Two jobs here, both scoped to .villa and deliberately kept off the
  // site-wide reveal system.
  //
  //   1. A REPLAYABLE entrance. The shared reveal fires once and unobserves,
  //      and its sweep re-reveals anything above the fold — so a block that
  //      reset itself would be re-revealed on the next frame. These blocks own
  //      [data-villa-in] instead, and reset when they are clear of the window
  //      so scrolling back up plays the motion again.
  //
  //   2. --villa-p, 0 -> 1 across the block's passage through the window,
  //      which CSS turns into the photograph's zoom-out and drift.
  var villaBlocks = $$('.villa');

  if (villaBlocks.length && !REDUCED) {
    var villaParts = $$('[data-villa-in]');
    var vPaint, vQueue;   // declared up here: vNear's callback calls vQueue

    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); return; }
        // Reset only once the part is genuinely clear of the window. Resetting
        // the moment it stops intersecting would let a small scroll near the
        // trigger line flicker it on and off.
        var r = en.boundingClientRect;
        if (r.bottom < 0 || r.top > window.innerHeight) {
          en.target.classList.remove('is-in');
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0 });

    villaParts.forEach(function (el) {
      var d = el.getAttribute('data-villa-delay');
      if (d) el.style.setProperty('--d', (parseFloat(d) / 1000) + 's');
      vio.observe(el);
    });

    // Only blocks near the window are worth measuring each frame.
    var vLive = [];
    var vNear = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var i = vLive.indexOf(en.target);
        if (en.isIntersecting) { if (i < 0) vLive.push(en.target); }
        else if (i > -1) { vLive.splice(i, 1); }
      });
      // Paint as soon as the live list changes. Observer callbacks are
      // delivered after the scroll handler that caused them, so without this a
      // block that becomes live on a jump — restored scroll position, anchor
      // link, deep link — keeps the default --villa-p until the reader happens
      // to scroll again, and then visibly snaps.
      vQueue();
    }, { rootMargin: '30% 0px 30% 0px', threshold: 0 });
    villaBlocks.forEach(function (v) { vNear.observe(v); });

    var vRaf = null;
    vPaint = function () {
      vRaf = null;
      var vh = window.innerHeight;
      for (var i = 0; i < vLive.length; i++) {
        var el = vLive[i];
        var r  = el.getBoundingClientRect();
        // 0 when the block is just below the fold, 1 once it has fully left
        // the top — so the zoom runs across the whole passage, not just the
        // part of it that happens to be on screen.
        var p = clamp((vh - r.top) / (vh + r.height), 0, 1);
        el.style.setProperty('--villa-p', p.toFixed(4));
      }
    };
    vQueue = function () { if (!vRaf) vRaf = requestAnimationFrame(vPaint); };

    vPaint();
    window.addEventListener('scroll', vQueue, { passive: true });
    window.addEventListener('resize', vQueue, { passive: true });
    window.addEventListener('load', vQueue);
  }

  /* --------------------------------------------------- 7. HERO MOUSE PARALLAX */
  var depthHost = $('[data-mouse-parallax]');
  if (depthHost && DESKTOP) {
    var layers = $$('[data-depth]', depthHost);
    var tX = 0, tY = 0, cX = 0, cY = 0, raf = null;

    depthHost.addEventListener('mousemove', function (e) {
      var r = depthHost.getBoundingClientRect();
      tX = ((e.clientX - r.left) / r.width  - 0.5) * 2;
      tY = ((e.clientY - r.top)  / r.height - 0.5) * 2;
      if (!raf) raf = requestAnimationFrame(step);
    });
    depthHost.addEventListener('mouseleave', function () { tX = 0; tY = 0; });

    function step() {
      cX = lerp(cX, tX, 0.06);
      cY = lerp(cY, tY, 0.06);
      layers.forEach(function (l) {
        var d = parseFloat(l.getAttribute('data-depth')) || 0;
        l.style.transform = 'translate3d(' + (-cX * d * 34).toFixed(2) + 'px,' +
                                             (-cY * d * 22).toFixed(2) + 'px,0)';
      });
      raf = (Math.abs(cX - tX) > 0.001 || Math.abs(cY - tY) > 0.001)
        ? requestAnimationFrame(step) : null;
    }
  }

  /* ------------------------------------------------------------- 8. 3D TILT */
  if (DESKTOP) {
    $$('.tilt').forEach(function (card) {
      var max = parseFloat(card.getAttribute('data-tilt-max')) || 4.5; // degrees
      var rect = null;

      card.addEventListener('mouseenter', function () { rect = card.getBoundingClientRect(); });
      card.addEventListener('mousemove', function (e) {
        if (!rect) rect = card.getBoundingClientRect();
        var px = (e.clientX - rect.left) / rect.width  - 0.5;
        var py = (e.clientY - rect.top)  / rect.height - 0.5;
        card.style.transform =
          'perspective(1000px) rotateY(' + (px * max * 2).toFixed(2) + 'deg) rotateX(' +
          (-py * max * 2).toFixed(2) + 'deg) translateZ(0)';
      });
      card.addEventListener('mouseleave', function () {
        rect = null;
        card.style.transform = '';
      });
    });
  }

  /* ------------------------------------------------------ 9. MAGNETIC BUTTONS */
  if (DESKTOP) {
    $$('.magnetic').forEach(function (btn) {
      var pull = parseFloat(btn.getAttribute('data-pull')) || 10;
      btn.addEventListener('mousemove', function (e) {
        var r = btn.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) / (r.width / 2);
        var y = (e.clientY - r.top - r.height / 2) / (r.height / 2);
        btn.style.transform = 'translate(' + (x * pull).toFixed(1) + 'px,' + (y * pull * 0.6).toFixed(1) + 'px)';
      });
      btn.addEventListener('mouseleave', function () { btn.style.transform = ''; });
    });
  }

  /* Custom cursor removed in v3 — the reference UI uses the native cursor. */

  /* ------------------------------------------------ 9b. SPLIT MENU PANEL */
  /* Moving down the navigation crossfades the photograph on the right.
     Pointer, keyboard focus and touch all drive it; leaving the list
     restores the shot for the page you are actually on.                   */
  (function () {
    var ovl = $('#ovl');
    if (!ovl) return;
    var links = $$('.ovl__nav a', ovl);
    var shots = $$('.ovl__shot', ovl);
    if (!links.length || !shots.length) return;

    var current = $('.ovl__shot.is-active', ovl) || shots[0];

    function show(src) {
      var next = null;
      for (var i = 0; i < shots.length; i++) {
        if (shots[i].getAttribute('data-for') === src) { next = shots[i]; break; }
      }
      if (!next || next === current) return;
      if (current) current.classList.remove('is-active');
      next.classList.add('is-active');
      current = next;
    }

    var restore = (function () {
      var here = null;
      for (var i = 0; i < links.length; i++) {
        if (links[i].hasAttribute('aria-current')) { here = links[i]; break; }
      }
      var src = (here || links[0]).getAttribute('data-menu-img');
      return function () { show(src); };
    })();

    links.forEach(function (a) {
      var src = a.getAttribute('data-menu-img');
      function on()  { show(src); a.classList.add('is-hot'); }
      function off() { a.classList.remove('is-hot'); }
      a.addEventListener('mouseenter', on);
      a.addEventListener('mouseleave', off);
      a.addEventListener('focus', on);
      a.addEventListener('blur', off);
      a.addEventListener('touchstart', on, { passive: true });
    });

    var nav = $('.ovl__nav', ovl);
    if (nav) nav.addEventListener('mouseleave', restore);

    /* preload so the first crossfade is not a blank frame */
    ovl.addEventListener('menu:open', function () {
      shots.forEach(function (s) {
        var m = /url\(["']?(.*?)["']?\)/.exec(s.style.backgroundImage || '');
        if (m && m[1]) { var im = new Image(); im.src = m[1]; }
      });
    });
  })();

  /* ------------------------------------------------------------ 10. CURSOR RING */
  if (DESKTOP) {
    var ring = doc.createElement('div');
    ring.className = 'cursor-ring';
    ring.innerHTML = '<span class="cursor-ring__label">View</span>';
    body.appendChild(ring);
    html.classList.add('has-ring');

    var mx = window.innerWidth / 2, my = window.innerHeight / 2, rx = mx, ry = my;
    doc.addEventListener('mousemove', function (e) { mx = e.clientX; my = e.clientY; });

    (function follow() {
      rx = lerp(rx, mx, 0.18);          // catches up smoothly, no visible lag
      ry = lerp(ry, my, 0.18);
      ring.style.transform = 'translate3d(' + rx.toFixed(2) + 'px,' + ry.toFixed(2) + 'px,0)';
      requestAnimationFrame(follow);
    })();

    doc.addEventListener('mouseover', function (e) {
      var media = e.target.closest('.tile, .frame, .rcard__media, .slide__media, .jcard__media, .tblock__media');
      var hot   = e.target.closest('a, button, input, textarea, select, [role="tab"]');
      ring.classList.toggle('is-media', !!media && !hot);
      ring.classList.toggle('is-hot', !media && !!hot);
    });
    doc.addEventListener('mouseleave', function () { html.classList.remove('has-ring'); });
    doc.addEventListener('mouseenter', function () { html.classList.add('has-ring'); });
  }

  /* ------------------------------------------------------- 11. FLOATING MOTES */
  var moteHost = $('.hero__motes');
  if (moteHost && !REDUCED) {
    for (var m = 0; m < 16; m++) {
      var s = doc.createElement('span');
      s.className = 'mote';
      s.style.left = (Math.random() * 100).toFixed(2) + '%';
      s.style.animationDuration = (16 + Math.random() * 20).toFixed(1) + 's';
      s.style.animationDelay = (-Math.random() * 26).toFixed(1) + 's';
      s.style.opacity = 0;
      var sz = (1.5 + Math.random() * 2.6).toFixed(1);
      s.style.width = sz + 'px';
      s.style.height = sz + 'px';
      moteHost.appendChild(s);
    }
  }

  /* ---------------------------------------------------------- 13. LIGHTBOX */
  var lbTriggers = $$('[data-lightbox]');
  if (lbTriggers.length) {
    var lb = doc.createElement('div');
    lb.className = 'lb';
    lb.setAttribute('role', 'dialog');
    lb.setAttribute('aria-modal', 'true');
    lb.setAttribute('aria-label', 'Image viewer');
    lb.innerHTML =
      '<img class="lb__img" alt="">' +
      '<button class="lb__btn lb__close" aria-label="Close viewer">' +
        '<svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="1.2"/></svg>' +
      '</button>' +
      '<button class="lb__btn lb__prev" aria-label="Previous image">' +
        '<svg width="16" height="12" viewBox="0 0 16 12" aria-hidden="true"><path d="M6 1L1 6l5 5M1 6h15" stroke="currentColor" stroke-width="1.2" fill="none"/></svg>' +
      '</button>' +
      '<button class="lb__btn lb__next" aria-label="Next image">' +
        '<svg width="16" height="12" viewBox="0 0 16 12" aria-hidden="true"><path d="M10 1l5 5-5 5M15 6H0" stroke="currentColor" stroke-width="1.2" fill="none"/></svg>' +
      '</button>' +
      '<span class="lb__count"></span>';
    body.appendChild(lb);

    var lbImg   = $('.lb__img', lb);
    var lbCount = $('.lb__count', lb);
    var list    = [];
    var cur     = 0;
    var lastFocus = null;

    function collect() {
      list = $$('[data-lightbox]');
    }

    function show(i) {
      collect();
      cur = (i + list.length) % list.length;
      var a = list[cur];
      lbImg.src = a.getAttribute('href');
      lbImg.alt = ($('img', a) && $('img', a).alt) || 'Sambodhi Retreat';
      lbCount.textContent = (cur + 1) + ' / ' + list.length;
    }

    function open(i) {
      lastFocus = doc.activeElement;
      show(i);
      lb.classList.add('is-open');
      body.classList.add('is-locked');
      $('.lb__close', lb).focus();
    }

    function close() {
      lb.classList.remove('is-open');
      body.classList.remove('is-locked');
      if (lastFocus) lastFocus.focus();
    }

    doc.addEventListener('click', function (e) {
      var t = e.target.closest('[data-lightbox]');
      if (!t) return;
      e.preventDefault();
      collect();
      open(list.indexOf(t));
    });

    $('.lb__close', lb).addEventListener('click', close);
    $('.lb__prev', lb).addEventListener('click', function () { show(cur - 1); });
    $('.lb__next', lb).addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });

    doc.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape')     close();
      if (e.key === 'ArrowRight') show(cur + 1);
      if (e.key === 'ArrowLeft')  show(cur - 1);
      if (e.key === 'Tab') { e.preventDefault(); $('.lb__close', lb).focus(); }
    });
  }

  /* ------------------------------------------------------------ 14. FILTERS */
  var filterBar = $('[data-filters]');
  if (filterBar) {
    var cards = $$('[data-type]');
    filterBar.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-filter]');
      if (!b) return;
      var f = b.getAttribute('data-filter');
      $$('button', filterBar).forEach(function (x) {
        x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
      });
      cards.forEach(function (c) {
        var match = (f === 'all') || c.getAttribute('data-type') === f;
        c.classList.toggle('is-hidden', !match);
      });
    });
  }

  /* --------------------------------------------------- 15. ENQUIRY FORM */
  // No backend is bundled with these static files, so the form opens the
  // visitor's mail client pre-filled and addressed to the resort. Swap the
  // handler for a POST to your own endpoint when one is available.
  var form = $('#enquiry');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var get = function (n) { var f = form.elements[n]; return f ? f.value.trim() : ''; };
      var name = (get('first') + ' ' + get('last')).trim();
      var subject = get('subject') || 'Enquiry from the Sambodhi Retreat website';
      var lines = [
        'Name: '  + name,
        'Email: ' + get('email'),
        'Phone: ' + get('phone'),
        '',
        get('message')
      ].join('\n');
      window.location.href = 'mailto:info@sambodhiretreat.com?subject=' +
        encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines);
      var note = $('#enquiryNote');
      if (note) note.textContent = 'Opening your mail app with this enquiry ready to send.';
    });
  }

  /* -------------------------------------------------- 16. PAGE TRANSITIONS */
  var fade = $('.page-fade');
  if (fade && !REDUCED) {
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { fade.classList.add('is-out'); });
    });

    doc.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a) return;
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#') return;
      if (a.target === '_blank' || a.hasAttribute('download') || a.hasAttribute('data-lightbox')) return;
      if (/^(mailto:|tel:|https?:)/i.test(href) && a.host !== window.location.host) return;

      e.preventDefault();
      fade.classList.remove('is-out');
      fade.classList.add('is-in');
      setTimeout(function () { window.location.href = href; }, 560);
    });

    // returning via the back button must not leave the curtain down
    window.addEventListener('pageshow', function () {
      fade.classList.remove('is-in');
      fade.classList.add('is-out');
    });
  } else if (fade) {
    fade.style.display = 'none';
  }

  /* -------------------------------------------------- 16b. ACCOMMODATION CAROUSEL */
  $$('.carousel').forEach(function (root) {
    var track = $('.carousel__track', root);
    var slides = $$('.slide', root);
    var tabs   = $$('.carousel__rail .carousel__tab', root);
    var dots   = $$('.carousel__dots button', root);
    var prev   = $('.carousel__prev', root);
    var next   = $('.carousel__next', root);
    if (!track || slides.length < 2) return;

    var i = 0;

    function go(n) {
      i = (n + slides.length) % slides.length;
      // width lives in CSS (--slide-w) so the desktop peek stays in one place
      track.style.setProperty('--i', i);
      tabs.forEach(function (t, k) { t.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
      dots.forEach(function (d, k) { d.setAttribute('aria-current', k === i ? 'true' : 'false'); });
      slides.forEach(function (sl, k) {
        sl.setAttribute('aria-hidden', k === i ? 'false' : 'true');
        $$('a, button', sl).forEach(function (f) {
          if (k === i) f.removeAttribute('tabindex'); else f.setAttribute('tabindex', '-1');
        });
      });
    }

    if (prev) prev.addEventListener('click', function () { go(i - 1); });
    if (next) next.addEventListener('click', function () { go(i + 1); });
    tabs.forEach(function (t, k) { t.addEventListener('click', function () { go(k); }); });
    dots.forEach(function (d, k) { d.addEventListener('click', function () { go(k); }); });

    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { go(i + 1); }
      if (e.key === 'ArrowLeft')  { go(i - 1); }
    });

    // touch swipe
    var x0 = null;
    root.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    root.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) go(dx < 0 ? i + 1 : i - 1);
      x0 = null;
    }, { passive: true });

    go(0);
  });

  /* ------------------------------------------------- 18. AMENITIES SLIDER */
  // One index drives three lists — background, caption, rail cell — so the
  // photograph, the words and the marked panel can never disagree about which
  // amenity is showing. Direction is published to CSS as --dir, which is what
  // makes an advance slide left and a step back slide right using one rule.
  //
  // The timer is owned by sync(), not by the click handler: it runs only while
  // the stage is on screen, the tab is visible, and the pointer is not resting
  // on the rail. Anything else — choosing, reading, another tab — and it holds.
  $$('[data-amenx]').forEach(function (stage) {
    var slides = $$('.amenx__slide', stage);
    var caps   = $$('.amenx__cap', stage);
    var cells  = $$('.amenx__cell', stage);
    var rail   = $('.amenx__cells', stage);
    var n = Math.min(slides.length, caps.length, cells.length);
    if (n < 2 || !rail) return;

    var DUR = parseInt(stage.getAttribute('data-amenx-interval'), 10) || 6400;
    stage.style.setProperty('--amenx-dur', DUR + 'ms');

    var i = 0, timer = null;
    var inView = false, resting = false;

    // Re-arm a CSS animation. Clearing the property, forcing a reflow and
    // handing it back is the only way to make an animation replay without
    // swapping the class that owns it.
    function rearm(el) {
      if (!el || REDUCED) return;
      el.style.animation = 'none';
      void el.offsetWidth;
      el.style.animation = '';
    }
    function rearmBar() { rearm(cells[i].querySelector('.amenx__prog')); }

    function show(next, dir) {
      next = (next % n + n) % n;
      if (next === i) return false;
      stage.style.setProperty('--dir', dir);

      var out = slides[i];
      out.classList.remove('is-active');
      out.classList.add('is-out');
      caps[i].classList.remove('is-active');
      cells[i].classList.remove('is-active');
      cells[i].setAttribute('aria-selected', 'false');
      cells[i].tabIndex = -1;

      // Strip .is-out once the outgoing picture has faded, so its reset back to
      // the entry pose happens at opacity 0 where nobody can see it. Timed per
      // element rather than on one shared handle, or a fast second click would
      // orphan the first slide at the exit pose.
      if (out._amx) clearTimeout(out._amx);
      out._amx = setTimeout(function () {
        out.classList.remove('is-out');
        out._amx = null;
      }, 1000);

      i = next;

      if (slides[i]._amx) { clearTimeout(slides[i]._amx); slides[i]._amx = null; }
      slides[i].classList.remove('is-out');
      slides[i].classList.add('is-active');
      caps[i].classList.add('is-active');
      cells[i].classList.add('is-active');
      cells[i].setAttribute('aria-selected', 'true');
      cells[i].tabIndex = 0;

      rearm(slides[i].querySelector('img'));   // fresh cinematic pass
      return true;
    }

    // Keep the live cell visible once the rail is a scroller (mobile).
    function follow() {
      if (rail.scrollWidth <= rail.clientWidth + 4) return;
      var c = cells[i];
      var x = Math.max(0, c.offsetLeft - (rail.clientWidth - c.offsetWidth) / 2);
      if (rail.scrollTo) rail.scrollTo({ left: x, behavior: REDUCED ? 'auto' : 'smooth' });
      else rail.scrollLeft = x;
    }

    function sync() {
      var run = inView && !resting && !doc.hidden && !REDUCED;
      stage.classList.toggle('is-held', !run && inView);
      if (run) {
        if (!timer) { rearmBar(); timer = setInterval(function () { select(i + 1, 1, false); }, DUR); }
      } else if (timer) {
        clearInterval(timer); timer = null;
      }
    }

    // restart: a reader's choice resets the clock from the slide they picked,
    // so they get a full interval to look at it. The automatic advance does
    // not, or the cadence would drift a frame later on every step.
    function select(next, dir, restart) {
      if (!show(next, dir)) rearmBar();
      follow();
      if (restart) { if (timer) { clearInterval(timer); timer = null; } sync(); }
    }

    cells.forEach(function (cell, k) {
      cell.addEventListener('click', function () { select(k, k >= i ? 1 : -1, true); });
    });

    rail.addEventListener('keydown', function (e) {
      var to = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') to = i + 1;
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') to = i - 1;
      else if (e.key === 'Home') to = 0;
      else if (e.key === 'End') to = n - 1;
      if (to === null) return;
      e.preventDefault();
      select(to, to > i ? 1 : -1, true);
      cells[i].focus();
    });

    // Hold while the reader is choosing or reading — and give keyboard users
    // the same hold, which is also the pause mechanism auto-advancing content
    // is meant to offer.
    if (FINE) {
      rail.addEventListener('mouseenter', function () { resting = true;  sync(); });
      rail.addEventListener('mouseleave', function () { resting = false; sync(); });
    }
    rail.addEventListener('focusin',  function () { resting = true;  sync(); });
    rail.addEventListener('focusout', function (e) {
      if (!rail.contains(e.relatedTarget)) { resting = false; sync(); }
    });

    // Swipe the picture. Touches that begin on the rail belong to the rail,
    // which does its own horizontal scrolling.
    var x0 = null, y0 = null;
    stage.addEventListener('touchstart', function (e) {
      if (e.target.closest && e.target.closest('.amenx__cells')) { x0 = null; return; }
      x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
    }, { passive: true });
    stage.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      var dy = e.changedTouches[0].clientY - y0;
      if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy)) {
        var d = dx < 0 ? 1 : -1;
        select(i + d, d, true);
      }
      x0 = y0 = null;
    }, { passive: true });

    doc.addEventListener('visibilitychange', sync);

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { inView = en.isIntersecting; });
        sync();
      }, { threshold: 0.12 }).observe(stage);
    } else {
      inView = true; sync();
    }
  });

  /* --------------------------------------------------- 19. NEWSLETTER FORM */
  // There is no backend to post to, so the form's job is to be honest about
  // what it can and cannot do: validate the address, require the consent box
  // the brief asks for, and say so in a live region rather than silently
  // reloading the page.
  $$('#newsletter').forEach(function (form) {
    var note = $('.news__note', form.parentNode);
    var email = $('#news-email', form);
    var consent = $('#news-consent', form.parentNode);

    var say = function (msg, ok) {
      if (!note) return;
      note.textContent = msg;
      if (ok) note.setAttribute('data-ok', ''); else note.removeAttribute('data-ok');
    };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = (email && email.value || '').trim();
      if (!v || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
        say('Please enter a valid email address.');
        if (email) email.focus();
        return;
      }
      if (consent && !consent.checked) {
        say('Please accept the Privacy Policy to subscribe.');
        consent.focus();
        return;
      }
      say('Thank you — we will be in touch at ' + v + '.', true);
      form.reset();
      if (consent) consent.checked = false;
    });

    if (consent) consent.addEventListener('change', function () {
      if (consent.checked && note && !note.hasAttribute('data-ok')) say('');
    });
  });

  /* ---------------------------------------------------------- 17. YEAR STAMP */
  $$('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
