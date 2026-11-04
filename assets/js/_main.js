/* ==========================================================================
   jQuery plugin settings and other scripts
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {
  fitvids();

  // The header scrolls with the page, so anchors need no fixed-header offset.
  $('a').smoothScroll({ offset: 0 });

  // add lightbox class to all image links
  $("a[href$='.jpg'],a[href$='.jpeg'],a[href$='.JPG'],a[href$='.png'],a[href$='.gif']").addClass("image-popup");

});
