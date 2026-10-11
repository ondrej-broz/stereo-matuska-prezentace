"""Vyfotí slidy, které vznikají z HTML (cenová nabídka a závěr), do slideshow/*.webp – na Windows i v Claude Code v prohlížeči (Linux).

    python vyfot-slidy.py nabidka-60          jeden slide
    python vyfot-slidy.py nabidka-80 zaver    několik
    python vyfot-slidy.py vse                 všechny

Slidy: nabidka-80 (40_…), ale (40b_…), nabidka-60 (41_…), zaver (50_…). Každý se vyfotí v headless Chromu ve 2× (3840 × 2160,
originál vedle HTML – podklad pro PDF, do gitu nejde) a zmenší na 1920 × 1080 do slideshow/. Kořen = složka tohoto skriptu
(v repozitáři kořen repa, na Disku Prezentace/final/); skript si sám pustí místní server, nic dalšího běžet nemusí.
Chrome: proměnná CHROME, nainstalovaný Chrome / Chromium, jinak (Linux) stáhne Chrome for Testing ze storage.googleapis.com
do ~/.cache/stereo-chrome a chybějící systémové knihovny doinstaluje přes apt. Náhrada nabidka/nabidka-snimky.py a zaver/zaver-snimek.py (11. 10. 2026)."""
import functools, http.server, os, platform, random, shutil, socketserver, subprocess, sys, threading, urllib.request, zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')   # čeština i v konzoli Windows

KOREN = Path(__file__).resolve().parent
SLIDY = {  # název: (stránka, originál 2×, slide ve slideshow/)
    'nabidka-80': ('nabidka/nabidka.html#80', 'nabidka/nabidka-80.png', '40_nabidka-80000.webp'),
    'ale':        ('nabidka/nabidka.html#ale', 'nabidka/nabidka-ale.png', '40b_nabidka-ale.webp'),
    'nabidka-60': ('nabidka/nabidka.html#60', 'nabidka/nabidka-60.png', '41_nabidka-60000-kredit.webp'),
    'zaver':      ('zaver/zaver.html', 'zaver/zaver.png', '50_zaver.webp'),
}
CFT = '155.0.8059.39'   # Chrome for Testing pro Linux (ověřeno 11. 10. 2026, že ke stažení existuje)
CFT_URL = f'https://storage.googleapis.com/chrome-for-testing-public/{CFT}/linux64/chrome-headless-shell-linux64.zip'
CFT_DIR = Path.home() / '.cache' / 'stereo-chrome' / CFT
# knihovny pro chrome-headless-shell na Ubuntu 24.04 (jména s t64) a starších
APT = ['libnss3 libnspr4 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 '
       'libxrandr2 libgbm1 libasound2t64 libpango-1.0-0 libcairo2 libdbus-1-3 libexpat1 libxext6 libx11-6 libxcb1 fontconfig',
       'libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 '
       'libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libdbus-1-3 libexpat1 libxext6 libx11-6 libxcb1 fontconfig']


def pillow():
    try:
        from PIL import Image
    except ImportError:
        print('Instaluji Pillow (pip install pillow)…')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'pillow'], check=True)
        from PIL import Image
    return Image


def chybejici_knihovny(exe):
    r = subprocess.run(['ldd', str(exe)], capture_output=True, text=True)
    return [l.split()[0] for l in r.stdout.splitlines() if 'not found' in l]


def doinstaluj_knihovny(exe):
    if not chybejici_knihovny(exe):
        return
    if not shutil.which('apt-get'):
        sys.exit('Chromu chybí systémové knihovny a apt-get tu není: ' + ', '.join(chybejici_knihovny(exe)))
    sudo = [] if os.geteuid() == 0 else ['sudo']
    print('Doinstaluji knihovny pro Chrome (apt-get)…')
    subprocess.run(sudo + ['apt-get', 'update', '-qq'], check=False)
    for balicky in APT:
        if subprocess.run(sudo + ['apt-get', 'install', '-y', '-qq', '--no-install-recommends'] + balicky.split()).returncode == 0:
            break
    if chybejici_knihovny(exe):
        sys.exit('Chromu pořád chybí knihovny: ' + ', '.join(chybejici_knihovny(exe)))


def stahni_chrome():
    exe = CFT_DIR / 'chrome-headless-shell-linux64' / 'chrome-headless-shell'
    if not exe.exists():
        CFT_DIR.mkdir(parents=True, exist_ok=True)
        zip_ = CFT_DIR / 'chrome.zip'
        print(f'Stahuji Chrome for Testing {CFT} (~124 MB) z storage.googleapis.com…')
        urllib.request.urlretrieve(CFT_URL, zip_)
        with zipfile.ZipFile(zip_) as z:
            z.extractall(CFT_DIR)
        zip_.unlink()
        exe.chmod(0o755)
    doinstaluj_knihovny(exe)
    return exe


def najdi_chrome():
    if os.environ.get('CHROME'):
        return Path(os.environ['CHROME'])
    if platform.system() == 'Windows':
        for p in (r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'):
            if Path(p).exists():
                return Path(p)
    if platform.system() == 'Darwin':
        p = Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
        if p.exists():
            return p
    shell = CFT_DIR / 'chrome-headless-shell-linux64' / 'chrome-headless-shell'
    if shell.exists():
        doinstaluj_knihovny(shell)
        return shell
    for jmeno in ('google-chrome', 'google-chrome-stable', 'chromium', 'chrome-headless-shell'):
        p = shutil.which(jmeno)
        if p and subprocess.run([p, '--version'], capture_output=True, timeout=30).returncode == 0:
            return Path(p)
    if platform.system() == 'Linux':
        return stahni_chrome()
    sys.exit('Nenašel jsem Chrome – nastav proměnnou CHROME na cestu k chrome.exe.')


class TichyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def main(nazvy):
    if not nazvy or any(n not in SLIDY and n != 'vse' for n in nazvy):
        sys.exit(__doc__ + '\nNeznámý slide: ' + ' '.join(n for n in nazvy if n not in SLIDY and n != 'vse'))
    if 'vse' in nazvy:
        nazvy = list(SLIDY)
    Image = pillow()
    chrome = najdi_chrome()
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 0), functools.partial(TichyHandler, directory=str(KOREN)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    port = server.server_address[1]
    prepinace = ['--disable-gpu', '--hide-scrollbars', '--window-size=1920,1080', '--force-device-scale-factor=2', '--virtual-time-budget=10000']
    if 'headless-shell' not in chrome.name:
        prepinace.insert(0, '--headless=new')
    else:
        prepinace.insert(0, '--headless')
    if platform.system() == 'Linux':
        prepinace += ['--no-sandbox', '--disable-dev-shm-usage']
    try:
        for n in nazvy:
            stranka, png, webp = SLIDY[n]
            cesta, _, kotva = stranka.partition('#')
            url = f'http://127.0.0.1:{port}/{cesta}?x={random.randrange(1 << 30)}' + (f'#{kotva}' if kotva else '')
            png = KOREN / png
            if png.exists():
                png.unlink()
            subprocess.run([str(chrome)] + prepinace + ['--screenshot=' + str(png), url],
                           check=True, timeout=180, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            im = Image.open(png).convert('RGB')
            if im.size != (3840, 2160):
                sys.exit(f'{n}: snímek má {im.size[0]} × {im.size[1]} místo 3840 × 2160 – Chrome nevzal 2× zvětšení.')
            im.resize((1920, 1080), Image.LANCZOS).save(KOREN / 'slideshow' / webp, 'WEBP', quality=95)
            print(f'{n}: slideshow/{webp}')
    finally:
        server.shutdown()


if __name__ == '__main__':
    main(sys.argv[1:])
