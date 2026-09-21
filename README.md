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

## Grafika pro všechny, kdo otevřou odkaz

Vlož soubor do [`assets/`](assets/), pojmenuj ho podle panelu (`back.jpg`,
`leva-stena.pdf`, `lista.png` — celá tabulka názvů je v `assets/README.md`),
spusť build a pushni:

```bash
python3 build.py && git add -A && git commit -m "grafika stěn" && git push
```

`build.py` z toho poskládá `assets/panels.json` a stránka grafiku načte každému
návštěvníkovi.

**Dávej sem zmenšené náhledy, ne tisková data.** Stránka se jinak načítá desítky
sekund. Z tiskového PDF náhled vyrobí jednou ranou macOS `sips`:

```bash
sips -s format jpeg -s formatOptions 80 -Z 2400 tisk.pdf --out assets/back.jpg
```

Rastrový soubor z repozitáře má v aplikaci odznak **náhled z repozitáře** a hlásí
se u něj jen poměr stran — PPI by měřilo náhled, ne tisková data, takže by
zbytečně svítilo červeně. Poměr stran smysl má, ten odhalí špatné proporce.

Když do `assets/` dáš přímo **PDF**, přečte se z něj fyzický rozměr stránky
a aplikace hlásí měřítko (1:1, 1:10 …) i spadávku. Je to přesnější, ale pomalé —
hodí se to na vlastní kontrolu, ne na sdílený odkaz.

## Soukromí

Grafika **nahraná v aplikaci** zůstává jen v prohlížeči (IndexedDB) — nikam se
neodesílá a není v repozitáři. Je nadřazená tomu, co je v `assets/`: co si nahraješ,
vidíš jen ty, a tlačítkem **Odebrat** se vrátí verze z repozitáře.

Pořadí: vlastní nahraná grafika → `assets/` → ukázka kreslená za běhu.

## Struktura

| | |
|---|---|
| `src/booth.html` | zdroj — holý obsah stránky bez `<!doctype>` a `<head>` |
| `index.html` | generovaný soubor, který servíruje GitHub Pages |
| `build.py` | doplní obálku (charset, viewport, reset), přesune `<title>`/`<link>` do `<head>` a poskládá manifest assetů |
| `assets/` | grafika dodaná v repozitáři + `panels.json` (generovaný) |

Zdroj je bez obálky proto, že v téhle podobě ho publikují Claude Artifacts, které si ji
přidávají samy. Po úpravě `src/booth.html` je potřeba spustit:

```bash
python3 build.py
```

Bez knihoven, kromě [pdf.js](https://mozilla.github.io/pdf.js/) z CDN pro čtení PDF.
3D je čisté CSS `transform`, žádný WebGL.

Ukázková grafika v prvním spuštění se kreslí do canvasu za běhu — je to placeholder,
ne skutečný návrh.
