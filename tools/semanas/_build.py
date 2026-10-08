"""Monta os JSONs das semanas com gráficos ilustrativos. Referência de como usar temas e componentes.
Uso: python3 tools/semanas/_build.py && python3 tools/render.py tools/semanas/AAAA-MM-DD.json
"""
import json, os
D = os.path.dirname(os.path.abspath(__file__))
SW = 'arraste <span class=swipe>→</span>'
NOTE = '<div class=note>Dados ilustrativos</div>'

def line(vals, labels, zero=None, hl_last=True, fmt="{}"):
    """SVG de linha 804x340. zero = valor da linha de referência (ex.: 0)."""
    W, H, pl, pr, pt, pb = 804, 340, 10, 10, 40, 50
    lo, hi = min(vals + ([zero] if zero is not None else [])), max(vals)
    pad = (hi - lo) * .12 or 1; lo -= pad; hi += pad
    X = lambda i: pl + i * (W - pl - pr) / (len(vals) - 1)
    Y = lambda v: pt + (hi - v) * (H - pt - pb) / (hi - lo)
    pts = " ".join(f"{X(i):.0f},{Y(v):.0f}" for i, v in enumerate(vals))
    s = f'<svg viewBox="0 0 {W} {H}">'
    if zero is not None:
        s += f'<line x1="0" x2="{W}" y1="{Y(zero):.0f}" y2="{Y(zero):.0f}" stroke="#FF8A7A" stroke-width="2" stroke-dasharray="8 8"/>'
        s += f'<text x="{W-6}" y="{Y(zero)-12:.0f}" text-anchor="end" font-size="22" fill="#FF8A7A" font-family="Inter">saldo zero</text>'
    area = f"{X(0):.0f},{H-pb} " + pts + f" {X(len(vals)-1):.0f},{H-pb}"
    s += f'<polygon points="{area}" fill="rgba(54,226,201,.12)"/>'
    s += f'<polyline points="{pts}" fill="none" stroke="#36E2C9" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'
    for i, v in enumerate(vals):
        r = 9 if (hl_last and i == len(vals) - 1) else 6
        s += f'<circle cx="{X(i):.0f}" cy="{Y(v):.0f}" r="{r}" fill="#36E2C9"/>'
    i = len(vals) - 1
    s += f'<text x="{X(i)-4:.0f}" y="{Y(vals[i])-20:.0f}" text-anchor="end" font-size="28" font-weight="700" fill="#F6F9FC" font-family="Inter">{fmt.format(vals[i]).replace(".", ",")}</text>'
    for i, l in enumerate(labels):
        if l: s += f'<text x="{X(i):.0f}" y="{H-12}" text-anchor="{("start" if i==0 else "end" if i==len(labels)-1 else "middle")}" font-size="22" fill="rgba(246,249,252,.62)" font-family="Inter">{l}</text>'
    return s + "</svg>"

def hbars(rows):
    out = '<div class="chart hbars">'
    for l, w, v, hl in rows:
        out += f'<div class=row><span class=l>{l}</span><span class=t><i class="{"hl" if hl else ""}" style="--w:{w}%"></i></span><span class=v>{v}</span></div>'
    return out + "</div>"

def vbars(cols):
    out = '<div class="chart"><div class=vbars>'
    for l, h, v, hl in cols:
        out += f'<i class="{"hl" if hl else ""}" style="--h:{h}%" data-l="{l}" data-v="{v}"></i>'
    return out + "</div></div>"

W1 = [
 {"file": "2026-10-05_lucro-nao-e-caixa", "tag": "Gestão financeira", "theme": "light", "body":
  '<div class=bar></div><h1>Lucro no papel não paga <em>boleto.</em></h1>'
  '<div class=cmp><div class=box><div class=k>DRE do mês</div><div class=v>+ lucro</div><div class=s>vendas faturadas</div></div>'
  '<div class="box hl"><div class=k>Caixa do mês</div><div class=v>– saldo</div><div class=s>vendas a receber</div></div></div>'
  '<p>A empresa pode dar lucro e ficar sem dinheiro. Quem decide olhando só o resultado <b>quebra com a DRE positiva.</b></p>'},
 {"file": "2026-10-07_dashboard-1", "tag": "BI na prática", "foot": SW, "body":
  '<div class=bar></div><h1>3 perguntas que um bom dashboard responde em <em>10&nbsp;segundos.</em></h1>'
  '<p>Se você precisa abrir 4 planilhas para responder, o problema não é falta de dado.</p>'},
 {"file": "2026-10-07_dashboard-2", "tag": "Pergunta 1", "foot": SW, "body":
  '<div class=num>01</div><h2>Quanto vou ter em <em>caixa</em> daqui a 30&nbsp;dias?</h2>'
  '<div class=chart>' + line([42, 35, 18, -6, 4, 22, 31], ["hoje", "", "dia 10", "", "dia 20", "", "dia 30"], zero=0, fmt="R$ {}k") + '</div>' + NOTE},
 {"file": "2026-10-07_dashboard-3", "tag": "Pergunta 2", "foot": SW, "body":
  '<div class=num>02</div><h2>Qual produto <em>realmente</em> dá&nbsp;margem?</h2>'
  + hbars([("Produto A", 90, "38%", True), ("Produto B", 58, "24%", False), ("Produto C", 22, "9%", False), ("Produto D", 6, "2%", False)]) + NOTE},
 {"file": "2026-10-07_dashboard-4", "tag": "Pergunta 3", "foot": SW, "body":
  '<div class=num>03</div><h2>Onde o mês <em>desviou</em> do&nbsp;planejado?</h2>'
  + hbars([("Marketing", 90, "+18%", True), ("Fretes", 55, "+11%", True), ("Pessoal", 10, "+2%", False), ("Aluguel", 2, "0%", False)]) + NOTE},
 {"file": "2026-10-07_dashboard-5", "tag": "GPSBI", "theme": "light", "body":
  '<div class=bar></div><h1>Seu painel responde essas&nbsp;<em>3?</em></h1>'
  '<p>A GPSBI conecta seu ERP e suas planilhas a dashboards que <b>respondem a pergunta, não só mostram o número.</b></p>'
  '<div><span class=pill>Fale com a gente · gpsbi.com.br</span></div>'},
 {"file": "2026-10-09_planilha-nao-e-o-problema", "tag": "Visão GPSBI", "theme": "quote", "body":
  '<h1>Planilha não é o problema. <em>Decidir no escuro&nbsp;é.</em></h1>'
  '<p>A maioria das empresas que atendemos já tem os dados. Falta <b>organizar, cruzar e enxergar</b> no momento da decisão.</p>'
  '<div class=sign><b>Gustavo Silveira</b><span>fundador GPSBI</span></div>'},
]

W2 = [
 {"file": "2026-10-12_capital-de-giro", "tag": "Gestão financeira", "theme": "light", "body":
  '<div class=bar></div><h1>Você está <em>financiando</em> seu&nbsp;cliente.</h1>'
  '<div class=cmp><div class=box><div class=k>Você paga</div><div class=v>30 dias</div><div class=s>fornecedor</div></div>'
  '<div class="box hl"><div class=k>Você recebe</div><div class=v>60 dias</div><div class=s>cliente</div></div></div>'
  '<p>Nesse exemplo, são 30 dias em que o dinheiro sai do seu caixa antes de voltar. <b>Isso é capital&nbsp;de&nbsp;giro.</b></p>'},
 {"file": "2026-10-14_contas-a-receber-1", "tag": "BI na prática", "foot": SW, "body":
  '<div class=bar></div><h1>O que um painel de contas a receber <em>precisa mostrar.</em></h1>'
  '<p>Saber o total em aberto é pouco. A pergunta é: <b>quanto disso vai virar dinheiro?</b></p>'},
 {"file": "2026-10-14_contas-a-receber-2", "tag": "Visão 1", "foot": SW, "body":
  '<div class=num>01</div><h2>Vencidos por <em>faixa&nbsp;de&nbsp;atraso</em></h2>'
  + vbars([("até 30d", 92, "R$ 48k", False), ("31–60d", 55, "R$ 29k", False), ("61–90d", 30, "R$ 16k", False), ("+90d", 42, "R$ 22k", True)])
  + '<div class=note>Dados ilustrativos · quanto mais velho o atraso, menor a chance de receber</div>'},
 {"file": "2026-10-14_contas-a-receber-3", "tag": "Visão 2", "foot": SW, "body":
  '<div class=num>02</div><h2>Quem concentra o <em>valor em&nbsp;aberto</em></h2>'
  + hbars([("Cliente A", 85, "34%", True), ("Cliente B", 53, "21%", True), ("Cliente C", 30, "12%", False), ("Cliente D", 15, "6%", False), ("Outros", 68, "27%", False)])
  + '<div class=note>Dados ilustrativos · a cobrança começa pelos maiores</div>'},
 {"file": "2026-10-14_contas-a-receber-4", "tag": "Visão 3", "foot": SW, "body":
  '<div class=num>03</div><h2>A <em>tendência</em> mês a&nbsp;mês</h2>'
  '<div class=chart>' + line([6.1, 6.8, 7.4, 8.9, 10.2, 12.5], ["mai", "jun", "jul", "ago", "set", "out"], fmt="{}%") + '</div>'
  '<div class=note>Dados ilustrativos · % vencido sobre a carteira</div>'},
 {"file": "2026-10-14_contas-a-receber-5", "tag": "GPSBI", "theme": "light", "body":
  '<div class=bar></div><h1>Seu contas a receber já é <em>um&nbsp;painel?</em></h1>'
  '<p>A GPSBI conecta seu ERP a dashboards que mostram <b>o que cobrar, de quem e quando.</b></p>'
  '<div><span class=pill>Fale com a gente · gpsbi.com.br</span></div>'},
 {"file": "2026-10-16_antes-do-grafico", "tag": "Visão GPSBI", "theme": "quote", "body":
  '<h1>Todo projeto de BI começa sem <em>nenhum&nbsp;gráfico.</em></h1>'
  '<p>Começa com uma conversa: <b>quais decisões você precisa tomar</b> e o que falta saber para&nbsp;tomá-las.</p>'
  '<div class=sign><b>Gustavo Silveira</b><span>fundador GPSBI</span></div>'},
]

W3 = [
 {"file": "2026-10-19_desconto-e-margem", "tag": "Gestão financeira", "theme": "light", "body":
  '<div class=bar></div><h1>Desconto de 10% pode exigir <em>50% a mais</em> de&nbsp;vendas.</h1>'
  '<div class=cmp><div class=box><div class=k>Preço cheio</div><div class=v>R$ 30</div><div class=s>sobram por venda</div></div>'
  '<div class="box hl"><div class=k>Com 10% off</div><div class=v>R$ 20</div><div class=s>sobram por venda</div></div></div>'
  '<p>Exemplo: produto de R$ 100 com custo variável de R$ 70. Para sobrar o mesmo no fim do mês, <b>você precisa vender 50% a&nbsp;mais.</b></p>'},
 {"file": "2026-10-21_vendas-1", "tag": "BI na prática", "foot": SW, "body":
  '<div class=bar></div><h1>O faturamento subiu. Você sabe <em>por&nbsp;quê?</em></h1>'
  '<p>Mais clientes, ticket maior ou só desconto? <b>Cada resposta pede uma decisão diferente.</b></p>'},
 {"file": "2026-10-21_vendas-2", "tag": "Pergunta 1", "foot": SW, "body":
  '<div class=num>01</div><h2>Mais pedidos ou <em>ticket&nbsp;maior?</em></h2>'
  + vbars([("jun", 92, "R$ 410", False), ("jul", 86, "R$ 395", False), ("ago", 78, "R$ 372", False), ("set", 70, "R$ 350", False), ("out", 64, "R$ 338", True)])
  + '<div class=note>Dados ilustrativos · ticket médio caindo enquanto os pedidos sobem</div>'},
 {"file": "2026-10-21_vendas-3", "tag": "Pergunta 2", "foot": SW, "body":
  '<div class=num>02</div><h2>Qual linha <em>puxou</em> o&nbsp;crescimento?</h2>'
  + hbars([("Linha A", 90, "+32%", True), ("Linha B", 38, "+12%", False), ("Linha C", 14, "+4%", False), ("Linha D", 6, "–6%", False)])
  + '<div class=note>Dados ilustrativos · variação do faturamento contra o mês anterior</div>'},
 {"file": "2026-10-21_vendas-4", "tag": "Pergunta 3", "foot": SW, "body":
  '<div class=num>03</div><h2>O desconto médio está <em>subindo?</em></h2>'
  '<div class=chart>' + line([4.2, 5.1, 6.0, 7.4, 8.8, 10.3], ["mai", "jun", "jul", "ago", "set", "out"], fmt="{}%") + '</div>'
  '<div class=note>Dados ilustrativos · desconto médio sobre o preço de tabela</div>'},
 {"file": "2026-10-21_vendas-5", "tag": "GPSBI", "theme": "light", "body":
  '<div class=bar></div><h1>Seu painel de vendas mostra <em>o&nbsp;porquê?</em></h1>'
  '<p>A GPSBI conecta seu ERP a dashboards que separam <b>volume, preço e desconto</b> no mesmo&nbsp;lugar.</p>'
  '<div><span class=pill>Fale com a gente · link na bio</span></div>'},
 {"file": "2026-10-23_mesmo-numero", "tag": "Visão GPSBI", "theme": "quote", "body":
  '<h1>Quando cada área tem o seu número, a reunião vira <em>briga de&nbsp;planilha.</em></h1>'
  '<p>Antes de qualquer painel, a gente alinha <b>o que cada indicador mede</b> e de onde ele&nbsp;vem.</p>'
  '<div class=sign><b>Gustavo Silveira</b><span>fundador GPSBI</span></div>'},
]

if __name__ == "__main__":
    for name, w in (("2026-10-05", W1), ("2026-10-12", W2), ("2026-10-19", W3)):
        json.dump(w, open(os.path.join(D, name + ".json"), "w"), ensure_ascii=False, indent=1)
    print("ok")
