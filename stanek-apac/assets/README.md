# assets — grafika stánku APAC dodaná v repozitáři

Co je tady, uvidí **každý**, kdo otevře veřejný odkaz. Pojmenuj soubor podle panelu,
spusť `python3 build.py` a pushni.

| panel | názvy souboru, které build pozná |
|---|---|
| Stěna 190 × 250 cm | `back`, `stena`, `zadni`, `zadni-stena` |
| Obrazovka TV | `tv`, `obrazovka` |

Přípony `.jpg`, `.jpeg`, `.png`, `.webp`, `.pdf`. `panels.json` generuje `build.py`.

Náhled stěny je z grafikova PDF (190 × 250 cm), tisková data sem nepatří:

```bash
sips -s format jpeg -s formatOptions 80 -Z 2400 Stánek.pdf --out stanek-apac/assets/back.jpg
```

Verze grafiky: `assets/` je v1, `assets/v2/` přebíjí soubory v2 (např. `v2/back.jpg`, později i `v2/tv.jpg`);
co ve složce verze chybí, se vezme z `assets/`. Odkaz `?v=1` / `?v=2`, bez parametru se otevře nejnovější (v2).
Náhled v2: `sips -s format jpeg -s formatOptions 80 -Z 2400 Stánek.pdf --out stanek-apac/assets/v2/back.jpg`.

TV 55″ visí vodorovně uprostřed, horní hrana rámu 50 cm od horní hrany stěny
(podle specifikace pořadatele) — `tv.top` v `booths/apac.json`.

`furniture/chair.glb` je 3D model křesla pro stolek (`table` v `booths/apac.json`), build.py
ho nechává být. Původ a licence (CC BY 4.0) viz README v kořeni repozitáře.
