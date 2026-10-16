# Stereo Matuška – prezentace (návod pro Clauda v prohlížeči)

Prezentace vizuální identity podniku STEREO MATUŠKA (kavárna přes den, bar s živou hudbou večer) od Ondřeje Brože a Tomáše Bendy.
Živě běží na **https://ondrej-broz.github.io/stereo-matuska-prezentace/** (GitHub Pages z větve `main`, kořen repozitáře).
Opravy zadává Ondra (grafik, ne vývojář) přes Claude Code v prohlížeči nebo v mobilu – často narychlo před prezentací.

## Jak s Ondrou pracovat

- Odpovídej **česky**, jednoduše, bez žargonu. Odborný pojem vysvětli poprvé jednou větou.
- **Měň jen to, co Ondra zadal.** Design je schválený – nic „nevylepšuj“, neuklízej kód, nepřejmenovávej soubory.
- Ondra mluví o slidech čísly ze stavového řádku vpravo dole („N / 33“). Čísla → soubory vypíše `python3 kontrola.py`.
- Když není jasné, který slide nebo jaký text, zeptej se dřív, než začneš.

## Postup u každé opravy

1. `python3 kontrola.py` – očíslovaný seznam slidů a odkud se který bere.
2. Uprav (viz tabulka níže).
3. Slide, který vzniká z HTML (závěr): `python3 vyfot-slidy.py <název>` a výsledný obrázek ve `slideshow/` si prohlédni (otevři ho jako obrázek), jestli text sedí a nic nepřetéká.
4. `python3 kontrola.py` musí skončit „V pořádku“. Jinak oprav a pusť znovu.
5. Commit (zpráva česky: co se na kterém slidu změnilo) a push do své větve.
6. Řekni Ondrovi, co přesně se změnilo, a ať změnu pustí na web: **Create PR** → na GitHubu **Merge pull request** (jde i v mobilní aplikaci GitHub). Jeho Merge je zároveň kontrola člověkem před zveřejněním.
7. Po Merge je změna na webu zhruba do minuty. Prohlížeč ale drží starou verzi až 10 minut – ať to Ondra ověří v **anonymním okně**.

## Co je kde

| Slide (č.) | Kde se mění | Poznámka |
|---|---|---|
| texty Úvod, Přepínač, Přenoska, Font, Barvy (2, 5, 8, 18, 22) | `slideshow.html`, objekt `TEXTY` | text je v rovných apostrofech `'…'` |
| pořadí slidů, vyřazení slidu | `slideshow.html`, pole `SLIDES` | názvy ve stavovém řádku: objekt `NAZVY` |
| podpis „CREATED BY…“ (1) | `slideshow.html`, `#kredit` | |
| závěr – slogan a kontakty (33) | `zaver/zaver.html` | `python3 vyfot-slidy.py zaver` |
| Instagram – profil a posty (30, 31) | `socialni site/instagram.js` | živé HTML, nic se nefotí |
| animace intro, přepínač, logo (1, 7, 9) | `intro-vyloha.html` | |
| přepínač naležato (6) | `koncept/prepinac-nalezato.html` | |
| outro (32) | `outro/vrstvy/` | |
| ostatní obrázkové slidy | `slideshow/*.webp` (1920 × 1080) | hotové exporty od Ondry – text v nich jde opravit jen novým obrázkem |

Písma ve `web/`: `StereoDisplay-Regular.otf` (autorské písmo identity), `KitRounded-Light.otf` (licence Adobe – nešířit, nekopírovat jinam).

## Nový obrázek od Ondry

Obrázek z konverzace neumíš uložit do souboru. Ať ho Ondra nahraje na GitHub: repozitář → **Add file → Upload files** → do složky `nahrane/` (větev `main`). Ty si ho stáhneš `git pull origin main`, převedeš na webp 1920 × 1080 (Pillow), uložíš pod názvem, který slide používá, a soubor z `nahrane/` smažeš.

## Na co si dát pozor

- **Rovný apostrof `'` uvnitř textů v `TEXTY` shodí celou prezentaci.** Uvozovky piš české „…“. Kontrola to pozná.
- Repozitář je **veřejný**: nepřidávej interní dokumenty, ceny ani obchodní podmínky (jsou jen v Ondrově verzi na Disku), smlouvy ani osobní údaje (kromě kontaktů, které už jsou na závěru). Žádné hesla ani klíče.
- Nemaž soubory, které Ondra nezmínil, a nikdy nedělej force push ani přepis historie.
- Rozměry slidů zůstávají 1920 × 1080; když měníš název obrázku, uprav i `SLIDES` a `NAZVY`.

## Prostředí v cloudu

- `vyfot-slidy.py` si sám stáhne Chrome for Testing (~124 MB ze storage.googleapis.com, výchozí síťový přístup „Trusted“ ho povoluje), doinstaluje knihovny přes `apt-get` a Pillow přes `pip`. První spuštění trvá déle.
- Kdyby stažení selhalo kvůli síti: ať Ondra v claude.ai/code klikne na ikonu mraku nad polem pro zprávu a nastaví přístup k síti na **Full** (nebo Custom + `storage.googleapis.com`), pak novou session.
- Drobné rozdíly ve vyhlazení písma oproti snímkům z Windows jsou normální.
- `kontrola.py` potřebuje Node.js (v cloudu je).

## Vztah k Ondrovým podkladům

Kořen repozitáře odpovídá složce `Prezentace/final/` na Ondrově Google Disku, kde jsou i zdrojové podklady. Na Disku je prezentace delší (má části, které sem nepatří), tady je veřejná verze – slidy proto čísluj podle `python3 kontrola.py` tady, ne podle Disku. Ondrův Claude na počítači odtud nahrává změny a před tím si stáhne všechno, co mezitím přibylo tady. Proto neměň strukturu složek a do zpráv commitů piš srozumitelně, co se změnilo.
