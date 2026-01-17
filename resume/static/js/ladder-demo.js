(function () {
  var state = {
    s1: false,
    s2: false,
    s3: false,
    s4: false,
    s5: false,
    s6: false
  };

  function updateLamp(container) {
    var lamp = container.querySelector('.lamp');
    var solved = (state.s1 && state.s2 && state.s3) || (state.s4 && state.s5) || state.s6;
    if (solved) {
      lamp.classList.add('lamp-on');
    } else {
      lamp.classList.remove('lamp-on');
    }

    var scope = document.querySelector('.scope-demo');
    if (scope) {
      scope.classList.toggle('locked', !solved);
    }
  }

  function updateContacts(container) {
    container.querySelectorAll('.contact').forEach(function (c) {
      var key = c.getAttribute('data-contact');
      if (state[key]) {
        c.classList.add('closed');
      } else {
        c.classList.remove('closed');
      }
    });
  }

  function toggleContact(container, key) {
    state[key] = !state[key];
    updateContacts(container);
    updateLamp(container);
  }

  function resetState(container) {
    Object.keys(state).forEach(function (k) {
      state[k] = false;
    });
    updateContacts(container);
    updateLamp(container);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var container = document.querySelector('.ladder-demo');
    if (!container) return;

    updateContacts(container);
    updateLamp(container);

    container.addEventListener('click', function (e) {
      var contact = e.target.closest('.contact');
      if (!contact) return;
      var key = contact.getAttribute('data-contact');
      if (!key) return;
      if (window.machineState && window.machineState !== 'running') return;
      toggleContact(container, key);
    });

    // expose reset hook for state machine
    window.resetLadderState = function () {
      resetState(container);
    };
  });
})();
