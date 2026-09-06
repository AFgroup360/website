/* Drag and drop onto the checklist, and the filename once one is chosen.
   Everything works without this file; it only makes the drop area live. */
(function () {
  'use strict';
  document.querySelectorAll('.portal-drop').forEach(function (drop) {
    var input = drop.querySelector('.portal-drop__input');
    var label = drop.querySelector('.portal-drop__label');
    if (!input || !label) return;
    var original = label.innerHTML;

    ['dragenter', 'dragover'].forEach(function (t) {
      drop.addEventListener(t, function (e) { e.preventDefault(); drop.classList.add('is-over'); });
    });
    ['dragleave', 'drop'].forEach(function (t) {
      drop.addEventListener(t, function () { drop.classList.remove('is-over'); });
    });
    drop.addEventListener('drop', function (e) {
      e.preventDefault();
      if (e.dataTransfer && e.dataTransfer.files.length) {
        input.files = e.dataTransfer.files;
        input.dispatchEvent(new Event('change'));
      }
    });
    input.addEventListener('change', function () {
      label.innerHTML = input.files.length
        ? '<strong>' + input.files[0].name.replace(/</g, '&lt;') + '</strong><span>Ready to upload</span>'
        : original;
    });
  });
})();
