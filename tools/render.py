"""Gerador de artes GPSBI (PNG 1080x1350).
Uso: python3 tools/render.py tools/semanas/AAAA-MM-DD.json
O JSON é uma lista de {"file": "AAAA-MM-DD_tema", "tag": "Gestão financeira", "body": "<html>", "foot": "@gps.bi" opcional}.
Requer: pip playwright (chromium) e `npm i @fontsource/inter@5` dentro de tools/.
Classes disponíveis no body: .bar, h1/h2 (com <em> em ciano), p (com <b>), .num, .pill, .cmp > .box(.hl) > .k/.v/.s, .swipe
"""
import os, sys, json, base64, subprocess
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
F = os.path.join(D, "node_modules/@fontsource/inter/files")
if not os.path.isdir(F):
    subprocess.run(["npm", "i", "@fontsource/inter@5", "--silent", "--prefix", D], check=True)
LOGO = base64.b64encode(open(os.path.join(ROOT, "brand/logo/gpsbi-logo-branco.png"), "rb").read()).decode()

def font(w):
    b = base64.b64encode(open(f"{F}/inter-latin-{w}-normal.woff2", "rb").read()).decode()
    return f"@font-face{{font-family:Inter;font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2');}}"

CSS = "".join(font(w) for w in (400, 600, 700, 800)) + """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:Inter;color:#F6F9FC;background:#071B33;overflow:hidden;position:relative}
.bg{position:absolute;inset:0;background:
 radial-gradient(900px 700px at 100% 0%, rgba(54,226,201,.16), transparent 60%),
 radial-gradient(800px 600px at 0% 100%, rgba(11,37,69,1), transparent 70%);}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(246,249,252,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(246,249,252,.04) 1px,transparent 1px);background-size:60px 60px}
.wrap{position:absolute;inset:96px 96px 96px 96px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:28px;letter-spacing:.5px}
.brand{display:flex;align-items:center;gap:12px;font-weight:800;font-size:34px;letter-spacing:1px}
.dot{width:18px;height:18px;border-radius:50%;background:linear-gradient(135deg,#36E2C9,#0B2545);box-shadow:0 0 18px rgba(54,226,201,.6)}
.logo{height:84px}
.tag{color:#36E2C9;font-size:26px;text-transform:uppercase;letter-spacing:3px;font-weight:700}
.main{flex:1;display:flex;flex-direction:column;justify-content:center}
h1{font-size:96px;line-height:1.04;font-weight:800;letter-spacing:-2px}
h1 em{font-style:normal;color:#36E2C9}
h2{font-size:72px;line-height:1.08;font-weight:800;letter-spacing:-1.5px}
h2 em{font-style:normal;color:#36E2C9}
p{font-size:38px;line-height:1.4;color:rgba(246,249,252,.82);font-weight:400;margin-top:44px}
p b{color:#F6F9FC;font-weight:700}
.bar{width:120px;height:8px;border-radius:4px;background:#36E2C9;margin-bottom:48px}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:26px;color:rgba(246,249,252,.6)}
.num{font-size:200px;font-weight:800;color:#36E2C9;line-height:1;letter-spacing:-6px;margin-bottom:24px}
.pill{display:inline-block;border:2px solid rgba(54,226,201,.5);color:#36E2C9;border-radius:999px;padding:14px 30px;font-size:28px;font-weight:600;margin-top:56px}
.cmp{display:flex;gap:28px;margin-top:64px}
.box{flex:1;border-radius:28px;padding:40px;background:rgba(246,249,252,.05);border:2px solid rgba(246,249,252,.1)}
.box.hl{border-color:#36E2C9;background:rgba(54,226,201,.08)}
.box .k{font-size:26px;text-transform:uppercase;letter-spacing:2px;color:rgba(246,249,252,.6);font-weight:600}
.box .v{font-size:64px;font-weight:800;margin-top:14px}
.box .s{font-size:26px;color:rgba(246,249,252,.6);margin-top:10px}
.swipe{color:#36E2C9;font-weight:700}
"""

def page(tag, body, foot_right="@gps.bi"):
    return f"""<html><head><style>{CSS}</style></head><body><div class=bg></div><div class=grid></div>
<div class=wrap><div class=top><img class=logo src="data:image/png;base64,{LOGO}"><div class=tag>{tag}</div></div>
<div class=main>{body}</div>
<div class=foot><span>gpsbi.com.br</span><span>{foot_right}</span></div></div></body></html>"""


if __name__ == "__main__":
    slides = json.load(open(sys.argv[1]))
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for s in slides:
            month = s["file"][:7]
            out = os.path.join(ROOT, "posts", month); os.makedirs(out, exist_ok=True)
            pg.set_content(page(s["tag"], s["body"], s.get("foot", "@gps.bi"))); pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(out, s["file"] + ".png")); print(s["file"])
        b.close()
