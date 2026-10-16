"""Kontrola prezentace před nahráním (11. 10. 2026): python kontrola.py

1. skripty ve stránkách jdou přeložit (node --check) – např. rovný apostrof v textu slidu by jinak shodil celou prezentaci,
2. každý slide ze seznamu SLIDES ve slideshow.html má svůj obrázek / text / animaci,
3. obrázky, písma a stránky, na které stránky odkazují, existují.
Vypíše očíslovaný seznam slidů (stejná čísla jako stavový řádek „N / počet“). Konec s kódem 1, když něco nesedí. Potřebuje Node.js."""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
from urllib.parse import unquote

sys.stdout.reconfigure(encoding='utf-8', errors='replace')   # čeština i v konzoli Windows

KOREN = Path(__file__).resolve().parent
STRANKY = ['slideshow.html', 'intro-vyloha.html', 'koncept/prepinac-nalezato.html', 'socialni site/instagram-slide.html',
           'zaver/zaver.html']
SKRIPTY = ['socialni site/instagram.js']
VYFOT = {'50_zaver.webp': 'zaver'}   # slidy z HTML (vyfot-slidy.py)
chyby = []


def node_check(kod, kde):
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(kod)
    r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True, encoding='utf-8')
    Path(f.name).unlink()
    if r.returncode:
        radky = [l for l in r.stderr.splitlines() if l.strip() and not l.startswith(('    at ', 'Node.js '))]
        chyby.append(f'{kde}: skript nejde přeložit – ' + ' | '.join(radky[-4:]))


if not shutil.which('node'):
    sys.exit('Chybí Node.js (node) – bez něj kontrolu skriptů neudělám.')

# 1. skripty
for s in STRANKY:
    html = (KOREN / s).read_text(encoding='utf-8')
    for i, m in enumerate(re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>', html)):
        node_check(m.group(1), f'{s} (skript {i + 1})')
for s in SKRIPTY:
    node_check((KOREN / s).read_text(encoding='utf-8'), s)

# 2. seznam slidů
html = (KOREN / 'slideshow.html').read_text(encoding='utf-8')
def literal(jmeno, konec):
    m = re.search(r'const ' + jmeno + r' = ([\s\S]*?' + konec + r');', html)
    if not m:
        chyby.append(f'slideshow.html: nenašel jsem {jmeno}')
    return m.group(1) if m else '[]'
js = ('const NOC = ' + (re.search(r"const NOC = ('[^']*')", html) or [None, "''"])[1] + ', DEN = ' + (re.search(r"DEN = ('[^']*')", html) or [None, "''"])[1] + ';\n'
      + 'const SLIDES = ' + literal('SLIDES', r'\n\]') + ';\nconst TEXTY = ' + literal('TEXTY', r'\n\}') + ';\nconst ANIM_SRC = ' + literal('ANIM_SRC', r'\}')
      + ';\nconst NAZVY = ' + literal('NAZVY', r'\n\}') + ';\nconsole.log(JSON.stringify({SLIDES, TEXTY, ANIM_SRC, NAZVY, NOC, DEN}));')
r = subprocess.run(['node', '-e', js], capture_output=True, text=True, encoding='utf-8')
if r.returncode:
    chyby.append('slideshow.html: seznam slidů nejde načíst – ' + next((l for l in r.stderr.splitlines() if 'Error' in l), r.stderr.strip()[-200:]))
    data = {'SLIDES': [], 'TEXTY': {}, 'ANIM_SRC': {}, 'NAZVY': {}}
else:
    data = json.loads(r.stdout)
def existuje(cesta, kde):
    cesta = unquote(cesta.split('#')[0].split('?')[0])
    if not (KOREN / cesta).is_file():
        chyby.append(f'{kde}: chybí soubor {cesta}')
print('Slidy:')
for i, n in enumerate(data['SLIDES'], 1):
    pozn = ''
    if n.startswith('text:'):
        t = data['TEXTY'].get(n[5:])
        if not t:
            chyby.append(f'slide {i} ({n}): v TEXTY chybí položka {n[5:]}')
        else:
            pozn = f"text „{t['nadpis']}“ (TEXTY.{n[5:]} ve slideshow.html)"
            existuje(t['pozadi'], f'slide {i} ({n}) – pozadí')
    elif n.startswith('anim:'):
        src = data['ANIM_SRC'].get(n[5:], 'intro-vyloha.html#usek=' + n[5:])
        existuje(src, f'slide {i} ({n})'); pozn = 'animace ' + unquote(src.split('?')[0].split('#')[0])
    elif n == 'outro':
        pozn = 'outro (outro/vrstvy/)'
    else:
        existuje('slideshow/' + n, f'slide {i}')
        pozn = 'obrázek' + (f' z HTML – python vyfot-slidy.py {VYFOT[n]}' if n in VYFOT else '')
    nazev = data['NAZVY'].get(n, '')
    print(f'  {i:2}  {n}' + (f'  [{nazev}]' if nazev else '') + f'  – {pozn}')

# 3. odkazy ve stránkách (src="…", url(…), href="…"), bez dynamicky skládaných
for s in STRANKY:
    obsah = (KOREN / s).read_text(encoding='utf-8')
    for m in re.finditer(r'''(?:src|href)=["']([^"'#?${}+]+\.(?:png|webp|jpg|jpeg|svg|otf|ttf|woff2?|js|css|html))["#?]|url\(['"]?([^'")$+]+\.(?:png|webp|jpg|jpeg|svg|otf|ttf|woff2?))['"]?\)''', obsah):
        cil = m.group(1) or m.group(2)
        if cil.startswith(('http:', 'https:', 'data:', '//')):
            continue
        existuje(str(Path(s).parent / cil), s)

if chyby:
    print('\nCHYBY:'); [print('  - ' + c) for c in chyby]
    sys.exit(1)
print(f'\nV pořádku: {len(data["SLIDES"])} slidů, skripty jdou přeložit, všechny soubory existují.')
