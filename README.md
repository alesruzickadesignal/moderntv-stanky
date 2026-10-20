# ModernTV stánky

Interaktivní 3D náhledy výstavních stánků. Nahraješ grafiku na stěny, lištu, čelo pultu
a na obrazovku televize a hned vidíš, jak stánek vypadá — plus kontrolu, jestli jsou data
dost velká pro tisk.

**Živě: https://alesruzickadesignal.github.io/moderntv-stanky/**

| stánek | odkaz |
|---|---|
| FUTURECOM — 3 stěny 4,00 × 3,00 m, lišta, pult, TV na stojanu | [stanek-futurecom/](https://alesruzickadesignal.github.io/moderntv-stanky/stanek-futurecom/) |
| APAC — samostatná stěna 1,90 × 2,50 m, TV na stěně | [stanek-apac/](https://alesruzickadesignal.github.io/moderntv-stanky/stanek-apac/) |

## Co to umí

- **3D náhled** — tažením otáčení, kolečkem zoom, presety čelní / ¾ / půdorys.
  Přepínač **Řez** odkryje stěnu, za kterou stojí kamera.
- **Nárys** — tiskové plochy čelně vedle sebe ve správném vzájemném měřítku.
- **JPG, PNG i PDF.** U bitmap se počítá PPI na finální rozměr panelu proti potřebnému
  rozlišení podle pozorovací vzdálenosti. U PDF se čte fyzický rozměr stránky a z něj
  se pozná **měřítko** (1:1, 1:10 …) a **spadávka**.
- **Poměr stran** hlídá deformaci. Rozměry panelů se dají přepsat v cm.

## Struktura

| | |
|---|---|
| `src/booth.html` | jediný zdroj pro všechny stánky — holý obsah stránky bez `<!doctype>` a `<head>` |
| `booths/<id>.json` | konfigurace stánku: název, podtitulek, Jira, layout, panely s rozměry, TV |
| `build.py` | z každé konfigurace vyrobí `stanek-<id>/index.html` + `stanek-<id>/assets/panels.json` a kořenový rozcestník `index.html` |
| `stanek-<id>/assets/` | grafika dodaná v repozitáři (zmenšené náhledy) |
| `index.html`, `stanek-*/index.html`, `panels.json` | generované — needitovat ručně |

Po každé změně zdroje, konfigurace nebo grafiky:

```bash
python3 build.py && git add -A && git commit -m "…" && git push
```

Zdroj je bez obálky proto, že v téhle podobě ho publikují Claude Artifacts. Když v něm
chybí `window.BOOTH` (samostatně publikovaný soubor), platí výchozí konfigurace
FUTURECOM zapsaná přímo v `src/booth.html` — při změně `booths/futurecom.json` ji uprav taky.

## Nový stánek

1. Zkopíruj `booths/apac.json` (jedna stěna) nebo `booths/futurecom.json` (tři stěny)
   na `booths/<id>.json` a uprav. Klíče:
   - `layout`: `"u"` = zadní + dvě boční stěny, lišta, pult, TV na stojanu;
     `"wall"` = jen jedna samostatná stěna (panel `back`), TV na stěně
   - `panels`: které panely stánek má (`back`, `left`, `right`, `fascia`, `counter`, `tv`)
     a jejich výchozí `w`/`h` v cm, případně `name`
   - `tv.size`: výchozí úhlopříčka (43/50/55/65); `tv.pos` (`back`/`left`/`right`) pro `"u"`;
     `tv.top` = horní hrana TV (vč. rámu) v cm od horní hrany stěny pro `"wall"`
   - `table` (volitelně): kulatý bistro stolek a dvě šedá křesla po stranách před stěnou, `{"d":80,"h":75,"dist":90,"chairs":2}` v cm,
     `d` = průměr desky, `h` = výška, `dist` = od líce stěny ke středu stolku, `chairs` = počet křesel (0–2); zapíná se tlačítkem **Stolek**, netiskne se.
     Nábytek kreslí three.js do WebGL vrstvy přes CSS scénu (načte se jen u stánku s `table`); model křesla musí ležet
     v `stanek-<id>/assets/furniture/chair.glb`, stolek se modeluje v kódu
2. Náhledy grafiky dej do `stanek-<id>/assets/` (názvy viz `stanek-futurecom/assets/README.md`).
3. `python3 build.py` — vznikne `stanek-<id>/` a odkaz v rozcestníku.

## Verze grafiky

Stánek může mít víc verzí grafiky: v `booths/<id>.json` `"versions": ["v1", "v2"]` (první = základ,
tedy `assets/`) a volitelně `"defaultVersion"` (bez něj platí poslední). Soubory verze leží v
`stanek-<id>/assets/<verze>/` a přebíjejí jen panely, které obsahují; zbytek se bere ze základu.
`build.py` je zapíše do `panels.json` pod `versions`. V hlavičce je přepínač v1 | v2, adresa
`?v=1` / `?v=2` (i `?v=v1`) verzi vybere a přepínač ji přepisuje v URL bez znovunačtení;
neznámá hodnota nebo žádná = výchozí verze. Nahraná grafika se ukládá zvlášť pro každou verzi
(základ `stanek-<id>`, ostatní `stanek-<id>-<verze>`); pořadí: nahraná > verze z repozitáře > základ > ukázka.
Stánky bez `versions` se chovají jako dřív.

Úložiště v prohlížeči (IndexedDB `stanek-<id>`, localStorage `stanek-<id>-cfg`
a `stanek-<id>-seeded`) je pro každý stánek zvlášť — stánky sdílí jeden origin.

## Grafika a soukromí

**Dávej do repozitáře zmenšené náhledy, ne tisková data.** Z tiskového PDF náhled
vyrobí macOS `sips`:

```bash
sips -s format jpeg -s formatOptions 80 -Z 2400 tisk.pdf --out stanek-<id>/assets/back.jpg
```

U náhledu z repozitáře se hlásí jen poměr stran (PPI by měřilo náhled). Grafika
**nahraná v aplikaci** zůstává jen v prohlížeči a má přednost před `assets/`;
tlačítko **Odebrat** vrátí verzi z repozitáře.

Knihovny jen z CDN: [pdf.js](https://mozilla.github.io/pdf.js/) pro čtení PDF a u stánků se stolkem
[three.js](https://threejs.org/) 0.170.0 pro nábytek. Stěny, TV a podlaha jsou čisté CSS `transform`;
WebGL kamera se z CSS kamery dopočítává (perspektiva a `perspective-origin` ze stylu `.stage`).

## Licence modelů

- `stanek-apac/assets/furniture/chair.glb` — [„Zel-velvetsilk-dustpink (geometry)"](https://sketchfab.com/3d-models/zel-velvetsilk-dustpink-geometry-f655b8411de94f13acc0439a82b94462)
  od sil3dfurniture (Sketchfab, dnes účet deephousefurniture), licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  Upraveno: textura látky přebarvená z růžové na šedou, textury zmenšené na 512 px, vypuštěné tangenty.
