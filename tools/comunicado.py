"""Arte de comunicado para clientes (WhatsApp/e-mail), 1080x1350, identidade GPSBI.
Uso: python3 tools/comunicado.py  -> brand/comunicados/<arquivo>.png
Para um novo aviso, adicione um item em COMUNICADOS e rode de novo.
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import CSS, ROOT
from playwright.sync_api import sync_playwright

LOGO = base64.b64encode(open(os.path.join(ROOT, "brand/logo/gpsbi-logo-branco.png"), "rb").read()).decode()
OUT = os.path.join(ROOT, "brand/comunicados"); os.makedirs(OUT, exist_ok=True)

EXTRA = """
.wrap{inset:110px 96px 96px}
.head{display:flex;justify-content:space-between;align-items:center}
.head img{height:78px}
.date{margin-top:40px;display:flex;align-items:baseline;gap:26px}
.date .d{font-size:230px;font-weight:800;letter-spacing:-8px;line-height:.9;color:#36E2C9}
.date .m{font-size:40px;font-weight:700;line-height:1.25}
.date .m span{display:block;font-weight:400;font-size:30px;color:var(--muted);margin-top:6px}
.rows{margin-top:48px;border-top:2px solid var(--line)}
.r{display:flex;gap:28px;align-items:flex-start;padding:26px 0;border-bottom:2px solid var(--line)}
.r:last-child{border-bottom:none}
.r .ic{flex:none;width:68px;height:68px;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:800;background:rgba(54,226,201,.14);color:#36E2C9}
.r h3{font-size:36px;font-weight:700}
.r p{font-size:28px;margin-top:6px;line-height:1.35}
"""

def comunicado(tag, titulo, dia, mes, sub, rows):
    items = "".join(f'<div class=r><div class=ic>{i}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for i, t, d in rows)
    return f"""<html><head><style>{CSS}{EXTRA}</style></head><body class=dark><div class=bg></div><div class=grid></div>
<div class=wrap><div class=head><img src="data:image/png;base64,{LOGO}"><div class=tag>{tag}</div></div>
<div class=main style="justify-content:flex-start;padding-top:56px"><h2>{titulo}</h2>
<div class=date><div class=d>{dia}</div><div class=m>{mes}<span>{sub}</span></div></div>
<div class=rows>{items}</div></div>
<div class=foot><span>gpsbi.com.br</span><span>@gps.bi</span></div></div></body></html>"""

COMUNICADOS = {
 "2026-10-12_feriado-aparecida": comunicado(
   "Comunicado", "Aviso de <em>feriado</em>", "12", "de outubro · segunda-feira",
   "Nossa Senhora Aparecida e Dia das Crianças",
   [("✕", "Sem expediente", "Não haverá atendimento no dia 12/10."),
    ("✓", "Seu BI segue atualizado", "Atualização e envio normais, sem interrupção."),
    ("$", "Sem expediente bancário", "Títulos desse período: antecipar para <b>09/10</b> ou postergar para <b>13/10</b>.")]),
}

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for k, html in COMUNICADOS.items():
            pg.set_content(html); pg.wait_for_timeout(150); pg.screenshot(path=f"{OUT}/{k}.png"); print(k)
        b.close()
