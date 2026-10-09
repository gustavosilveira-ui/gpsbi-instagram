# Guia editorial — Instagram @gps.bi

## Rotina semanal
- 3 posts por semana: **segunda, quarta e sexta, às 10h** (America/Sao_Paulo). São os melhores horários do perfil segundo o Metricool.
- Os posts sempre entram no Metricool como **rascunho** (`draft: true`). O Gustavo revisa e agenda. Nunca publicar direto.
- Metricool: brandId `7177912`, rede `instagram`, tipo `POST`.
- As imagens vão por link raw público: `https://raw.githubusercontent.com/gustavosilveira-ui/gpsbi-instagram/main/posts/AAAA-MM/arquivo.png`
- Sempre preencher `mediaAltText` (um por imagem).

## Pilares
- **Segunda, gestão financeira na prática:** fluxo de caixa, DRE, margem, capital de giro, inadimplência, precificação. Card único.
- **Quarta, BI e dados:** carrossel de 4 a 6 telas. Como um dashboard responde uma pergunta de negócio. Dados sempre fictícios.
- **Sexta, autoridade e bastidores:** visão do fundador, erros comuns vistos nos projetos (sem nomes), como a GPSBI trabalha. Assinado "— Gustavo Silveira, fundador da GPSBI".

## Regras (inegociáveis)
- Nenhum nome, dado, número ou print de cliente sem autorização por escrito.
- Não inventar estatísticas de mercado nem números "da GPSBI". Usar exemplos claramente ilustrativos.
- Omie: falar "integração homologada", nunca "parceria".
- Não prometer resultado financeiro.
- Tom: direto, próximo, dono de PME como público. Português do Brasil. Frases curtas. No máximo 2–3 emojis por legenda.
- Legenda: gancho na 1ª linha, desenvolvimento curto, CTA (comentar, arrastar ou "link na bio"), de 5 a 7 hashtags, sempre incluindo #GPSBI.

## Arte
- Gerador: `python3 tools/render.py tools/semanas/AAAA-MM-DD.json` (AAAA-MM-DD = segunda da semana). Leia o docstring de tools/render.py e use tools/semanas/_build.py como modelo (ele tem helpers de gráfico de linha, barras verticais e ranking).
- Marca: **só a seta** (sem escrever "Gpsbi"), já embutida no gerador. Seta colorida no tema claro, branca nos escuros.
- **Variar os modelos para o grid não ficar repetitivo** (decisão do Gustavo):
  - Segunda → tema `light` (fundo claro, destaque marca-texto ciano).
  - Quarta → carrossel tema `dark`: capa tipográfica; telas internas SEMPRE com um gráfico ilustrativo (linha, barras ou ranking) e a nota "Dados ilustrativos"; última tela (CTA) em `light`.
  - Sexta → tema `quote` (citação + assinatura do Gustavo).
- Números em formato brasileiro (vírgula decimal, R$).
- Sem fotos por enquanto (decisão do Gustavo em 01/10/2026).
- Paleta: Azul #071B33, Azul 2 #0B2545, Ciano #36E2C9, Branco #F6F9FC. Fonte Inter.
- Formato 1080x1350. Nome: `AAAA-MM-DD_tema.png`, carrossel `AAAA-MM-DD_tema-1.png`, `-2.png`...
- Depois de gerar, abrir cada PNG e conferir se há texto cortado, palavra solta numa linha ou sobreposição.

## Histórico de temas (não repetir; acrescentar a cada semana)
| Semana | Seg | Qua | Sex |
|---|---|---|---|
| 2026-10-05 | Lucro no papel não paga boleto (DRE x caixa) | 3 perguntas que um bom dashboard responde | Planilha não é o problema |
| 2026-10-12 | Você está financiando seu cliente (capital de giro / prazos) | O que um painel de contas a receber precisa mostrar | Todo projeto de BI começa sem nenhum gráfico |
| 2026-10-19 | Desconto de 10% pode exigir 50% a mais de vendas (desconto x margem) | O faturamento subiu. Você sabe por quê? (ticket, mix, desconto) | Cada área com seu número vira briga de planilha (alinhar indicadores) |

## Stories (desde 05/10/2026)
- **Stories não podem parar nunca** (decisão do Gustavo em 09/10/2026): toda semana com feed precisa ter os stories prontos junto. Ao preparar uma semana, confira também se as semanas anteriores já agendadas têm stories.
- 1 por dia útil + 1 no sábado; domingo sem story. Gerador: `python3 tools/stories.py AAAA-MM-DD` (adicione a semana no dict SEMANAS, siga o modelo de 2026-10-05).
- Seg 12h dica rápida (dark) · Ter 12h "Mito ou verdade?" (light) + 18h resposta (dark) · Qua 12h "Post novo no feed" com miniatura da capa do carrossel (dark) · Qui 12h termo da semana (light) · Sex 12h reflexão do Gustavo (quote) · Sáb 11h resumo da semana (light).
- Metricool: instagramData {"type":"STORY"}, sem texto, mediaAltText preenchido, draft true até o Gustavo aprovar.
- A API não coloca adesivos (enquete, pergunta, link); isso o Gustavo faz pelo app quando quiser.
