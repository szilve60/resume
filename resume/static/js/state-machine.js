(function () {
  var current = 'idle';
  var labels = {
    idle: 'IDLE',
    running: 'RUNNING',
    stopped: 'STOPPED'
  };

  function setState(next) {
    current = next;
    window.machineState = current;
    var label = document.getElementById('state-label');
    var leds = document.querySelectorAll('.state-led');
    leds.forEach(function (led) {
      led.classList.toggle('active', led.getAttribute('data-state') === current);
    });
    if (label) label.textContent = labels[current] || current.toUpperCase();

    // When reset to idle, clear ladder contacts and lamp
    if (current === 'idle') {
      document.querySelectorAll('.ladder-demo .contact').forEach(function (c) {
        c.classList.remove('closed');
        c.dataset.manual = 'false';
      });
      var lamp = document.querySelector('.ladder-demo .lamp');
      if (lamp) lamp.classList.remove('lamp-on');
      // reset ladder internal state if exposed
      if (window.resetLadderState) window.resetLadderState();
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    var container = document.querySelector('.state-demo');
    if (!container) return;

    container.addEventListener('click', function (e) {
      var btn = e.target.closest('button[data-action]');
      if (!btn) return;
      var action = btn.getAttribute('data-action');
      if (action === 'start') setState('running');
      if (action === 'stop') setState('stopped');
      if (action === 'reset') setState('idle');
    });

    setState('idle');
  });
})();
