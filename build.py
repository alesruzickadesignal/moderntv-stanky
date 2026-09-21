#!/usr/bin/env python3
"""Z src/booth.html vyrobí samostatné index.html pro GitHub Pages.

src/booth.html je holý obsah stránky bez <!doctype> a <head>, protože přesně
v téhle podobě ho publikují Claude Artifacts – obálku si přidávají samy.
Pro Pages ji musí doplnit tenhle skript, hlavně charset (bez něj se rozsype
diakritika) a viewport. <title> a <link> se přesouvají do <head>, kam patří.
"""
import json, pathlib, re

SRC = pathlib.Path("src/booth.html")
OUT = pathlib.Path("index.html")
ASSETS = pathlib.Path("assets")
MANIFEST = ASSETS / "panels.json"

# jak se smí jmenovat soubor pro daný panel (bez přípony)
PANEL_NAMES = {
    "back":    ("back", "zadni", "zadni-stena"),
    "left":    ("left", "leva", "leva-stena"),
    "right":   ("right", "prava", "prava-stena"),
    "fascia":  ("fascia", "lista", "placa"),
    "counter": ("counter", "pult", "celo-pultu", "balcao"),
    "tv":      ("tv", "obrazovka"),
}
EXTS = (".jpg", ".jpeg", ".png", ".webp", ".pdf")
GH_WARN, GH_LIMIT = 50 * 1024**2, 100 * 1024**2

HEAD_TAGS = re.compile(r"^[ \t]*(?:<title>.*?</title>|<link\b[^>]*>|<meta\b[^>]*>)[ \t]*\r?\n",
                       re.IGNORECASE | re.DOTALL | re.MULTILINE)

RESET = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Interaktivní 3D náhled výstavního stánku: nahraj grafiku na stěny, lištu, pult i obrazovku a zkontroluj rozlišení a poměr stran.">
<style>
:root{color-scheme:light dark;
  padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px)}
html,body{margin:0}
body{font:14px system-ui,-apple-system,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>"""


def scan_assets():
    """Poskládá assets/panels.json z toho, co leží v assets/."""
    lookup = {name: pid for pid, names in PANEL_NAMES.items() for name in names}
    found, notes = {}, []
    for f in sorted(ASSETS.glob("*")) if ASSETS.is_dir() else []:
        if f.suffix.lower() not in EXTS:
            continue
        pid = lookup.get(f.name[: -len(f.suffix)].lower())
        if pid is None:
            notes.append(f"  ! {f.name} – název neodpovídá žádnému panelu, přeskočeno")
            continue
        if pid in found:
            notes.append(f"  ! {f.name} – pro panel {pid} už soubor je, přeskočeno")
            continue
        size = f.stat().st_size
        if size >= GH_LIMIT:
            notes.append(f"  ! {f.name} – {size/1024**2:.0f} MB, GitHub to odmítne (limit 100 MB)")
            continue
        if size >= GH_WARN:
            notes.append(f"  ~ {f.name} – {size/1024**2:.0f} MB, GitHub bude varovat; zmenši náhled")
        found[pid] = f.as_posix()
        notes.append(f"  + {pid:<8} {f.name} ({size/1024:,.0f} kB)")

    if ASSETS.is_dir() or found:
        ASSETS.mkdir(exist_ok=True)
        MANIFEST.write_text(json.dumps(found, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")
    return found, notes


def main():
    src = SRC.read_text(encoding="utf-8")

    # souvislý blok hlavičkových tagů na začátku souboru patří do <head>
    prefix_end = 0
    for m in HEAD_TAGS.finditer(src):
        if m.start() != prefix_end:
            break
        prefix_end = m.end()
    head = [m.group(0).strip() for m in HEAD_TAGS.finditer(src[:prefix_end])]
    body = src[prefix_end:].lstrip("\n")

    doc = ("<!doctype html>\n<html lang=\"cs\">\n<head>\n"
           + RESET + "\n"
           + "\n".join(head) + "\n"
           + "</head>\n<body>\n"
           + body.rstrip() + "\n</body>\n</html>\n")
    OUT.write_text(doc, encoding="utf-8")
    print(f"{OUT} ({OUT.stat().st_size:,} B), do <head> přesunuto tagů: {len(head)}")

    found, notes = scan_assets()
    print(f"{MANIFEST}: {len(found)} z {len(PANEL_NAMES)} panelů má grafiku v repozitáři")
    for n in notes:
        print(n)
    if not found:
        print("  (assets/ je prázdné – návštěvníkům se ukáže ukázková grafika)")


if __name__ == "__main__":
    main()
