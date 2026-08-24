/* Platform filter for /apps. Progressive: without JS every app is visible,
   which is why the chips are only wired up once this runs. */
(function () {
  var grid = document.getElementById('grid');
  if (!grid) return;
  var cards = Array.prototype.slice.call(grid.querySelectorAll('.app-card'));
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var count = document.getElementById('count');
  var empty = document.getElementById('empty');

  function apply(filter, push) {
    var shown = 0;
    cards.forEach(function (c) {
      var ok = filter === 'all' ||
               c.dataset.platforms.split(',').indexOf(filter) !== -1;
      c.hidden = !ok;
      if (ok) shown++;
    });
    chips.forEach(function (b) {
      var on = b.dataset.filter === filter;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    if (empty) empty.hidden = shown !== 0;
    if (count) {
      count.textContent = shown === cards.length
        ? shown + ' apps'
        : shown + ' of ' + cards.length + ' apps';
    }
    if (push) {
      history.replaceState(null, '',
        filter === 'all' ? location.pathname : location.pathname + '#' + filter);
    }
  }

  chips.forEach(function (b) {
    b.addEventListener('click', function () { apply(b.dataset.filter, true); });
  });

  // A shared link like /apps/#Mac should open already filtered.
  var initial = decodeURIComponent((location.hash || '').replace('#', '')) || 'all';
  if (!chips.some(function (b) { return b.dataset.filter === initial; })) initial = 'all';
  apply(initial, false);
})();
