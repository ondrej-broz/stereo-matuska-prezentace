# Stereo Matuška – prezentace vizuální identity

Interaktivní prezentace (slideshow) pro klienta Stereo Matuška. Soukromý repozitář – obsahuje nevydanou identitu klienta.

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

Jen soubory, které prezentace za běhu používá (zdrojové podklady a generátory jsou mimo repozitář).
Písmo Kit Rounded (`web/KitRounded-Light.otf`) je licencované přes Adobe.
