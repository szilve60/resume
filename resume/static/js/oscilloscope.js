(function () {
  function drawGrid(ctx, w, h) {
    ctx.save();
    ctx.strokeStyle = 'rgba(255,255,255,0.06)';
    ctx.lineWidth = 1;
    for (var x = 0; x <= w; x += 30) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, h);
      ctx.stroke();
    }
    for (var y = 0; y <= h; y += 20) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(w, y);
      ctx.stroke();
    }
    ctx.restore();
  }

  function drawPWM(ctx, w, h, duty, phase) {
    var high = h * 0.25;
    var low = h * 0.75;
    ctx.save();
    ctx.strokeStyle = '#3fe6ff';
    ctx.lineWidth = 2;
    ctx.beginPath();

    var period = 140;
    var onWidth = period * duty;

    var x = -phase % period;
    while (x < w + period) {
      ctx.lineTo(x, low);
      ctx.lineTo(x, high);
      ctx.lineTo(x + onWidth, high);
      ctx.lineTo(x + onWidth, low);
      x += period;
    }

    ctx.stroke();
    ctx.restore();
  }

  function drawSine(ctx, w, h, phase) {
    var mid = h * 0.5;
    var amp = h * 0.25;
    ctx.save();
    ctx.strokeStyle = '#3fe6ff';
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (var x = 0; x <= w; x += 2) {
      var y = mid + Math.sin((x + phase) * 0.045) * amp;
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.restore();
  }

  function drawTriangle(ctx, w, h, phase) {
    var mid = h * 0.5;
    var amp = h * 0.26;
    var period = 160;
    ctx.save();
    ctx.strokeStyle = '#3fe6ff';
    ctx.lineWidth = 2;
    ctx.beginPath();
    for (var x = 0; x <= w; x += 2) {
      var t = ((x + phase) % period) / period;
      var y = t < 0.5
        ? mid - amp + (t * 2) * amp * 2
        : mid + amp - ((t - 0.5) * 2) * amp * 2;
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
    ctx.restore();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var canvas = document.getElementById('scope-canvas');
    var slider = document.getElementById('duty');
    var label = document.getElementById('duty-value');
    var waveform = document.getElementById('waveform');
    if (!canvas || !slider || !label || !waveform) return;

    var ctx = canvas.getContext('2d');
    var phase = 0;
    var duty = parseInt(slider.value, 10) / 100;
    var running = false;

    function render() {
      var state = window.machineState || 'idle';
      if (state === 'stopped') {
        requestAnimationFrame(render);
        return;
      }
      var w = canvas.width;
      var h = canvas.height;
      ctx.clearRect(0, 0, w, h);
      drawGrid(ctx, w, h);
      label.textContent = Math.round(duty * 100) + '%';
      if (waveform.value === 'sine') {
        drawSine(ctx, w, h, phase);
      } else if (waveform.value === 'triangle') {
        drawTriangle(ctx, w, h, phase);
      } else {
        drawPWM(ctx, w, h, duty, phase);
      }
      phase += 0.3; // slower movement
      requestAnimationFrame(render);
    }

    slider.addEventListener('input', function () {
      duty = parseInt(slider.value, 10) / 100;
    });
    waveform.addEventListener('change', function () {
      // no-op: render loop picks up current waveform value
    });

    if (!running) {
      running = true;
      render();
    }
  });
})();
