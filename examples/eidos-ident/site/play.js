(function () {
  var v = document.getElementById("ident");
  var go = document.getElementById("go");
  var film = document.querySelector(".film");
  if (!v || !go || !film) return;
  var armed = false;

  v.muted = true;
  v.defaultMuted = true;
  v.loop = true;
  v.playsInline = true;
  var preview = v.play();
  if (preview && preview.catch) preview.catch(function () {});

  function reveal() {
    film.classList.add("is-revealing");
    window.setTimeout(function () {
      film.classList.remove("is-restarting", "is-revealing");
      go.hidden = true;
      v.controls = true;
    }, 560);
  }

  go.addEventListener("click", function () {
    if (armed) return;
    armed = true;
    film.classList.add("playing", "is-restarting");
    v.muted = false;
    v.loop = true;
    v.currentTime = 0;
    var p = v.play();
    if (p && p.catch) p.catch(function () {});
    window.setTimeout(reveal, 180);
  });
})();
