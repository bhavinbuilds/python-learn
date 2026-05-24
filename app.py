import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# JPMorgan Annual Finance Model
# FY2021-FY2025
# Units: USD Billions
# -----------------------------

data = {
    "FY": ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"],
    "Revenue_B": [130.898, 122.306, 145.670, 166.775, 168.235],
    "Net_Income_B": [48.334, 37.676, 49.552, 58.471, 57.048],
    "Total_Assets_B": [3743.567, 3665.743, 3875.393, 4002.814, 4424.900],
    "Total_Equity_B": [294.127, 292.332, 327.878, 344.758, 362.438],
    "Net_Interest_Income_B": [52.311, 66.710, 89.267, 92.583, 95.443],
    "Operating_Expense_B": [71.336, 75.874, 82.836, 90.332, 96.042],
    "Total_Deposits_B": [2462.303, 2340.179, 2400.688, 2406.032, 2559.320]
}

df = pd.DataFrame(data).set_index("FY")

# -----------------------------
# Ratio Calculations
# -----------------------------
df["Revenue_Growth_%"] = df["Revenue_B"].pct_change() * 100
df["Net_Income_Growth_%"] = df["Net_Income_B"].pct_change() * 100
df["Assets_Growth_%"] = df["Total_Assets_B"].pct_change() * 100
df["Equity_Growth_%"] = df["Total_Equity_B"].pct_change() * 100

# Approximate returns using ending balances
df["ROA_%"] = (df["Net_Income_B"] / df["Total_Assets_B"]) * 100
df["ROE_%"] = (df["Net_Income_B"] / df["Total_Equity_B"]) * 100

df["Efficiency_Ratio_%"] = (df["Operating_Expense_B"] / df["Revenue_B"]) * 100
df["NII_to_Revenue_%"] = (df["Net_Interest_Income_B"] / df["Revenue_B"]) * 100
df["Deposits_to_Assets_%"] = (df["Total_Deposits_B"] / df["Total_Assets_B"]) * 100

# -----------------------------
# Optional FY2026 Forecast
# -----------------------------
forecast_2026 = {
    "Revenue_B": df.loc["FY2025", "Revenue_B"] * 1.04,           # user assumption: 4% growth
    "Net_Income_B": df.loc["FY2025", "Net_Income_B"] * 1.03,     # user assumption: 3% growth
    "Total_Assets_B": df.loc["FY2025", "Total_Assets_B"] * 1.05, # user assumption: 5% growth
    "Total_Equity_B": df.loc["FY2025", "Total_Equity_B"] * 1.04, # user assumption: 4% growth
    "Net_Interest_Income_B": 103.0,                              # management outlook
    "Operating_Expense_B": 105.0,                                # management outlook
    "Total_Deposits_B": df.loc["FY2025", "Total_Deposits_B"] * 1.03
}

forecast_df = pd.DataFrame(forecast_2026, index=["FY2026E"])

forecast_df["Revenue_Growth_%"] = (
    (forecast_df["Revenue_B"] / df.loc["FY2025", "Revenue_B"]) - 1
) * 100
forecast_df["Net_Income_Growth_%"] = (
    (forecast_df["Net_Income_B"] / df.loc["FY2025", "Net_Income_B"]) - 1
) * 100
forecast_df["Assets_Growth_%"] = (
    (forecast_df["Total_Assets_B"] / df.loc["FY2025", "Total_Assets_B"]) - 1
) * 100
forecast_df["Equity_Growth_%"] = (
    (forecast_df["Total_Equity_B"] / df.loc["FY2025", "Total_Equity_B"]) - 1
) * 100
forecast_df["ROA_%"] = (forecast_df["Net_Income_B"] / forecast_df["Total_Assets_B"]) * 100
forecast_df["ROE_%"] = (forecast_df["Net_Income_B"] / forecast_df["Total_Equity_B"]) * 100
forecast_df["Efficiency_Ratio_%"] = (forecast_df["Operating_Expense_B"] / forecast_df["Revenue_B"]) * 100
forecast_df["NII_to_Revenue_%"] = (forecast_df["Net_Interest_Income_B"] / forecast_df["Revenue_B"]) * 100
forecast_df["Deposits_to_Assets_%"] = (forecast_df["Total_Deposits_B"] / forecast_df["Total_Assets_B"]) * 100

full_df = pd.concat([df, forecast_df])

# -----------------------------
# Display Table
# -----------------------------
print("\nJPMorgan Annual Finance Model (USD Billions)\n")
print(full_df.round(2))

# -----------------------------
# Simple Text Summary
# -----------------------------
best_revenue_year = df["Revenue_B"].idxmax()
best_income_year = df["Net_Income_B"].idxmax()
largest_assets_year = df["Total_Assets_B"].idxmax()

print("\nSummary:")
print(f"- Highest revenue year: {best_revenue_year} (${df.loc[best_revenue_year, 'Revenue_B']:.2f}B)")
print(f"- Highest net income year: {best_income_year} (${df.loc[best_income_year, 'Net_Income_B']:.2f}B)")
print(f"- Largest asset base year: {largest_assets_year} (${df.loc[largest_assets_year, 'Total_Assets_B']:.2f}B)")
print(f"- FY2026E Efficiency Ratio: {forecast_df.loc['FY2026E', 'Efficiency_Ratio_%']:.2f}%")
print(f"- FY2026E ROE: {forecast_df.loc['FY2026E', 'ROE_%']:.2f}%")

# -----------------------------
# Charts
# -----------------------------
plt.style.use("seaborn-v0_8")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Chart 1: Revenue & Net Income
axes[0, 0].plot(full_df.index, full_df["Revenue_B"], marker="o", label="Revenue")
axes[0, 0].plot(full_df.index, full_df["Net_Income_B"], marker="o", label="Net Income")
axes[0, 0].set_title("Revenue and Net Income")
axes[0, 0].set_ylabel("USD Billions")
axes[0, 0].legend()

# Chart 2: Assets & Deposits
axes[0, 1].plot(full_df.index, full_df["Total_Assets_B"], marker="o", label="Total Assets")
axes[0, 1].plot(full_df.index, full_df["Total_Deposits_B"], marker="o", label="Total Deposits")
axes[0, 1].set_title("Assets and Deposits")
axes[0, 1].set_ylabel("USD Billions")
axes[0, 1].legend()

# Chart 3: ROA & ROE
axes[1, 0].plot(full_df.index, full_df["ROA_%"], marker="o", label="ROA %")
axes[1, 0].plot(full_df.index, full_df["ROE_%"], marker="o", label="ROE %")
axes[1, 0].set_title("Profitability Ratios")
axes[1, 0].set_ylabel("%")
axes[1, 0].legend()

# Chart 4: Efficiency Ratio & NII/Revenue
axes[1, 1].plot(full_df.index, full_df["Efficiency_Ratio_%"], marker="o", label="Efficiency Ratio %")
axes[1, 1].plot(full_df.index, full_df["NII_to_Revenue_%"], marker="o", label="NII / Revenue %")
axes[1, 1].set_title("Banking Efficiency Metrics")
axes[1, 1].set_ylabel("%")
axes[1, 1].legend()

plt.tight_layout()
plt.show()