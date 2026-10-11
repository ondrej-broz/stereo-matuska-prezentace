/* Obrazovka Instagramu pro mockup Stereo Matuška (Ondra 11. 10. 2026) – společné pro instagram.html (jedna obrazovka)
   a instagram-slide.html (telefony na slidu, animace v prezentaci).
   IG.obrazovka(view) = HTML obrazovky: 'profil' (bez výběrů, mřížka postů 18–20 v 3 : 4) nebo 'post-18' / 'post-19' / 'post-20' (detail bez popisku).
   IG.stav(el, view, t) = stav animace v čase t s od začátku animace obrazovky; t = null → klidový stav bez animace.
     profil: posty naskočí do mřížky jeden po druhém (počítadlo 0 → 3), pak klepnutí na Sledovat → „Sledujete“, sledující +1
     post:   dvojklik na fotku – velké srdce, ikona zčervená, lajky +1
   Zástupné: účet „stereomatuska“, čísla sledujících a lajků, bio (finální texty dodá copywriter). */
const IG = (() => {
  const W = '#f5f5f5';
  const tecky = `<circle cx="5" cy="12" r="1.3" fill="${W}" stroke="none"/><circle cx="12" cy="12" r="1.3" fill="${W}" stroke="none"/><circle cx="19" cy="12" r="1.3" fill="${W}" stroke="none"/>`;
  const zpet = `<svg class="i" viewBox="0 0 24 24"><path d="M15 4l-8 8 8 8" stroke-width="2.2"/></svg>`;
  const reels = f => `<rect x="3" y="3" width="18" height="18" rx="5"/><path d="M3 8.5h18M8 3l3 5.5M14 3l3 5.5"/><path d="M10 12.2v5l4.3-2.5z" fill="${f}" stroke-width="1.4"/>`;
  const SRDCE = 'M12 20.5s-8-4.9-8-11A4.6 4.6 0 0 1 12 6.6a4.6 4.6 0 0 1 8 2.9c0 6.1-8 11-8 11z';
  const POSTY = { 18: { lk: 312, km: 18 }, 19: { lk: 248, km: 14 }, 20: { lk: 196, km: 23 } };
  const SLEDUJICI = 1248;
  const cislo = n => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  const prispevky = n => n === 1 ? 'příspěvek' : n >= 2 && n <= 4 ? 'příspěvky' : 'příspěvků';

  const lista = `<div class="sb"><span>20:41</span><span class="ic">
      <svg width="18" height="12" viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx="1" fill="${W}"/><rect x="5" y="5.5" width="3" height="6.5" rx="1" fill="${W}"/><rect x="10" y="3" width="3" height="9" rx="1" fill="${W}"/><rect x="15" y="0" width="3" height="12" rx="1" fill="${W}"/></svg>
      <svg width="17" height="12" viewBox="0 0 17 12"><path d="M8.5 11.2l2.4-2.6a3.5 3.5 0 0 0-4.8 0zM3.9 6.4a6.6 6.6 0 0 1 9.2 0l1.6-1.7a9 9 0 0 0-12.4 0zM.6 3a11.3 11.3 0 0 1 15.8 0L17 2.3A12.3 12.3 0 0 0 0 2.3z" fill="${W}"/></svg>
      <svg width="27" height="13" viewBox="0 0 27 13"><rect x=".5" y=".5" width="23" height="12" rx="3.5" fill="none" stroke="#8a8a8a"/><rect x="2" y="2" width="17" height="9" rx="2" fill="${W}"/><path d="M25 4.5v4a2 2 0 0 0 0-4z" fill="#8a8a8a"/></svg>
    </span></div>`;
  const spodek = `<div class="tb"><div class="ic">
      <svg class="i" viewBox="0 0 24 24"><path d="M3.5 10.5L12 3l8.5 7.5V20a1 1 0 0 1-1 1H15v-6.5H9V21H4.5a1 1 0 0 1-1-1z"/></svg>
      <svg class="i" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="7"/><path d="M15.6 15.6L21 21"/></svg>
      <svg class="i" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><path d="M12 7.5v9M7.5 12h9"/></svg>
      <svg class="i" viewBox="0 0 24 24">${reels(W)}</svg>
      <span class="me"></span>
    </div><div class="home"></div></div>`;

  const profil = () => `
    <div class="nav">${zpet}<b>stereomatuska</b><span class="r">
      <svg class="i" viewBox="0 0 24 24"><path d="M18 16.5V11a6 6 0 0 0-12 0v5.5L4.5 18.5h15zM10 21h4"/></svg>
      <svg class="i" viewBox="0 0 24 24">${tecky}</svg></span></div>
    <div class="head"><img src="PROFILOVKA.png" alt="">
      <div class="stats">
        <div><b class="np">3</b><span class="lp">příspěvky</span></div>
        <div><b class="ns">${cislo(SLEDUJICI)}</b><span>sledující</span></div>
        <div><b>87</b><span>sledovaní</span></div>
      </div></div>
    <div class="bio"><b>STEREO MATUŠKA</b><br><span class="cat">Kavárna</span><br>
      Ve dne vinyly u&nbsp;kávy, večer pivo a&nbsp;živá hudba.<br>Pasáž Lucerna, Praha&nbsp;1<br>Otevíráme v&nbsp;prosinci 2026</div>
    <div class="btns">
      <div class="f sled"><span class="tx">Sledovat</span><svg class="i" viewBox="0 0 24 24"><path d="M6 9.5l6 6 6-6"/></svg></div><div>Zpráva</div>
      <div class="s"><svg class="i" viewBox="0 0 24 24"><circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3-6.5 7-6.5s7 2.5 7 6.5M19 8v6M16 11h6"/></svg></div>
    </div>
    <div class="tabs">
      <div class="on"><svg class="i" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 3v18M15 3v18M3 9h18M3 15h18"/></svg></div>
      <div><svg class="i" viewBox="0 0 24 24">${reels('#8e8e8e')}</svg></div>
      <div><svg class="i" viewBox="0 0 24 24"><path d="M9.5 3H6a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3V6a3 3 0 0 0-3-3h-3.5L12 5.5z"/><circle cx="12" cy="11" r="2.8"/><path d="M6.8 21c.6-3 2.7-4.6 5.2-4.6s4.6 1.6 5.2 4.6"/></svg></div>
    </div>
    <div class="grid"><img src="18.png" alt=""><img src="19.png" alt=""><img src="20.png" alt=""></div>`;

  const post = n => `
    <div class="nav c">${zpet}<b>Příspěvky</b></div>
    <div class="row"><img src="PROFILOVKA.png" alt=""><div class="who"><b>stereomatuska</b><small>Pasáž Lucerna</small></div>
      <svg class="i dots" width="24" height="24" viewBox="0 0 24 24">${tecky}</svg></div>
    <div class="foto"><img class="post" src="${n}.png" alt=""><svg class="srdce" viewBox="0 0 24 24"><path d="${SRDCE}" fill="#fff"/></svg></div>
    <div class="act">
      <span><svg class="i lk" viewBox="0 0 24 24"><path d="${SRDCE}"/></svg><i class="nl" style="font-style:normal">${POSTY[n].lk}</i></span>
      <span><svg class="i" viewBox="0 0 24 24"><path d="M20.5 11.6a8.5 8.5 0 1 1-4.3-7.4c2.6 1.5 4.3 4.3 4.3 7.4zM20.5 20.5l-1.6-4.6"/></svg>${POSTY[n].km}</span>
      <span><svg class="i" viewBox="0 0 24 24"><path d="M21.5 3L10.2 13.4M21.5 3l-6.6 18-4.7-7.6L2.5 9.2z"/></svg>9</span>
      <svg class="i sv" viewBox="0 0 24 24"><path d="M18.5 21l-6.5-6.2L5.5 21V3.5h13z"/></svg>
    </div>`;

  const cisloPostu = view => (/^post-(\d+)$/.exec(view) || [])[1];
  const obrazovka = view => `<div class="ph">${lista}${cisloPostu(view) ? post(cisloPostu(view)) : profil()}${spodek}</div>`;

  // --- animace (brand easing jako zbytek prezentace) ---
  function bez(x1, y1, x2, y2) {
    const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx, cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    return t => { let x = t; for (let i = 0; i < 8; i++) { const f = ((ax * x + bx) * x + cx) * x - t, d = (3 * ax * x + 2 * bx) * x + cx; if (Math.abs(d) < 1e-6) break; x -= f / d; } return ((ay * x + by) * x + cy) * x; };
  }
  const ease = bez(.65, 0, .35, 1), easeOut = bez(.2, .7, .3, 1);
  const cl = x => Math.max(0, Math.min(1, x));
  const hrb = (t, t0, d) => Math.sin(Math.PI * cl((t - t0) / d));          // 0 → 1 → 0 (krátké „pérování“ po změně)
  // časy v s od začátku animace obrazovky
  const PROFIL = { dlazdice: [.5, .9, 1.3], naskok: .55, klep: 2.3, konec: 2.8 };
  const POST = { lajk: .1, konec: 1.0 };

  function stav(el, view, t) {
    const n = cisloPostu(view);
    if (n) {
      const s = el.querySelector('.srdce'), lk = el.querySelector('.lk'), nl = el.querySelector('.nl');
      const on = t !== null && t >= POST.lajk;
      lk.classList.toggle('on', on);
      nl.textContent = POSTY[n].lk + (on ? 1 : 0);
      lk.style.transform = t === null ? '' : `scale(${1 + .28 * hrb(t, POST.lajk, .3)})`;
      if (t === null || t < 0 || t > .95) { s.style.opacity = 0; return; }
      const sc = t < .18 ? 1.2 * easeOut(t / .18) : t < .32 ? 1.2 - .2 * ease((t - .18) / .14) : t < .7 ? 1 : 1 - .25 * ease((t - .7) / .25);
      s.style.opacity = t < .7 ? Math.min(1, t / .08) : 1 - ease((t - .7) / .25);
      s.style.transform = `scale(${sc})`;
      return;
    }
    const D = PROFIL.dlazdice, tiles = el.querySelectorAll('.grid img');
    tiles.forEach((img, i) => {
      const e = t === null ? 1 : ease(cl((t - D[i]) / PROFIL.naskok));
      img.style.opacity = e; img.style.transform = e < 1 ? `scale(${.92 + .08 * e})` : '';
    });
    const kolik = t === null ? 3 : D.filter(d => t >= d + .12).length;
    el.querySelector('.np').textContent = kolik;
    el.querySelector('.lp').textContent = prispevky(kolik);
    el.querySelector('.np').style.transform = t === null || !kolik ? '' : `scale(${1 + .2 * hrb(t, D[kolik - 1] + .12, .28)})`;
    const k = PROFIL.klep, sled = t !== null && t >= k + .12, b = el.querySelector('.sled');
    b.classList.toggle('f', !sled); b.classList.toggle('sl', sled);
    b.querySelector('.tx').textContent = sled ? 'Sledujete' : 'Sledovat';
    b.style.transform = t === null ? '' : `scale(${1 - .05 * ease(cl((t - k) / .12)) + .05 * ease(cl((t - k - .12) / .22))})`;
    el.querySelector('.ns').textContent = cislo(SLEDUJICI + (sled ? 1 : 0));
    el.querySelector('.ns').style.transform = t === null ? '' : `scale(${1 + .2 * hrb(t, k + .12, .28)})`;
  }
  return { obrazovka, stav, PROFIL, POST, ease };
})();
