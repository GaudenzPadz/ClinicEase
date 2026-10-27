/* =========================================================
   JS: dots, keyboard arrows, dark-slide detection
   ========================================================= */
(function () {
    var slides = [].slice.call(document.querySelectorAll('.slide'));
    var dots = document.getElementById('dots');
    slides.forEach(function (s, i) {                       // 1. one dot per slide
        var a = document.createElement('a');
        a.href = '#' + s.id; a.setAttribute('aria-label', s.dataset.title); a.title = s.dataset.title;
        dots.appendChild(a);
    });
    var links = [].slice.call(dots.children);
    var current = 0;
    var io = new IntersectionObserver(function (entries) {  // 2. which slide is on screen?
        entries.forEach(function (e) {
            if (e.isIntersecting) {
                current = slides.indexOf(e.target);
                links.forEach(function (l, i) { l.classList.toggle('on', i === current) });
                var dark = e.target.classList.contains('dark') || e.target.id === 'start';
                document.body.classList.toggle('on-dark', dark);
            }
        });
    }, { threshold: 0.6 });
    slides.forEach(function (s) { io.observe(s) });
    document.addEventListener('keydown', function (e) {     // 3. arrows / PageUp / PageDown / space
        var next = ['ArrowDown', 'PageDown'].indexOf(e.key) > -1;
        var prev = ['ArrowUp', 'PageUp'].indexOf(e.key) > -1;
        if (!next && !prev) return;
        e.preventDefault();
        var t = Math.max(0, Math.min(slides.length - 1, current + (next ? 1 : -1)));
        slides[t].scrollIntoView({ behavior: 'smooth' });
    });
})();