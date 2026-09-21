# assets — grafika dodaná v repozitáři

Co je tady, uvidí **každý**, kdo otevře veřejný odkaz. Pojmenuj soubor podle panelu,
spusť `python3 build.py` a pushni.

| panel | názvy souboru, které build pozná |
|---|---|
| Zadní stěna 400 × 300 cm | `back`, `zadni`, `zadni-stena` |
| Levá stěna 300 × 300 cm | `left`, `leva`, `leva-stena` |
| Pravá stěna 300 × 300 cm | `right`, `prava`, `prava-stena` |
| Lišta 200 × 70 cm | `fascia`, `lista`, `placa` |
| Čelo pultu 108 × 95 cm | `counter`, `pult`, `celo-pultu`, `balcao` |
| Obrazovka TV | `tv`, `obrazovka` |

Přípony: `.jpg`, `.jpeg`, `.png`, `.webp`, `.pdf`. Takže např. `back.jpg`,
`leva-stena.pdf`, `lista.png`.

`panels.json` generuje `build.py` — needituj ho ručně.

## Na velikost souborů pozor

GitHub odmítne soubor nad 100 MB a nad 50 MB varuje. Tisková data v plném
rozlišení se sem nehodí — nahraj **náhledovou verzi**, na kontrolu stačí:

```bash
# JPG na dlouhou stranu 3000 px
magick back.tif -resize 3000x3000 -quality 88 back.jpg
```

Kontrola PPI v aplikaci pak ukáže rozlišení toho náhledu, ne finálních dat —
u panelů z repozitáře to ber jako informaci o náhledu.
