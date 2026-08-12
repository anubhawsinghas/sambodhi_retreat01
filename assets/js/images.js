/* ==========================================================================
   SAMBODHI RETREAT — images.js
   SINGLE SOURCE OF TRUTH FOR IMAGERY.

   Every photograph on this site is an authentic Sambodhi Retreat image served
   from the official domain. To move to self-hosted files, change BASE below to
   your own path (e.g. "assets/img/") and keep the filenames, or replace the
   individual entries.

   Any image that fails to load degrades to a labelled placeholder tile rather
   than a broken icon (see .frame.img-missing in site.css and the loader in
   site.js) — so a missing file is visible and replaceable, never silent.
   ========================================================================== */

(function (root) {
  'use strict';

  var BASE = 'https://www.sambodhiretreat.org/images/';

  var IMAGES = {
    base: BASE,

    /* --- Hero / atmosphere ------------------------------------------------ */
    hero: [
      BASE + 'Homepage_Resort_INDEX/top-slider-img8.jpg',
      BASE + 'Homepage_Resort_INDEX/top-slider-img3.jpg',
      BASE + 'Homepage_Resort_INDEX/top-slider-img7.jpg',
      BASE + 'Homepage_Resort_INDEX/top-slider-img1a.jpg'
    ],

    pageHero: {
      accommodations: BASE + 'Homepage_Resort_INDEX/top-slider-img11.jpg',
      banquet:        BASE + 'promotions/1.jpg',
      events:         BASE + 'Gallery/top-post-img3.jpg',
      dining:         BASE + 'dining/restaurant1.jpg',
      gallery:        BASE + 'Homepage_Resort_INDEX/top-slider-img10.jpg',
      blog:           BASE + 'Gallery/Top-5-Places-in-Bodh-Gaya.jpg',
      contact:        BASE + 'Homepage_Resort_INDEX/top-slider-img5.jpg'
    },

    /* --- Property / editorial -------------------------------------------- */
    estate:   BASE + 'Homepage_Resort_INDEX/top-slider-img13.jpg',
    grounds:  BASE + 'Homepage_Resort_INDEX/learn-img1.jpg',
    grounds2: BASE + 'Homepage_Resort_INDEX/learn-img2.jpg',
    video:    BASE + 'Homepage_Resort_INDEX/video.jpg',
    pool:     BASE + 'Homepage_Resort_INDEX/top-slider-img11.jpg',

    /* --- Accommodation ---------------------------------------------------- */
    rooms: {
      igloo:     BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-igloo-1.jpg',
      woodland:  BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-woodland-cottages-1.jpg',
      greenCave: BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-green-caves-1.jpg',
      timber:    BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-timber-cottages-1.jpg',
      pyramid:   BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-pyramid-cottages-1.jpg',
      lotus:     BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-lotus-1.jpg',
      buddha:    BASE + 'homePage-Villas/riverside.jpg'
    },
    roomsAlt: {
      igloo:     BASE + 'homePage-Villas/igloo-house.jpg',
      woodland:  BASE + 'homePage-Villas/woodland.jpg',
      greenCave: BASE + 'homePage-Villas/green-cave.jpg',
      timber:    BASE + 'homePage-Villas/timber.jpg',
      pyramid:   BASE + 'homePage-Villas/pyramid.jpg',
      lotus:     BASE + 'homePage-Villas/lotus.jpg'
    },

    /* --- Dining ----------------------------------------------------------- */
    dining: [
      BASE + 'dining/restaurant1.jpg',
      BASE + 'dining/restaurant2.jpg',
      BASE + 'dining/restaurant3.jpg',
      BASE + 'Homepage_Resort_INDEX/home-gal-img6.jpg'
    ],

    /* --- Banquet & events ------------------------------------------------- */
    banquet: {
      convention1: BASE + 'promotions/1.jpg',
      convention2: BASE + 'promotions/2.jpg',
      conference1: BASE + 'promotions/5.jpg',
      conference2: BASE + 'promotions/6.jpg'
    },
    events: {
      sights:    BASE + 'Gallery/top-post-img1.jpg',
      candle:    BASE + 'Gallery/top-post-img2.jpg',
      wedding:   BASE + 'Gallery/top-post-img3.jpg',
      honeymoon: BASE + 'Gallery/top-post-img4.jpg',
      candleLg:  BASE + 'Gallery/main-blog-img9.jpg',
      floating:  BASE + 'Gallery/main-blog-img1.jpg',
      venue:     BASE + 'Gallery/main-blog-img2.jpg'
    },

    /* --- Destinations ----------------------------------------------------- */
    destinations: {
      bodhgaya: BASE + 'Homepage_Resort_INDEX/top-slider-img7.jpg',
      dhanbad:  BASE + 'HomePage-Villas/budhha-heights.jpg'
    },

    /* --- Journal ---------------------------------------------------------- */
    journal: {
      wedding:   BASE + 'Gallery/Make-Wedding-Special-at-Sambodhi-Retreat.jpg',
      organic:   BASE + 'Gallery/Top-7-Organic-Foods-in-Sambodhi-Retreat.jpg',
      places:    BASE + 'Gallery/Top-5-Places-in-Bodh-Gaya.jpg',
      family:    BASE + 'Gallery/Top-Family-Events-Organized-in-the-Best-Luxury-Family-Hotels-in-Bodhgaya-Bihar.PNG',
      activity:  BASE + 'Gallery/What-Kind-of-Activities-Can-Guests-Enjoy-in-Top-Luxury-Resorts-in-Bodh-Gaya-Bihar.PNG',
      oneNight:  BASE + 'Gallery/One-Night-Stay-in-A-Luxury-Hotel-in-Bodh-Gaya-Bihar.PNG',
      couples:   BASE + 'Gallery/blog1-19-feb.jpg',
      anniv:     BASE + 'Gallery/blog3-19-feb.jpg',
      expect:    BASE + 'Gallery/blog4-19feb.jpg',
      romantic:  BASE + 'Gallery/blog2-19-feb.jpg',
      cuisine:   BASE + 'Gallery/Unveiling.jpg',
      luxury:    BASE + 'Gallery/unspral.jpg',
      recreation:BASE + 'Gallery/blog-3sam.jpg',
      comfort:   BASE + 'Gallery/blog-4sam.jpg',
      holi:      BASE + 'Gallery/Hotels-in-Bodhgaya-Bihar-Bodh-gayasambodhi-resort1.jpeg'
    },

    /* --- Gallery (27 official frames) ------------------------------------- */
    gallery: (function () {
      var out = [];
      for (var i = 1; i <= 27; i++) out.push(BASE + 'gallery/' + i + '.jpg');
      return out;
    })()
  };

  root.SAMBODHI_IMAGES = IMAGES;
})(window);
