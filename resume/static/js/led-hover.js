(function () {
  function initLedHover() {
    var svgObject = document.getElementById('schematic-object');
    if (!svgObject || !svgObject.contentDocument) return;

    var svgDoc = svgObject.contentDocument;
    var leds = svgDoc.querySelectorAll('.led');
    if (!leds.length) return;

    leds.forEach(function (led) {
      led.addEventListener('mouseenter', function () {
        led.classList.add('led-active');
      });
      led.addEventListener('mouseleave', function () {
        led.classList.remove('led-active');
      });
      // touch fallback
      led.addEventListener('touchstart', function () {
        led.classList.add('led-active');
      });
      led.addEventListener('touchend', function () {
        led.classList.remove('led-active');
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    var svgObject = document.getElementById('schematic-object');
    if (!svgObject) return;
    // Wait for the SVG to load
    svgObject.addEventListener('load', initLedHover);
  });
})();
