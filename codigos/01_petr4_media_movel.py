# ============================================================
# IA Aplicada a Finanças — SBFin 2026
# Prof. André Nunes Maranhão — FGV-EESP · FEA-USP
# ============================================================
# Exemplo 01: Preço da PETR4 com Média Móvel de 30 dias
# ------------------------------------------------------------
# Instalação (execute uma vez no terminal):
#   pip install yfinance matplotlib pandas
# ============================================================

import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import sys

# Evita erro de encoding no console do Windows (cp1252) ao imprimir emojis/acentos.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ── 1. Baixar dados históricos ────────────────────────────
ticker = yf.Ticker("PETR4.SA")
df = ticker.history(period="2y")          # últimos 2 anos

if df.empty:
    raise SystemExit(
        "Nenhum dado retornado para PETR4.SA.\n"
        "Causa comum: yfinance desatualizado (Yahoo mudou a API).\n"
        f"Versão instalada: {yf.__version__}\n"
        "Atualize no mesmo Python do Cursor:\n"
        "  python -m pip install -U yfinance"
    )

# ── 2. Calcular média móvel de 30 dias ────────────────────
df["MM30"] = df["Close"].rolling(window=30).mean()

# ── 3. Visualização ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(df.index, df["Close"], label="PETR4 — Preço de Fechamento",
        color="#00c8ff", linewidth=1.2, alpha=0.8)
ax.plot(df.index, df["MM30"],  label="Média Móvel 30 dias",
        color="#00ffb3", linewidth=2.2)

ax.set_title("Petrobras (PETR4.SA) — Preço e Média Móvel", fontsize=14, pad=12)
ax.set_xlabel("Data")
ax.set_ylabel("Preço (R$)")
ax.legend()
ax.grid(alpha=0.2)
plt.tight_layout()
plt.show()

# ── 4. Estatísticas básicas ───────────────────────────────
print("\n📊 Estatísticas PETR4 (últimos 2 anos)")
print(df["Close"].describe().round(2))
