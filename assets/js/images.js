/* ==========================================================================
   SAMBODHI RETREAT — images.js
   SINGLE SOURCE OF TRUTH FOR IMAGERY.

   All website images are loaded from the local "new_img/" directory.

   IMPORTANT:
   - Folder name: new_img
   - Gallery folder name: gallary
   - Keep file/folder names exactly the same on the server.
   ========================================================================== */

(function (root) {
  'use strict';

  /* ------------------------------------------------------------------------
     BASE IMAGE DIRECTORY
     ------------------------------------------------------------------------ */
  var BASE = 'new_img/';

  var IMAGES = {

    /* ----------------------------------------------------------------------
       Base
       ---------------------------------------------------------------------- */
    base: BASE,


    /* ----------------------------------------------------------------------
       Hero / Main Slider
       ---------------------------------------------------------------------- */
    hero: [
      BASE + 'slider1.png',
      BASE + 'slider3.png',
      BASE + 'slider2.png',
      BASE + 'slider4.png'
    ],


    /* ----------------------------------------------------------------------
       Page Hero Images
       ---------------------------------------------------------------------- */
    pageHero: {
      accommodations: BASE + 'slider4.png',
      banquet:        BASE + 'banquet1.png',
      events:         BASE + 'event3.png',
      dining:         BASE + 'dining1.png',
      gallery:        BASE + 'gallery10.png',
      blog:           BASE + 'blog.png',
      contact:        BASE + 'contact.png'
    },


    /* ----------------------------------------------------------------------
       Property / Editorial
       ---------------------------------------------------------------------- */
    estate:
      BASE + 'Homepage_Resort_INDEX/top-slider-img13.jpg',

    grounds:
      BASE + 'Homepage_Resort_INDEX/learn-img1.jpg',

    grounds2:
      BASE + 'Homepage_Resort_INDEX/learn-img2.jpg',

    video:
      BASE + 'Homepage_Resort_INDEX/video.jpg',

    pool:
      BASE + 'Homepage_Resort_INDEX/top-slider-img11.jpg',


    /* ----------------------------------------------------------------------
       Accommodation
       ---------------------------------------------------------------------- */
    rooms: {

      igloo:
        BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-igloo-1.jpg',

      woodland:
        BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-woodland-cottages-1.jpg',

      greenCave:
        BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-green-caves-1.jpg',

      timber:
        BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-timber-cottages-1.jpg',

      pyramid:
        BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-pyramid-cottages-1.jpg',

      lotus:
        BASE + 'rooms-col1/sambodhi-retreat-bodhgaya-lotus-1.jpg',

      buddha:
        BASE + 'homePage-Villas/riverside.jpg'
    },


    /* ----------------------------------------------------------------------
       Accommodation Alternate Images
       ---------------------------------------------------------------------- */
    roomsAlt: {

      igloo:
        BASE + 'homePage-Villas/igloo-house.jpg',

      woodland:
        BASE + 'homePage-Villas/woodland.jpg',

      greenCave:
        BASE + 'homePage-Villas/green-cave.jpg',

      timber:
        BASE + 'homePage-Villas/timber.jpg',

      pyramid:
        BASE + 'homePage-Villas/pyramid.jpg',

      lotus:
        BASE + 'homePage-Villas/lotus.jpg'
    },


    /* ----------------------------------------------------------------------
       Dining
       ---------------------------------------------------------------------- */
    dining: [

      BASE + 'dining/restaurant1.jpg',

      BASE + 'dining/restaurant2.jpg',

      BASE + 'dining/restaurant3.jpg',

      BASE + 'Homepage_Resort_INDEX/home-gal-img6.jpg'
    ],


    /* ----------------------------------------------------------------------
       Banquet
       ---------------------------------------------------------------------- */
    banquet: {

      convention1:
        BASE + 'promotions/1.jpg',

      convention2:
        BASE + 'promotions/2.jpg',

      conference1:
        BASE + 'promotions/5.jpg',

      conference2:
        BASE + 'promotions/6.jpg'
    },


    /* ----------------------------------------------------------------------
       Events
       ---------------------------------------------------------------------- */
    events: {

      sights:
        BASE + 'Gallery/top-post-img1.jpg',

      candle:
        BASE + 'Gallery/top-post-img2.jpg',

      wedding:
        BASE + 'Gallery/top-post-img3.jpg',

      honeymoon:
        BASE + 'Gallery/top-post-img4.jpg',

      candleLg:
        BASE + 'Gallery/main-blog-img9.jpg',

      floating:
        BASE + 'Gallery/main-blog-img1.jpg',

      venue:
        BASE + 'Gallery/main-blog-img2.jpg'
    },


    /* ----------------------------------------------------------------------
       Destinations
       ---------------------------------------------------------------------- */
    destinations: {

      bodhgaya:
        BASE + 'Homepage_Resort_INDEX/top-slider-img7.jpg',

      dhanbad:
        BASE + 'HomePage-Villas/budhha-heights.jpg'
    },


    /* ----------------------------------------------------------------------
       Journal / Blog
       ---------------------------------------------------------------------- */
    journal: {

      wedding:
        BASE + 'Gallery/Make-Wedding-Special-at-Sambodhi-Retreat.jpg',

      organic:
        BASE + 'Gallery/Top-7-Organic-Foods-in-Sambodhi-Retreat.jpg',

      places:
        BASE + 'Gallery/Top-5-Places-in-Bodh-Gaya.jpg',

      family:
        BASE + 'Gallery/Top-Family-Events-Organized-in-the-Best-Luxury-Family-Hotels-in-Bodhgaya-Bihar.PNG',

      activity:
        BASE + 'Gallery/What-Kind-of-Activities-Can-Guests-Enjoy-in-Top-Luxury-Resorts-in-Bodh-Gaya-Bihar.PNG',

      oneNight:
        BASE + 'Gallery/One-Night-Stay-in-A-Luxury-Hotel-in-Bodh-Gaya-Bihar.PNG',

      couples:
        BASE + 'Gallery/blog1-19-feb.jpg',

      anniv:
        BASE + 'Gallery/blog3-19-feb.jpg',

      expect:
        BASE + 'Gallery/blog4-19feb.jpg',

      romantic:
        BASE + 'Gallery/blog2-19-feb.jpg',

      cuisine:
        BASE + 'Gallery/Unveiling.jpg',

      luxury:
        BASE + 'Gallery/unspral.jpg',

      recreation:
        BASE + 'Gallery/blog-3sam.jpg',

      comfort:
        BASE + 'Gallery/blog-4sam.jpg',

      holi:
        BASE + 'Gallery/Hotels-in-Bodhgaya-Bihar-Bodh-gayasambodhi-resort1.jpeg'
    },


    /* ----------------------------------------------------------------------
       Gallery — 27 Images
       IMPORTANT: Folder is "gallary" as used by your current HTML.
       ---------------------------------------------------------------------- */
    gallery: (function () {

      var out = [];

      for (var i = 1; i <= 27; i++) {

        out.push(
          BASE + 'gallary/' + i + '.jpg'
        );

      }

      return out;

    })()

  };


  /* ------------------------------------------------------------------------
     Make images globally available
     ------------------------------------------------------------------------ */
  root.SAMBODHI_IMAGES = IMAGES;

})(window);