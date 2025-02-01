/*
* Greedy Navigation
*
* http://codepen.io/lukejacksonn/pen/PwmwWV
*
*/

const $nav = $('#site-nav');
const $btn = $('#site-nav button');
const $vlinks = $('#site-nav .visible-links');
const $hlinks = $('#site-nav .hidden-links');

let breaks = [];

function calculateAvailableSpace() {
  return $btn.hasClass('hidden') ? $nav.width() : $nav.width() - $btn.width() - 30
}

function updateNav() {

  let availableSpace = calculateAvailableSpace();

  // The visible list is overflowing the nav
  if ($vlinks.width() > availableSpace) {

    while ($vlinks.width() > availableSpace && $vlinks.children('*:not(.masthead__menu-item--lg)').length > 0) {

      // Record the width of the list
      breaks.push($vlinks.width());

      // Move item to the hidden list
      $vlinks.children('*:not(.masthead__menu-item--lg)').last().prependTo($hlinks);

      availableSpace = $btn.hasClass('hidden') ? $nav.width() : $nav.width() - $btn.width() - 30;
    }

    // Show the dropdown btn
    if ($btn.hasClass('hidden')) {
      $btn.removeClass('hidden');
    }

    // The visible list is not overflowing
  } else {

    // There is space for another item in the nav
    while (breaks.length > 0 && availableSpace > breaks[breaks.length - 1]) {
      // Move the item to the visible list
      $hlinks.children().first().appendTo($vlinks);
      breaks.pop();
    }

    // Hide the dropdown btn if hidden list is empty
    if (breaks.length < 1) {
      $btn.addClass('hidden');
      $hlinks.addClass('hidden');
    }
  }

  // Keep counter updated
  $btn.attr("count", breaks.length);
}



// Window listeners
$(window).on('resize', () => {
  updateNav();
});
screen.orientation.addEventListener("change", () => {
  updateNav();
});


$btn.on('click', (event) => {
  event.preventDefault();
  $hlinks.toggleClass('hidden');
  $btn.toggleClass('close');
});

$(document).on("click", (event) => {
  if (!$(event.target).closest($btn).length) {
    $hlinks.addClass('hidden');
    $btn.removeClass('close');
  }
});

updateNav();