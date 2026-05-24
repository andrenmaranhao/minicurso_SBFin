# ============================================================
# IA Aplicada a Finanças — SBFin 2026
# Prof. André Nunes Maranhão — FGV-EESP · FEA-USP
# ============================================================
# Exemplo 04 (R): Preço da PETR4 com Média Móvel de 30 dias
# ------------------------------------------------------------
# Instalação (execute uma vez no console do R):
#   install.packages(c("quantmod", "ggplot2", "dplyr"))
# ============================================================

library(quantmod)
library(ggplot2)
library(dplyr)

# ── 1. Baixar dados históricos ────────────────────────────
cat("📡 Baixando dados da PETR4...\n")
getSymbols("PETR4.SA",
           src  = "yahoo",
           from = Sys.Date() - 730,   # últimos 2 anos
           auto.assign = TRUE)

# ── 2. Organizar em data.frame ────────────────────────────
df <- data.frame(
  data    = index(PETR4.SA),
  preco   = as.numeric(Cl(PETR4.SA))   # Close price
) %>%
  filter(!is.na(preco)) %>%
  mutate(mm30 = zoo::rollmean(preco, k = 30, fill = NA, align = "right"))

# ── 3. Visualização com ggplot2 ───────────────────────────
ggplot(df, aes(x = data)) +
  geom_line(aes(y = preco, colour = "PETR4"), linewidth = 0.8, alpha = 0.7) +
  geom_line(aes(y = mm30,  colour = "MM 30 dias"), linewidth = 1.5) +
  scale_colour_manual(
    values = c("PETR4" = "#00c8ff", "MM 30 dias" = "#00ffb3")
  ) +
  labs(
    title   = "Petrobras (PETR4.SA) — Preço e Média Móvel",
    x       = "Data",
    y       = "Preço (R$)",
    colour  = NULL
  ) +
  theme_minimal(base_size = 13) +
  theme(
    plot.title   = element_text(face = "bold"),
    legend.position = "bottom"
  )

# ── 4. Estatísticas básicas ───────────────────────────────
cat("\n📊 Estatísticas PETR4 (últimos 2 anos)\n")
print(summary(df$preco))
