#!/usr/bin/env python3
"""Z src/booth.html vyrobí pro každý stánek z booths/*.json stránku
stanek-<id>/index.html a manifest stanek-<id>/assets/panels.json,
a k tomu rozcestník index.html v kořeni.

src/booth.html je holý obsah stránky bez <!doctype> a <head>, protože přesně
v téhle podobě ho publikují Claude Artifacts – obálku si přidávají samy.
Pro Pages ji musí doplnit tenhle skript, hlavně charset (bez něj se rozsype
diakritika) a viewport. <title> a <link> se přesouvají do <head>, kam patří,
a do <head> přibude konfigurace stánku jako window.BOOTH.
"""
import html, json, pathlib, re

SRC = pathlib.Path("src/booth.html")
BOOTHS = pathlib.Path("booths")

# jak se smí jmenovat soubor pro daný panel (bez přípony)
PANEL_NAMES = {
    "back":    ("back", "zadni", "zadni-stena", "stena"),
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
<meta name="description" content="Interaktivní 3D náhled výstavního stánku: nahraj grafiku a zkontroluj rozlišení a poměr stran.">
<style>
:root{color-scheme:light dark;
  padding-top:env(safe-area-inset-top,0px); padding-bottom:env(safe-area-inset-bottom,0px)}
html,body{margin:0}
body{font:14px system-ui,-apple-system,sans-serif}
img{max-width:100%}
[hidden]{display:none!important}
</style>"""

LANDING = """<!doctype html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ModernTV stánky</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..700&family=IBM+Plex+Sans:wght@400;600&display=swap">
<style>
:root{color-scheme:light dark; --bg:#F5F2ED; --surface:#FFFFFF; --line:#DAD3C9; --text:#1A1613; --dim:#665E55; --accent:#9E550C; --accent-bright:#E4883C}
@media (prefers-color-scheme: dark){:root{--bg:#14120F; --surface:#1C1A16; --line:#39332B; --text:#EFEAE3; --dim:#A49A8D; --accent:#EFA05C}}
body{margin:0; background:var(--bg); color:var(--text); font:15px/1.5 "IBM Plex Sans", system-ui, sans-serif}
main{max-width:560px; margin:0 auto; padding:48px 16px}
h1{font-family:"Archivo", system-ui, sans-serif; font-stretch:112%; font-size:26px; margin:0 0 24px; letter-spacing:-.01em}
a{display:block; padding:14px 16px; margin-bottom:10px; border:1px solid var(--line); border-radius:10px;
  background:var(--surface); color:inherit; text-decoration:none}
a:hover, a:focus-visible{border-color:var(--accent-bright); outline:none}
b{display:block; font-weight:600}
span{font-size:13px; color:var(--dim)}
</style>
</head>
<body>
<main>
<h1>ModernTV stánky</h1>
{links}
</main>
</body>
</html>
"""


def scan_dir(d, out, panels, notes):
    """Panelové soubory v jedné složce -> {panel: cesta relativně ke stránce stánku}."""
    lookup = {name: pid for pid, names in PANEL_NAMES.items() for name in names}
    found = {}
    for f in sorted(d.glob("*")) if d.is_dir() else []:
        if f.suffix.lower() not in EXTS:
            continue
        pid = lookup.get(f.name[: -len(f.suffix)].lower())
        if pid is None or pid not in panels:
            notes.append(f"  ! {f.relative_to(out)} – název neodpovídá žádnému panelu stánku, přeskočeno")
            continue
        if pid in found:
            notes.append(f"  ! {f.relative_to(out)} – pro panel {pid} už soubor je, přeskočeno")
            continue
        size = f.stat().st_size
        if size >= GH_LIMIT:
            notes.append(f"  ! {f.relative_to(out)} – {size/1024**2:.0f} MB, GitHub to odmítne (limit 100 MB)")
            continue
        if size >= GH_WARN:
            notes.append(f"  ~ {f.relative_to(out)} – {size/1024**2:.0f} MB, GitHub bude varovat; zmenši náhled")
        found[pid] = f.relative_to(out).as_posix()
        notes.append(f"  + {pid:<8} {f.relative_to(out)} ({size/1024:,.0f} kB)")
    return found


def scan_assets(out, cfg):
    """Poskládá <stánek>/assets/panels.json. Verze (cfg.versions; první = základ, tedy
    assets/) přebíjejí soubory podsložkou assets/<verze>/."""
    panels, assets, notes = cfg["panels"], out / "assets", []
    found = scan_dir(assets, out, panels, notes)
    vers = {}
    for v in cfg.get("versions", [])[1:]:
        o = scan_dir(assets / v, out, panels, notes)
        if o:
            vers[v] = o
    if vers:
        found["versions"] = vers

    assets.mkdir(parents=True, exist_ok=True)
    (assets / "panels.json").write_text(json.dumps(found, indent=2, ensure_ascii=False) + "\n",
                                        encoding="utf-8")
    return found, notes


def build_booth(src, cfg):
    out = pathlib.Path("stanek-" + cfg["id"])
    out.mkdir(exist_ok=True)

    # souvislý blok hlavičkových tagů na začátku souboru patří do <head>
    prefix_end = 0
    for m in HEAD_TAGS.finditer(src):
        if m.start() != prefix_end:
            break
        prefix_end = m.end()
    head = [m.group(0).strip() for m in HEAD_TAGS.finditer(src[:prefix_end])]
    head = [f"<title>{html.escape(cfg['title'])}</title>" if t.lower().startswith("<title>") else t
            for t in head]
    body = src[prefix_end:].lstrip("\n")
    # "</" uvnitř <script> by ho ukončilo
    booth = json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/")

    doc = ("<!doctype html>\n<html lang=\"cs\">\n<head>\n"
           + RESET + "\n"
           + "\n".join(head) + "\n"
           + f"<script>window.BOOTH = {booth};</script>\n"
           + "</head>\n<body>\n"
           + body.rstrip() + "\n</body>\n</html>\n")
    page = out / "index.html"
    page.write_text(doc, encoding="utf-8")
    print(f"{page} ({page.stat().st_size:,} B), do <head> přesunuto tagů: {len(head)}")

    found, notes = scan_assets(out, cfg)
    print(f"{out}/assets/panels.json: {len([k for k in found if k != 'versions'])} z {len(cfg['panels'])} panelů má grafiku v repozitáři")
    for n in notes:
        print(n)
    return out


def main():
    src = SRC.read_text(encoding="utf-8")
    links = []
    for f in sorted(BOOTHS.glob("*.json")):
        cfg = json.loads(f.read_text(encoding="utf-8"))
        out = build_booth(src, cfg)
        links.append(f'<a href="{out}/"><b>{html.escape(cfg["title"])}</b>'
                     f'<span>{html.escape(cfg["sub"])}</span></a>')
    pathlib.Path("index.html").write_text(LANDING.replace("{links}", "\n".join(links)),
                                          encoding="utf-8")
    print(f"index.html: rozcestník, stánků {len(links)}")


if __name__ == "__main__":
    main()
