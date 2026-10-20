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
2. Náhledy grafiky dej do `stanek-<id>/assets/` (názvy viz `stanek-futurecom/assets/README.md`).
3. `python3 build.py` — vznikne `stanek-<id>/` a odkaz v rozcestníku.

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

Bez knihoven, kromě [pdf.js](https://mozilla.github.io/pdf.js/) z CDN pro čtení PDF.
3D je čisté CSS `transform`, žádný WebGL.
