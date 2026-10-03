"""Stories diários (1080x1920) do @gps.bi.
Uso: python3 tools/stories.py AAAA-MM-DD   (segunda da semana) -> gera posts/AAAA-MM/stories/*.png
Cada semana é um dict em SEMANAS: {arquivo: (tag, body_html)}.
Formato da semana: seg dica · ter mito-ou-verdade (pergunta 12h, resposta 18h) · qua chamada pro carrossel
· qui termo da semana · sex reflexão do Gustavo · sáb resumo da semana · dom nada.
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from destaques import story
from render import ROOT
from playwright.sync_api import sync_playwright

def img(path, w=640):
    b = base64.b64encode(open(os.path.join(ROOT, path), "rb").read()).decode()
    return f'<img src="data:image/png;base64,{b}" style="width:{w}px;border-radius:28px;box-shadow:0 30px 80px rgba(0,0,0,.45);margin-top:60px">'

SEMANAS = {
 "2026-10-05": {
  "2026-10-05_story-dica": ("Dica rápida",
    '<div class=bar></div><h1>Antes de comemorar o <em>lucro</em> do mês…</h1>'
    '<p style="font-size:46px">…confere quanto dele <b>já entrou no caixa.</b></p>'
    '<p>Lucro é resultado. Caixa é o dinheiro que paga as contas amanhã.</p>'),
  "2026-10-06_story-mito-1": ("Mito ou verdade?",
    '<div class=bar></div><h1>"Se a empresa vende mais, o caixa <em>melhora.</em>"</h1>'
    '<p style="font-size:46px;margin-top:80px"><b>Mito ou verdade?</b></p><p>A resposta sai hoje às 18h 👀</p>'),
  "2026-10-06_story-mito-2": ("Resposta",
    '<div class=big style="font-size:150px;margin:0 0 30px">MITO.</div>'
    '<h2>Vender mais <em>a prazo</em> pode consumir caixa.</h2>'
    '<p>O fornecedor e a equipe são pagos antes de o cliente pagar você. Quanto mais cresce, mais dinheiro fica parado no meio do caminho.</p>'),
  "2026-10-07_story-post-novo": ("Post novo no feed",
    '<h2>3 perguntas que um bom dashboard responde em <em>10 segundos.</em></h2>'
    + '<div style="text-align:center">' + img("posts/2026-10/2026-10-07_dashboard-1.png", 560) + '</div>'
    '<p style="text-align:center">Toca no perfil e arrasta o carrossel ➡️</p>'),
  "2026-10-08_story-termo": ("Termo da semana",
    '<div class=bar></div><h1>Margem de <em>contribuição</em></h1>'
    '<p style="font-size:42px">Quanto sobra de cada venda depois dos custos e despesas <b>variáveis</b>.</p>'
    '<p>É ela que paga a estrutura fixa e, no fim, vira lucro. Produto que vende muito com margem baixa pode estar trabalhando contra você.</p>'),
  "2026-10-09_story-reflexao": ("Reflexão",
    '<h1 style="font-size:84px">Número não serve para assustar. Serve para <em>decidir antes</em> do problema aparecer.</h1>'
    '<div class=sign><b>Gustavo Silveira</b><span>fundador GPSBI</span></div>'),
  "2026-10-10_story-resumo": ("Resumo da semana",
    '<div class=bar></div><h1>Perdeu algum? <em>Tá no feed.</em></h1><div style="margin-top:56px">'
    '<div class=item><div class=ic>1</div><div><h3>Lucro no papel não paga boleto</h3><p>DRE x caixa</p></div></div>'
    '<div class=item><div class=ic>2</div><div><h3>3 perguntas de um bom dashboard</h3><p>Caixa, margem e desvio</p></div></div>'
    '<div class=item><div class=ic>3</div><div><h3>Planilha não é o problema</h3><p>Decidir no escuro é</p></div></div>'
    '</div><p>Bom fim de semana! 👋</p>'),
 },
}

SEMANAS["extra-2026-10-03"] = {
  "2026-10-03_story-vem-ai": ("A partir de segunda",
    '<div class=bar></div><h1>Toda semana, conteúdo para <em>decidir melhor.</em></h1><div style="margin-top:56px">'
    '<div class=item><div class=ic>S</div><div><h3>Segunda</h3><p>Gestão financeira na prática</p></div></div>'
    '<div class=item><div class=ic>Q</div><div><h3>Quarta</h3><p>BI e dados, em carrossel</p></div></div>'
    '<div class=item><div class=ic>S</div><div><h3>Sexta</h3><p>Bastidores e visão de quem vive os projetos</p></div></div>'
    '</div><p>E stories todo dia. <b>Ativa as notificações</b> 🔔</p>'),
  "2026-10-04_story-pergunta": ("Pergunta de domingo",
    '<h1>Você sabe quanto vai ter em <em>caixa</em> daqui a 30&nbsp;dias?</h1>'
    '<p style="font-size:44px;margin-top:60px">Se a resposta foi "mais ou menos"…</p>'
    '<p><b>Amanhã às 10h</b> tem post sobre isso no feed. 👀</p>'),
}

if __name__ == "__main__":
    semana = sys.argv[1]
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        for f, (tag, body) in SEMANAS[semana].items():
            out = os.path.join(ROOT, "posts", f[:7], "stories"); os.makedirs(out, exist_ok=True)
            theme = "quote" if "reflexao" in f else "light" if any(k in f for k in ("mito-1", "termo", "resumo", "vem-ai")) else "dark"
            pg.set_content(story(tag, body, theme)); pg.wait_for_timeout(150)
            pg.screenshot(path=os.path.join(out, f + ".png")); print(f)
        b.close()
