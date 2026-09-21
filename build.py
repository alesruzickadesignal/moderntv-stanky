#!/usr/bin/env python3
"""Z src/booth.html vyrobí samostatné index.html pro GitHub Pages.

src/booth.html je holý obsah stránky bez <!doctype> a <head>, protože přesně
v téhle podobě ho publikují Claude Artifacts – obálku si přidávají samy.
Pro Pages ji musí doplnit tenhle skript, hlavně charset (bez něj se rozsype
diakritika) a viewport. <title> a <link> se přesouvají do <head>, kam patří.
"""
import pathlib, re

SRC = pathlib.Path("src/booth.html")
OUT = pathlib.Path("index.html")

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


if __name__ == "__main__":
    main()
