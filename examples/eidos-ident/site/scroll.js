(function () {
  var rail = document.getElementById("rail");
  var dots = Array.prototype.slice.call(document.querySelectorAll(".dots a"));
  var links = Array.prototype.slice.call(document.querySelectorAll(".rail-links a[href^='#']"));

  function onScroll() {
    rail.classList.toggle("scrolled", window.scrollY > 12);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) e.target.classList.add("in");
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });

  var chapterIo = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var id = e.target.getAttribute("data-chapter");
      dots.forEach(function (d) {
        d.classList.toggle("on", d.getAttribute("data-chapter") === id);
      });
      links.forEach(function (a) {
        var href = a.getAttribute("href") || "";
        a.classList.toggle("on", href === "#" + id);
      });
    });
  }, { threshold: 0.45 });
  document.querySelectorAll("section.chapter[data-chapter]").forEach(function (el) {
    chapterIo.observe(el);
  });
})();
