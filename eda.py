"""
╔══════════════════════════════════════════════════════════════════════╗
║     NSE NIFTY 50 — Indian Stock Market Analysis                     ║
║     Exploratory Data Analysis & Data Cleaning Script                ║
║     Dataset: Top 15 Nifty Stocks | Jan 2023 – Mar 2026             ║
║     Author: Data Analytics Portfolio Project                         ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── CONFIGURATION ────────────────────────────────────────────────────────────
RAW_DATA   = 'data/nse_raw.csv'
CLEAN_DATA = 'data/nse_cleaned.csv'

# ── 1. LOAD DATA ─────────────────────────────────────────────────────────────
print("\n" + "═"*65)
print("  STEP 1: LOADING DATA")
print("═"*65)

df = pd.read_csv(RAW_DATA, parse_dates=['Date'])
print(f"  ✅ Loaded {len(df):,} rows × {df.shape[1]} columns")
print(f"  📅 Date Range  : {df['Date'].min().date()} → {df['Date'].max().date()}")
print(f"  📈 Stocks      : {df['Symbol'].nunique()} → {sorted(df['Symbol'].unique())}")
print(f"  🏭 Sectors     : {df['Sector'].nunique()} → {sorted(df['Sector'].unique())}")

# ── 2. DATA QUALITY CHECK ─────────────────────────────────────────────────────
print("\n" + "═"*65)
print("  STEP 2: DATA QUALITY CHECK")
print("═"*65)

missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
quality = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
quality = quality[quality['Missing Count'] > 0]

if len(quality) == 0:
    print("  ✅ No missing values in core OHLCV columns")
else:
    print(quality.to_string())

print(f"\n  Duplicate rows    : {df.duplicated().sum()}")
print(f"  Negative prices   : {(df[['Open','High','Low','Close']] < 0).sum().sum()}")
print(f"  High < Low rows   : {(df['High'] < df['Low']).sum()}")
print(f"  Zero volume rows  : {(df['Volume'] == 0).sum()}")

# ── 3. DESCRIPTIVE STATISTICS ────────────────────────────────────────────────
print("\n" + "═"*65)
print("  STEP 3: DESCRIPTIVE STATISTICS (CLOSE PRICE BY STOCK)")
print("═"*65)

desc = df.groupby('Symbol')['Close'].agg(['min','max','mean','std']).round(2)
desc.columns = ['Min ₹','Max ₹','Mean ₹','Std Dev']
print(desc.to_string())

# ── 4. DATA CLEANING ─────────────────────────────────────────────────────────
print("\n" + "═"*65)
print("  STEP 4: DATA CLEANING")
print("═"*65)

df_clean = df.copy()

# Drop rows where core indicators are NaN (first 200 rows per stock for MA_200)
before = len(df_clean)
df_clean = df_clean.dropna(subset=['MA_20', 'MA_50', 'RSI'])
print(f"  Dropped {before - len(df_clean):,} warm-up rows (MA/RSI calculation period)")

# Validate OHLC integrity
df_clean = df_clean[df_clean['High'] >= df_clean['Low']]
df_clean = df_clean[df_clean['Close'] > 0]
df_clean = df_clean[df_clean['Volume'] > 0]
print(f"  ✅ OHLC integrity check passed")
print(f"  ✅ Final cleaned dataset: {len(df_clean):,} rows")

# Add derived columns
df_clean['Signal'] = np.where(df_clean['RSI'] < 30, 'Oversold',
                     np.where(df_clean['RSI'] > 70, 'Overbought', 'Neutral'))
df_clean['Price_vs_MA200'] = np.where(df_clean['Close'] > df_clean['MA_200'], 'Above', 'Below')
df_clean['Daily_Return_Pct'] = (df_clean['Daily_Return'] * 100).round(4)
print(f"  ✅ Added Signal, Price_vs_MA200, Daily_Return_Pct columns")

# ── 5. RETURNS ANALYSIS ───────────────────────────────────────────────────────
print("\n" + "═"*65)
print("  STEP 5: RETURNS ANALYSIS")
print("═"*65)

returns = df_clean.groupby('Symbol').apply(
    lambda x: (x.iloc[-1]['Close'] - x.iloc[0]['Close']) / x.iloc[0]['Close'] * 100
).round(2).sort_values(ascending=False)
returns.name = 'Total Return %'
print("\n  3-Year Total Returns (Jan 2023 – Mar 2026):")
print("  " + "-"*35)
for sym, ret in returns.items():
    bar = "█" * int(abs(ret) / 5)
    sign = "+" if ret > 0 else ""
    print(f"  {sym:<15} {sign}{ret:>7.1f}%  {bar}")

# ── 6. VOLATILITY ANALYSIS ────────────────────────────────────────────────────
print("\n" + "═"*65)
print("  STEP 6: VOLATILITY & RISK ANALYSIS")
print("═"*65)

vol = df_clean.groupby('Symbol').agg(
    Ann_Volatility=('Daily_Return', lambda x: x.std() * np.sqrt(252) * 100),
    Sharpe_Approx=('Daily_Return', lambda x: (x.mean() * 252) / (x.std() * np.sqrt(252)) if x.std() > 0 else 0),
    Max_Drawdown=('Close', lambda x: ((x - x.cummax()) / x.cummax()).min() * 100)
).round(2)
vol.columns = ['Ann. Volatility %', 'Sharpe Ratio', 'Max Drawdown %']
vol = vol.sort_values('Sharpe Ratio', ascending=False)
print(vol.to_string())

# ── 7. SECTOR ANALYSIS ────────────────────────────────────────────────────────
print("\n" + "═"*65)
print("  STEP 7: SECTOR PERFORMANCE")
print("═"*65)

sector = df_clean.groupby('Sector').agg(
    Stocks=('Symbol','nunique'),
    Avg_Ann_Return=('Daily_Return', lambda x: x.mean() * 252 * 100),
    Avg_Volatility=('Volatility_20d', lambda x: x.mean() * 100),
    Avg_RSI=('RSI','mean'),
    Total_Turnover_Cr=('Turnover_Cr','sum')
).round(2)
sector = sector.sort_values('Avg_Ann_Return', ascending=False)
print(sector.to_string())

# ── 8. RSI SIGNAL DISTRIBUTION ───────────────────────────────────────────────
print("\n" + "═"*65)
print("  STEP 8: RSI SIGNAL DISTRIBUTION")
print("═"*65)

signals = df_clean['Signal'].value_counts()
print(f"\n  Total observations: {len(df_clean):,}")
for sig, count in signals.items():
    pct = count / len(df_clean) * 100
    print(f"  {sig:<15}: {count:>7,}  ({pct:.1f}%)")

# ── 9. CORRELATION MATRIX ────────────────────────────────────────────────────
print("\n" + "═"*65)
print("  STEP 9: INTER-STOCK RETURN CORRELATION (TOP 5 PAIRS)")
print("═"*65)

pivot = df_clean.pivot_table(index='Date', columns='Symbol', values='Daily_Return')
corr = pivot.corr()
corr = corr.where(~np.eye(len(corr), dtype=bool))
corr_pairs = corr.unstack().dropna().sort_values(ascending=False)
corr_pairs = corr_pairs[corr_pairs.index.get_level_values(0) < corr_pairs.index.get_level_values(1)]
print("\n  Most correlated pairs:")
for (s1, s2), c in corr_pairs.head(5).items():
    print(f"  {s1} ↔ {s2}: {c:.3f}")
print("\n  Least correlated pairs:")
for (s1, s2), c in corr_pairs.tail(5).items():
    print(f"  {s1} ↔ {s2}: {c:.3f}")

# ── 10. SAVE CLEANED DATA ────────────────────────────────────────────────────
print("\n" + "═"*65)
print("  STEP 10: SAVING CLEANED DATASET")
print("═"*65)

df_clean.to_csv(CLEAN_DATA, index=False)
print(f"  ✅ Saved {len(df_clean):,} rows to {CLEAN_DATA}")
print(f"  ✅ Columns: {list(df_clean.columns)}")

print("\n" + "═"*65)
print("  ✅ EDA COMPLETE — All outputs saved to data/ folder")
print("     → For Power BI: import data/nse_cleaned.csv")
print("     → For dashboard: open index.html in browser")
print("═"*65 + "\n")
