# Stereo Matuška – prezentace vizuální identity

Interaktivní prezentace (slideshow) pro klienta Stereo Matuška. Živě: https://ondrej-broz.github.io/stereo-matuska-prezentace/

## Spuštění

Prezentace potřebuje jednoduchý webový server (kvůli vloženým animacím a načítání dat), otevření souboru dvojklikem nestačí.

```bash
python -m http.server 8766
```

Pak otevřít `http://localhost:8766/slideshow.html` (nebo `index.html`, který na ni přesměruje).

## Ovládání

- šipky / mezerník / klik = další, šipka vlevo = zpět, Home = první slide, End = poslední
- F = celá obrazovka, H = skrýt / ukázat ovládání (šipky a stavový řádek)
- `#N` v adrese otevře N-tý slide

## Obsah

Soubory, které prezentace za běhu používá, a zdroj závěrečného slidu, který se dá opravit přímo tady (`zaver/`).
Ostatní zdrojové podklady jsou mimo repozitář.

- `python kontrola.py` – kontrola před nahráním (skripty, obrázky, odkazy) a očíslovaný seznam slidů
- `python vyfot-slidy.py <název>` – vyfotí slide z HTML do `slideshow/` (zaver, vse)
- `CLAUDE.md` – návod pro úpravy přes Claude Code v prohlížeči

Písmo Kit Rounded (`web/KitRounded-Light.otf`) je licencované přes Adobe.
