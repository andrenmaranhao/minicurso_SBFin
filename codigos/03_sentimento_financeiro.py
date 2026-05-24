# ============================================================
# IA Aplicada a Finanças — SBFin 2026
# Prof. André Nunes Maranhão — FGV-EESP · FEA-USP
# ============================================================
# Exemplo 03: Análise de Sentimento em Notícias Financeiras
#             usando a API da Anthropic (Claude)
# ------------------------------------------------------------
# Instalação (execute uma vez no terminal):
#   pip install anthropic pandas
#
# Configuração — chave de API:
#   export ANTHROPIC_API_KEY="sua-chave-aqui"
#   (ou defina a variável diretamente na linha ANTHROPIC_API_KEY abaixo)
# ============================================================

import os
import anthropic
import pandas as pd

# ── 1. Inicializar cliente ────────────────────────────────
# A chave é lida automaticamente da variável de ambiente ANTHROPIC_API_KEY
client = anthropic.Anthropic()

# ── 2. Função de classificação de sentimento ─────────────
def classificar_sentimento(headline: str) -> str:
    """
    Classifica uma headline financeira como Positivo, Negativo ou Neutro.

    Parâmetro:
        headline : texto da notícia financeira

    Retorna:
        str — 'Positivo', 'Negativo' ou 'Neutro'
    """
    resposta = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=10,
        system=(
            "Você é um analista financeiro especializado em NLP. "
            "Classifique o sentimento da notícia financeira como: "
            "Positivo, Negativo ou Neutro. "
            "Responda APENAS uma palavra, sem pontuação."
        ),
        messages=[{"role": "user", "content": headline}]
    )
    return resposta.content[0].text.strip()

# ── 3. Headlines de exemplo ───────────────────────────────
headlines = [
    "Petrobras bate recorde de produção no trimestre e eleva guidance",
    "SELIC sobe para 13,75% em decisão unânime do COPOM",
    "Dólar fecha estável ante o real com baixo volume de negócios",
    "Ambev reporta queda de 8% no lucro líquido do 3T24",
    "B3 anuncia novo produto de derivativos de crédito para 2025",
    "Inflação surpreende negativamente e pressiona juros futuros",
    "Bradesco reduz inadimplência e supera estimativas do mercado",
    "Risco Brasil recua ao menor nível desde 2019",
]

# ── 4. Classificar e montar DataFrame ────────────────────
print("🤖 Classificando sentimentos com Claude...\n")
resultados = []
for h in headlines:
    sentimento = classificar_sentimento(h)
    resultados.append({"Headline": h, "Sentimento": sentimento})
    icone = {"Positivo": "🟢", "Negativo": "🔴", "Neutro": "🟡"}.get(sentimento, "⚪")
    print(f"{icone} {sentimento:10s} | {h[:60]}")

# ── 5. Resumo ─────────────────────────────────────────────
df = pd.DataFrame(resultados)
print("\n📊 Distribuição de Sentimentos")
print(df["Sentimento"].value_counts())

# ── 6. Exportar resultado ─────────────────────────────────
df.to_csv("sentimentos_financeiros.csv", index=False, encoding="utf-8-sig")
print("\n✅ Resultado salvo em: sentimentos_financeiros.csv")
