var root = document.documentElement;
var theme = document.querySelector('.theme');


// |----------------------------------------------------------------| //
// | LOGIC BEHIND SWITCH LIGHT/DARK MODE WHEN THE BUTTON IS CLICKED | //
// |----------------------------------------------------------------| //
function scheme() {
    return root.style.colorScheme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
}

// ponytail: CSS can't read a manually overridden color-scheme, so the icon
// swap rides on this attribute instead of a second source of truth.
function syncIcon() {
    theme.dataset.scheme = scheme();
}

syncIcon();

theme.addEventListener('click', function () {
    root.style.colorScheme = scheme() === 'dark' ? 'light' : 'dark';
    try { localStorage.theme = root.style.colorScheme; } catch (e) {}
    syncIcon();
});


// |--------------------------------------------------------------------| //
// | BAGIAN NAVBAR DI HEADER KETIKA DALAM MOBILE DISPLAY (WIDTH <760PX) | //
// |--------------------------------------------------------------------| //
var toggle = document.querySelector('.nav-toggle');
var panel = document.getElementById('nav-panel');

toggle.addEventListener('click', function () {
    toggle.setAttribute('aria-expanded', toggle.getAttribute('aria-expanded') !== 'true');
});

// ponytail: close on link tap only. No outside-click / Escape handler until the
// menu grows past four anchors.
panel.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') toggle.setAttribute('aria-expanded', 'false');
});

// |---------------------------------------------------------------| //
// | BAGIAN DURASI DI SECTION EXPERIENCE, CALCULATED NOT HARDCODED | //
// |---------------------------------------------------------------| //
var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
var now = new Date();

function ym(s) {
    var p = s.split('-');
    return { y: +p[0], m: +p[1] - 1 };
}

function label(d) {
    return MONTHS[d.m] + ' ' + d.y;
}

// ponytail: months only, inclusive of both endpoints (Aug -> Sep = 2 mos).
// Roll up to "1 yr 4 mos" once an entry passes a year.
document.querySelectorAll('.entry-when[data-start]').forEach(function (el) {
    var start = ym(el.dataset.start);
    var end = el.dataset.end ? ym(el.dataset.end) : { y: now.getFullYear(), m: now.getMonth() };
    var months = (end.y - start.y) * 12 + end.m - start.m + 1;

    el.textContent = label(start) + ' \u2014 ' + (el.dataset.end ? label(end) : 'Present') +
        ' \u00B7 ' + months + (months === 1 ? ' month' : ' months');
});

// BAGIAN IMAGE MODAL/LIGHTBOX, KETIKA GAMBAR SERTIFIKAT DI SECTION ACHIEVEMENT DICLICK
// ponytail: native <dialog>. Escape, focus trap and backdrop come free; the
// anchor's href stays the no-JS fallback. Click anywhere in the dialog closes.
var lightbox = document.getElementById('lightbox');
var lightboxImg = lightbox.querySelector('img');

document.querySelectorAll('.cert').forEach(function (a) {
    a.addEventListener('click', function (e) {
        e.preventDefault();
        lightboxImg.src = a.href;
        lightboxImg.alt = a.querySelector('img').alt;
        lightbox.showModal();
        document.body.classList.add('no-scroll');
    });
});

lightbox.addEventListener('click', function () {
    lightbox.close();
    document.body.classList.remove('no-scroll');
});