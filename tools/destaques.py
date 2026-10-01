"""Stories (1080x1920) e capas (1080x1080) dos destaques do @gps.bi.
Uso: python3 tools/destaques.py  -> gera em brand/destaques/
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import CSS, SETA_BRANCO, SETA_COR, ROOT
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, "brand/destaques"); os.makedirs(OUT, exist_ok=True)

STORY_CSS = CSS + """
body{width:1080px;height:1920px}
.wrap{inset:150px 96px 200px}
.item{display:flex;gap:32px;align-items:flex-start;padding:36px 0;border-bottom:2px solid var(--line)}
.item:last-child{border-bottom:none}
.ic{flex:none;width:76px;height:76px;border-radius:22px;background:rgba(54,226,201,.14);color:#36E2C9;display:flex;align-items:center;justify-content:center;font-size:38px;font-weight:800}
.item h3{font-size:44px;font-weight:800;letter-spacing:-.5px}
.item div p{font-size:32px;margin-top:10px}
.big{font-size:84px;font-weight:800;letter-spacing:-1px;color:#36E2C9;margin-top:24px}
"""

def story(tag, body, theme="dark"):
    seta = SETA_COR if theme == "light" else SETA_BRANCO
    return f"""<html><head><style>{STORY_CSS}</style></head><body class="{theme}"><div class=bg></div><div class=grid></div>
<div class=wrap><div class=top><img class=logo src="data:image/png;base64,{seta}"><div class=tag>{tag}</div></div>
<div class=main>{body}</div><div class=foot><span>gpsbi.com.br</span><span>@gps.bi</span></div></div></body></html>"""

def items(rows):
    return "".join(f'<div class=item><div class=ic>{i}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for i, t, d in rows)

STORIES = {
 "1_servicos": story("Serviços", '<div class=bar></div><h1>O que a GPSBI <em>faz.</em></h1><div style="margin-top:56px">' + items([
   ("$", "Fluxo de caixa gerencial", "Realizado e projetado, dia a dia, para enxergar o caixa antes de faltar."),
   ("≡", "DRE gerencial", "Resultado por mês, por unidade e por categoria, no plano de contas da sua empresa."),
   ("▥", "Dashboards de BI", "Comercial, financeiro e estoque em um painel só, atualizado."),
   ("⇄", "Integração de dados", "Conectamos seu ERP e suas planilhas. Sem retrabalho manual."),
 ]) + "</div>"),
 "2_como-funciona": story("Como funciona", '<div class=bar></div><h1>Do diagnóstico ao <em>painel.</em></h1><div style="margin-top:56px">' + items([
   ("1", "Diagnóstico", "Entendemos quais decisões você precisa tomar e o que falta saber."),
   ("2", "Organização dos dados", "Conectamos e padronizamos ERP, planilhas e plano de contas."),
   ("3", "Painel sob medida", "Indicadores que respondem às suas perguntas, não ao modelo pronto."),
   ("4", "Acompanhamento", "Ajustes e suporte para o painel virar rotina de gestão."),
 ]) + "</div>"),
 "3_por-que-gpsbi": story("Por que GPSBI", '<div class=bar></div><h1>Finanças e dados <em>na mesma mesa.</em></h1><div style="margin-top:56px">' + items([
   ("✓", "Começamos pela decisão", "Primeiro o que você precisa decidir. O gráfico vem depois."),
   ("✓", "Entendemos de finanças", "Fluxo de caixa, DRE e margem não são só números para nós."),
   ("✓", "Um painel, não 4 planilhas", "Tudo que importa no mesmo lugar, atualizado."),
   ("✓", "Perto de você", "Suporte próximo até o painel virar rotina de gestão."),
 ]) + "</div>"),
 "4_contato": story("Contato", '<div class=bar></div><h1>Diagnóstico <em>gratuito.</em></h1><p>Uma conversa para entender seus números e onde um painel faz diferença na sua gestão.</p>'
   '<p style="margin-top:80px">Chama no WhatsApp:</p><div class=big>(11) 99812-5961</div>'
   '<p style="margin-top:60px">Ou toque no <b>link da bio</b> 👆</p>'),
}

ICONS = {  # capas: ícone simples branco
 "1_servicos": '<rect x="0" y="0" width="44" height="44" rx="10"/><rect x="56" y="0" width="44" height="44" rx="10"/><rect x="0" y="56" width="44" height="44" rx="10"/><rect x="56" y="56" width="44" height="44" rx="10" fill="#36E2C9"/>',
 "2_como-funciona": '<circle cx="12" cy="50" r="12"/><circle cx="50" cy="50" r="12"/><circle cx="88" cy="50" r="12" fill="#36E2C9"/><rect x="12" y="47" width="76" height="6"/>',
 "3_por-que-gpsbi": '<path d="M10 52 L38 80 L92 20" fill="none" stroke="#36E2C9" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>',
 "4_contato": '<path d="M10 10 H90 Q100 10 100 20 V66 Q100 76 90 76 H40 L18 96 V76 H10 Q0 76 0 66 V20 Q0 10 10 10 Z"/><circle cx="30" cy="43" r="7" fill="#071B33"/><circle cx="50" cy="43" r="7" fill="#071B33"/><circle cx="70" cy="43" r="7" fill="#36E2C9"/>',
}

def cover(svg):
    return f'<html><body style="margin:0;width:1080px;height:1080px;background:#071B33;display:flex;align-items:center;justify-content:center"><svg viewBox="-10 -10 120 120" width="420" height="420" fill="#F6F9FC">{svg}</svg></body></html>'

if __name__ == "__main__":
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for k, html in STORIES.items():
            pg.set_content(html); pg.wait_for_timeout(150); pg.screenshot(path=f"{OUT}/story_{k}.png"); print(k)
        pg = b.new_page(viewport={"width": 1080, "height": 1080})
        for k, svg in ICONS.items():
            pg.set_content(cover(svg)); pg.wait_for_timeout(100); pg.screenshot(path=f"{OUT}/capa_{k}.png")
        b.close()
