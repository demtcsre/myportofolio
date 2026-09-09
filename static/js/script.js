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

// |--------------------------------------------------------------------------------------| //
// | BAGIAN IMAGE MODAL/LIGHTBOX, KETIKA GAMBAR SERTIFIKAT DI SECTION ACHIEVEMENT DICLICK | //
// |--------------------------------------------------------------------------------------| //
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


// |-------------------------| //
// | BAGIAN ANIMASI SNOWFALL | //
// |-------------------------| //
var snow = document.querySelector('.snow');

var SNOW = {
    count: 150,
    speed: 2.5,
    size: 3,
    wind: 0.5
};
var FALL_SECONDS = [9, 18];
var DRIFT_VH = [26, 60];
var SIZE_STEP = [1.7, 4.0];
var GLYPHS = ['\u2744\uFE0E', '\u2746\uFE0E', '\u273B\uFE0E'];
var EASINGS = [
    'linear',
    'linear',
    'cubic-bezier(0.4, 0.05, 0.6, 0.95)',
    'cubic-bezier(0.35, 0.1, 0.65, 0.9)'
];

function rand(min, max) {
    return Math.random() * (max - min) + min;
}

function pick(list) {
    return list[Math.floor(Math.random() * list.length)];
}

if (snow && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var batch = document.createDocumentFragment();

    for (var f = 0; f < SNOW.count; f++) {
        var flake = document.createElement('span');
        var duration = rand(FALL_SECONDS[0], FALL_SECONDS[1]) / SNOW.speed;

        flake.className = 'snowflake';
        flake.textContent = pick(GLYPHS);
        flake.style.cssText =
            '--left:' + rand(-15, 95).toFixed(2) + '%;' +
            '--size:' + (rand(SIZE_STEP[0], SIZE_STEP[1]) * SNOW.size).toFixed(1) + 'px;' +
            '--duration:' + duration.toFixed(2) + 's;' +
            '--delay:-' + rand(0, duration).toFixed(2) + 's;' +
            '--drift:' + (rand(DRIFT_VH[0], DRIFT_VH[1]) * SNOW.wind).toFixed(1) + 'vh;' +
            '--opacity:' + rand(0.35, 0.85).toFixed(2) + ';' +
            'animation-timing-function:' + pick(EASINGS) + ';';

        batch.appendChild(flake);
    }

    snow.appendChild(batch);
}
