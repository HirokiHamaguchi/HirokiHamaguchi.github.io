/* ==========================================================================
   jQuery plugin settings and other scripts
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function () {
  // These should be the same as the settings in _variables.scss
  scssLarge = 925; // pixels


  // FitVids init
  fitvids();

  // Follow menu drop down
  const $btn = $(".author__urls-wrapper button");
  $btn.on("click", function (event) {
    event.stopPropagation();
    $(".author__urls").fadeToggle("fast");
    $btn.toggleClass("open");
  });

  // Close follow menu on click outside of ".author__urls-wrapper button"
  $(document).on("click", function (event) {
    if ($btn.hasClass("open") && $(event.target).closest(".author__urls-wrapper").length === 0) {
      $(".author__urls").fadeOut("fast");
      $btn.removeClass("open");
    }
  });

  // Restore the follow menu if toggled on a window resize
  jQuery(window).on('resize', function () {
    if ($('.author__urls.social-icons').css('display') == 'none' && $(window).width() >= scssLarge) {
      $(".author__urls").css('display', 'block')
    }
  });

  // init smooth scroll, this needs to be slightly more than then fixed masthead height
  $("a").smoothScroll({ offset: -65 });

  // add lightbox class to all image links
  $("a[href$='.jpg'],a[href$='.jpeg'],a[href$='.JPG'],a[href$='.png'],a[href$='.gif']").addClass("image-popup");

});
