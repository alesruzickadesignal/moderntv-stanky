# Stánek FUTURECOM

Interaktivní 3D náhled výstavního stánku. Nahraješ grafiku na stěny, lištu, čelo pultu
a na obrazovku televize a hned vidíš, jak stánek vypadá — plus kontrolu, jestli jsou data
dost velká pro tisk.

**Živá verze: https://alesruzickadesignal.github.io/stanek-futurecom/**

## Co to umí

- **3D náhled** — tažením otáčení, kolečkem zoom, presety čelní / ¾ / půdorys.
  Stěny jsou plné; přepínač **Řez** odkryje tu, za kterou stojí kamera, aby šlo
  nahlédnout dovnitř.
- **Nárys** — všech pět tiskových ploch čelně vedle sebe ve správném vzájemném
  měřítku. Na kontrolu grafiky před tiskem použitelnější než 3D.
- **JPG, PNG i PDF.** U bitmap se počítá PPI na finální rozměr panelu proti potřebnému
  rozlišení podle pozorovací vzdálenosti (1′ zorného úhlu — stěny z 1,5 m ≈ 23 PPI,
  čelo pultu z 0,6 m ≈ 57 PPI). U PDF se místo toho čte fyzický rozměr stránky a z něj
  se pozná **měřítko** (1:1, 1:10 …) a **spadávka** navíc oproti čistému formátu.
- **Poměr stran** hlídá deformaci — náhled grafiku roztahuje na plný panel, stejně
  jako tisk.
- Rozměry každého panelu se dají přepsat v cm, scéna se přepočítá.

Výchozí rozměry: půdorys 4,00 × 3,00 m, stěny 3,00 m, lišta 2,00 × 0,70 m,
čelo pultu 1,08 × 0,95 m, celkem 3,70 m na výšku.

## Soukromí

Nahrané obrázky zůstávají **jen v prohlížeči** (IndexedDB) — nikam se neodesílají
a nejsou v tomhle repozitáři. Na jiném počítači nebo v anonymním okně bude stánek
prázdný, s ukázkovou grafikou.

## Struktura

| | |
|---|---|
| `src/booth.html` | zdroj — holý obsah stránky bez `<!doctype>` a `<head>` |
| `index.html` | generovaný soubor, který servíruje GitHub Pages |
| `build.py` | doplní obálku (charset, viewport, reset) a přesune `<title>`/`<link>` do `<head>` |

Zdroj je bez obálky proto, že v téhle podobě ho publikují Claude Artifacts, které si ji
přidávají samy. Po úpravě `src/booth.html` je potřeba spustit:

```bash
python3 build.py
```

Bez knihoven, kromě [pdf.js](https://mozilla.github.io/pdf.js/) z CDN pro čtení PDF.
3D je čisté CSS `transform`, žádný WebGL.

Ukázková grafika v prvním spuštění se kreslí do canvasu za běhu — je to placeholder,
ne skutečný návrh.
