# assets — grafika stánku FUTURECOM dodaná v repozitáři

Co je tady, uvidí **každý**, kdo otevře veřejný odkaz. Pojmenuj soubor podle panelu,
spusť `python3 build.py` a pushni.

| panel | názvy souboru, které build pozná |
|---|---|
| Zadní stěna 400 × 300 cm | `back`, `zadni`, `zadni-stena`, `stena` |
| Levá stěna 300 × 300 cm | `left`, `leva`, `leva-stena` |
| Pravá stěna 300 × 300 cm | `right`, `prava`, `prava-stena` |
| Lišta 200 × 70 cm | `fascia`, `lista`, `placa` |
| Čelo pultu 108 × 95 cm | `counter`, `pult`, `celo-pultu`, `balcao` |
| Obrazovka TV | `tv`, `obrazovka` |

Přípony: `.jpg`, `.jpeg`, `.png`, `.webp`, `.pdf`. Takže např. `back.jpg`,
`leva-stena.pdf`, `lista.png`.

`panels.json` generuje `build.py` — needituj ho ručně.

## Zmenšené náhledy, ne tisková data

Stránka soubory stahuje a vykresluje v prohlížeči, takže tisková PDF ji zpomalí
na desítky sekund. Náhled vyrobí macOS `sips`:

```bash
sips -s format jpeg -s formatOptions 80 -Z 2400 tisk.pdf --out stanek-futurecom/assets/back.jpg
```

U rastrového náhledu aplikace hlásí jen poměr stran, ne PPI — měřilo by náhled,
ne finální data. Tisková data kontroluj na originálu, nebo si ho v aplikaci nahraj
přes **Nahradit** (zůstane jen u tebe v prohlížeči).

Vložené **PDF** se čte v plné parádě — pozná se z něj měřítko i spadávka —
ale je pomalé. GitHub navíc odmítne soubor nad 100 MB.
