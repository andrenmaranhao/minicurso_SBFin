# ============================================================
# IA Aplicada a Finanças — SBFin 2026
# Prof. André Nunes Maranhão — FGV-EESP · FEA-USP
# ============================================================
# Exemplo 02: SELIC e IPCA via API do Banco Central do Brasil
# ------------------------------------------------------------
# Instalação (execute uma vez no terminal):
#   pip install requests pandas matplotlib
# ============================================================

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ── 1. Função genérica para API do BCB ────────────────────
def get_bcb(serie: int, inicio: str, fim: str) -> pd.DataFrame:
    """
    Baixa série temporal do Banco Central do Brasil (SGS).

    Parâmetros:
        serie  : código da série (ex: 432 = SELIC, 433 = IPCA)
        inicio : data inicial no formato dd/mm/aaaa
        fim    : data final   no formato dd/mm/aaaa

    Retorna:
        DataFrame com índice de datas e coluna 'valor'
    """
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados"
        f"?formato=json&dataInicial={inicio}&dataFinal={fim}"
    )
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json())
    df["data"]  = pd.to_datetime(df["data"], dayfirst=True)
    df["valor"] = df["valor"].str.replace(",", ".").astype(float)
    return df.set_index("data")

# ── 2. Baixar SELIC (432) e IPCA (433) ───────────────────
print("📡 Baixando dados do BCB...")
selic = get_bcb(432, "01/01/2020", "01/01/2025")
ipca  = get_bcb(433, "01/01/2020", "01/01/2025")
print(f"   SELIC: {len(selic)} observações")
print(f"   IPCA : {len(ipca)} observações")

# ── 3. Visualização com eixo duplo ────────────────────────
fig, ax1 = plt.subplots(figsize=(13, 5))

# SELIC — eixo esquerdo
color_selic = "#00c8ff"
ax1.set_xlabel("Data")
ax1.set_ylabel("SELIC (% a.a.)", color=color_selic, fontsize=11)
ax1.plot(selic.index, selic["valor"],
         color=color_selic, linewidth=2, label="SELIC")
ax1.tick_params(axis="y", labelcolor=color_selic)

# IPCA — eixo direito
ax2 = ax1.twinx()
color_ipca = "#00ffb3"
ax2.set_ylabel("IPCA (% a.m.)", color=color_ipca, fontsize=11)
ax2.plot(ipca.index, ipca["valor"],
         color=color_ipca, linewidth=2, linestyle="--", label="IPCA")
ax2.tick_params(axis="y", labelcolor=color_ipca)

# Formatação
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b/%Y"))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.xticks(rotation=30)
ax1.grid(alpha=0.15)

# Legenda unificada
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("SELIC e IPCA — Banco Central do Brasil (2020–2025)",
          fontsize=14, pad=12)
plt.tight_layout()
plt.show()

# ── 4. Últimas observações ────────────────────────────────
print("\n📊 Últimas 5 observações — SELIC")
print(selic.tail())
print("\n📊 Últimas 5 observações — IPCA")
print(ipca.tail())
