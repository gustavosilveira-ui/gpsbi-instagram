"""Gerador de artes GPSBI (PNG 1080x1350).
Uso: python3 tools/render.py tools/semanas/AAAA-MM-DD.json
O JSON é uma lista de slides:
  {"file": "AAAA-MM-DD_tema", "tag": "Gestão financeira", "theme": "dark|light|quote", "body": "<html>", "foot": "@gps.bi" (opcional)}
Temas (alternar para o grid não ficar repetitivo):
  light -> fundo claro, seta colorida, destaque tipo marca-texto. Padrão de SEGUNDA (gestão financeira).
  dark  -> fundo azul, seta branca. Padrão de QUARTA (carrossel BI), com gráficos ilustrativos.
  quote -> fundo azul, seta gigante d'água, frase de autoridade + assinatura. Padrão de SEXTA.
Componentes para o body:
  .bar, h1/h2 (com <em> de destaque), p (com <b>), .num, .pill, .note (rodapé "dados ilustrativos")
  .cmp > .box(.hl) > .k/.v/.s                        -> comparação lado a lado
  .chart > .vbars > <i style="--h:70%" data-l="rótulo" data-v="valor" class="hl?">   -> barras verticais
  .chart > .hbars > .row > span.l + i(style="--w:60%", class hl?) + span.v           -> ranking horizontal
  .chart > svg (linha)                               -> use tools/semanas/_build.py como referência
  .sign > b + span                                   -> assinatura (tema quote)
Requer: playwright (chromium) e `npm i @fontsource/inter@5` dentro de tools/ (instala sozinho).
"""
import os, sys, json, base64, subprocess
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
F = os.path.join(D, "node_modules/@fontsource/inter/files")
if not os.path.isdir(F):
    subprocess.run(["npm", "i", "@fontsource/inter@5", "--silent", "--prefix", D], check=True)

def b64(path):
    return base64.b64encode(open(os.path.join(ROOT, path), "rb").read()).decode()

SETA_BRANCO = b64("brand/logo/gpsbi-seta-branco.png")
SETA_COR = b64("brand/logo/gpsbi-seta-cor.png")

def font(w):
    b = base64.b64encode(open(f"{F}/inter-latin-{w}-normal.woff2", "rb").read()).decode()
    return f"@font-face{{font-family:Inter;font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2');}}"

CSS = "".join(font(w) for w in (400, 600, 700, 800)) + """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:Inter;overflow:hidden;position:relative;
 --bg:#071B33;--fg:#F6F9FC;--muted:rgba(246,249,252,.62);--body:rgba(246,249,252,.84);--acc:#36E2C9;
 --line:rgba(246,249,252,.10);--card:rgba(246,249,252,.05);--track:rgba(246,249,252,.08);
 color:var(--fg);background:var(--bg)}
.bg{position:absolute;inset:0;background:radial-gradient(900px 700px at 100% 0%, rgba(54,226,201,.16), transparent 60%),radial-gradient(800px 600px at 0% 100%, #0B2545, transparent 70%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:60px 60px;opacity:.4}
.wm{display:none}
.wrap{position:absolute;inset:96px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;align-items:center}
.logo{height:104px}
.tag{color:var(--acc);font-size:26px;text-transform:uppercase;letter-spacing:3px;font-weight:700}
.main{flex:1;display:flex;flex-direction:column;justify-content:center}
h1{font-size:96px;line-height:1.04;font-weight:800;letter-spacing:-2px}
h2{font-size:68px;line-height:1.08;font-weight:800;letter-spacing:-1.5px}
h1 em,h2 em{font-style:normal;color:var(--acc)}
p{font-size:38px;line-height:1.4;color:var(--body);margin-top:40px}
p b{color:var(--fg);font-weight:700}
.bar{width:120px;height:8px;border-radius:4px;background:var(--acc);margin-bottom:48px}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:26px;color:var(--muted)}
.num{font-size:150px;font-weight:800;color:var(--acc);line-height:1;letter-spacing:-5px;margin-bottom:20px}
.pill{display:inline-block;border:2px solid var(--acc);color:var(--acc);border-radius:999px;padding:14px 30px;font-size:28px;font-weight:600;margin-top:56px}
.note{font-size:22px;color:var(--muted);margin-top:18px;letter-spacing:.5px}
.swipe{color:var(--acc);font-weight:700}
.cmp{display:flex;gap:28px;margin-top:60px}
.box{flex:1;border-radius:28px;padding:40px;background:var(--card);border:2px solid var(--line)}
.box.hl{border-color:var(--acc);background:rgba(54,226,201,.10)}
.box .k{font-size:26px;text-transform:uppercase;letter-spacing:2px;color:var(--muted);font-weight:600}
.box .v{font-size:64px;font-weight:800;margin-top:14px}
.box .s{font-size:26px;color:var(--muted);margin-top:10px}
/* gráficos */
.chart{margin-top:48px;border-radius:28px;padding:40px 40px 28px;background:var(--card);border:2px solid var(--line)}
.vbars{display:flex;align-items:flex-end;gap:28px;height:330px}
.vbars i{flex:1;height:var(--h);background:rgba(246,249,252,.22);border-radius:12px 12px 4px 4px;position:relative}
.vbars i.hl{background:var(--acc)}
.vbars i::before{content:attr(data-v);position:absolute;top:-44px;left:0;right:0;text-align:center;font-style:normal;font-size:28px;font-weight:700;color:var(--fg)}
.vbars i::after{content:attr(data-l);position:absolute;bottom:-46px;left:-10px;right:-10px;text-align:center;font-style:normal;font-size:23px;color:var(--muted);white-space:nowrap}
.vbars{margin:48px 0 52px}
.hbars .row{display:flex;align-items:center;gap:20px;margin:16px 0}
.hbars .l{width:210px;font-size:27px;color:var(--body)}
.hbars .t{flex:1;height:34px;background:var(--track);border-radius:8px;overflow:hidden}
.hbars i{display:block;height:100%;width:var(--w);background:rgba(246,249,252,.30);border-radius:8px}
.hbars i.hl{background:var(--acc)}
.hbars .v{width:110px;text-align:right;font-size:28px;font-weight:700}
.chart svg{display:block;width:100%}
.sign{display:flex;align-items:center;gap:22px;margin-top:64px;font-size:28px;color:var(--muted)}
.sign::before{content:"";width:64px;height:3px;background:var(--acc)}
.sign b{color:var(--fg);font-weight:700}
/* tema claro */
body.light{--bg:#F6F9FC;--fg:#071B33;--muted:#5B6B7F;--body:#33475B;--acc:#0B2545;--line:#DDE5EE;--card:#FFFFFF;--track:#E8EEF5}
body.light .bg{background:radial-gradient(900px 700px at 100% 0%, rgba(54,226,201,.18), transparent 60%)}
body.light .grid{opacity:.7}
body.light h1 em,body.light h2 em{color:#071B33;background:linear-gradient(transparent 60%, rgba(54,226,201,.65) 60%)}
body.light .bar,body.light .sign::before{background:#36E2C9}
body.light .tag{color:#0B2545}
body.light .num{color:#36E2C9}
body.light .box.hl{border-color:#36E2C9;background:rgba(54,226,201,.12)}
body.light .vbars i{background:#C9D4E1} body.light .vbars i.hl{background:#36E2C9}
body.light .hbars i{background:#C9D4E1} body.light .hbars i.hl{background:#36E2C9}
body.light .pill{border-color:#0B2545;color:#0B2545}
/* tema citação */
body.quote .bg{background:linear-gradient(160deg,#0B2545 0%,#071B33 70%)}
body.quote .grid{display:none}
body.quote .wm{display:block;position:absolute;right:-160px;top:280px;height:900px;opacity:.07}
body.quote .main{justify-content:flex-end;padding-bottom:40px}
body.quote h1{font-size:88px}
body.quote h1::before{content:"\\201C";display:block;font-size:200px;line-height:.6;color:#36E2C9;margin-bottom:24px}
"""

def page(tag, body, foot_right="@gps.bi", theme="dark"):
    seta = SETA_COR if theme == "light" else SETA_BRANCO
    return f"""<html><head><style>{CSS}</style></head><body class="{theme}"><div class=bg></div><div class=grid></div>
<img class=wm src="data:image/png;base64,{SETA_BRANCO}">
<div class=wrap><div class=top><img class=logo src="data:image/png;base64,{seta}"><div class=tag>{tag}</div></div>
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
            pg.set_content(page(s["tag"], s["body"], s.get("foot", "@gps.bi"), s.get("theme", "dark"))); pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(out, s["file"] + ".png")); print(s["file"])
        b.close()
