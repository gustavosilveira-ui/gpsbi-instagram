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
- Gerador: `python3 tools/render.py tools/semanas/AAAA-MM-DD.json` (AAAA-MM-DD = segunda da semana). Usar o JSON de 2026-10-05 como modelo de layout e classes.
- Paleta: Azul #071B33, Azul 2 #0B2545, Ciano #36E2C9, Branco #F6F9FC. Fonte Inter. Logo branca no topo (já embutida no gerador).
- Formato 1080x1350. Nome: `AAAA-MM-DD_tema.png`, carrossel `AAAA-MM-DD_tema-1.png`, `-2.png`...
- Depois de gerar, abrir cada PNG e conferir se há texto cortado, palavra solta numa linha ou sobreposição.

## Histórico de temas (não repetir; acrescentar a cada semana)
| Semana | Seg | Qua | Sex |
|---|---|---|---|
| 2026-10-05 | Lucro no papel não paga boleto (DRE x caixa) | 3 perguntas que um bom dashboard responde | Planilha não é o problema |
| 2026-10-12 | Você está financiando seu cliente (capital de giro / prazos) | O que um painel de contas a receber precisa mostrar | Todo projeto de BI começa sem nenhum gráfico |
