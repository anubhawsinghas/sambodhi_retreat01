BOTANICAL DECORATION ADD-ON  --  Sambodhi Retreat
=================================================

Purely additive. Restyles nothing except the decorative watermark layer, so it
is safe on any build of the markup.

INSTALL (4 files, 1 line of HTML)

1. Copy in, keeping these paths:
       assets/css/site-decoration.css
       assets/img/wm-bloom.svg
       assets/img/wm-branch.svg
       assets/img/wm-vine.svg

2. Add ONE line after the existing stylesheet in each page:
       <link rel="stylesheet" href="assets/css/site.css">
       <link rel="stylesheet" href="assets/css/site-decoration.css">   <-- add

   (Or paste its contents onto the end of your site.css and skip step 2.)

TOUCHES ONLY:  .wm   and   .on-white / .on-sage / .on-green
NOT the header, hero, menu, cursor, typography, forms or booking.

NOTE: this add-on carries the botanical decoration ONLY. The cursor fix, split
menu, hero entrance animation and image-typography contrast are in the full
build -- they need markup and script changes and cannot ship as a drop-in
stylesheet.

TUNING: opacity lives at the top of the layer (.085 cream / .115 sage / .075
green). make_botanicals.py regenerates the three SVGs.

UNINSTALL: delete the one <link> line.
