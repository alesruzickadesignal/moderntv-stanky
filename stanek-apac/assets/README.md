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

TV visí uprostřed volného pole grafiky (52–120 cm od horní hrany), střed
`tv.centerFromTop` v `booths/apac.json`. Když se grafika změní, přeměř ho.
