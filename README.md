# 📈 NSE Stock Market Analytics — Full Data Analytics Project

> **A professional end-to-end data analytics project** covering India's top 15 Nifty 50 stocks across 7 sectors from January 2023 to March 2026.

---

## 🚀 Live Dashboard

**[▶ View Live Dashboard](https://kaviyanivashini17.github.io/nse-stock-analysis/)**

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Power BI](https://img.shields.io/badge/Power%20BI-Ready-F2C811)
![Stocks](https://img.shields.io/badge/Stocks-15-orange)
![Data Points](https://img.shields.io/badge/Data%20Points-12%2C705-purple)

---

## 📁 Project Structure

```
nse-stock-analysis/
├── 📊 data/
│   ├── nse_raw.csv              ← Raw OHLCV data (12,705 rows)
│   └── nse_cleaned.csv          ← Cleaned + enriched data
│
├── 🐍 eda.py                    ← Python EDA & data cleaning script
│
├── 📊 data/
│   └── NSE_Stock_Analysis_Report.xlsx  ← 4-sheet Excel report
│
├── 📋 PowerBI/
│   └── GUIDE.md                  ← Step-by-step Power BI build guide(DAX formulas, visuals, layout)
|   └── nse_stock_dashboard.pbix
|   └──screenshots/
|      ├── dashboard_page1.png         
│      └── dashboard_page2.png                       
│
├── 🌐 index.html                 ← Live interactive dashboard
│
└── 📄 README.md
```

---

## 📊 Stocks Covered

| Sector | Stocks |
|--------|--------|
| 🏦 Banking | HDFCBANK, ICICIBANK, SBIN, AXISBANK |
| 💻 IT | TCS, INFY, WIPRO |
| ⚡ Energy | RELIANCE, ONGC |
| 🛒 FMCG | HINDUNILVR, ITC |
| 🚗 Automobile | MARUTI, TATAMOTORS |
| 💊 Healthcare | SUNPHARMA |
| 📡 Telecom | BHARTIARTL |

---

## 🔧 Features

### 🐍 Python EDA Script (`eda.py`)
- Data loading & quality checks
- Missing value analysis
- OHLCV descriptive statistics
- 3-year returns analysis with visual ASCII bars
- Volatility & Sharpe ratio calculation
- Sector-wise performance comparison
- RSI signal distribution
- Inter-stock correlation matrix
- Automated data cleaning & export

### 📊 Excel Report (4 Sheets)
- **Executive Dashboard** — KPI cards + performance table
- **Raw Data** — Full OHLCV dataset (3,000 rows preview)
- **Sector Analysis** — Sector-wise returns + bar chart
- **Technical Signals** — RSI, MA signals per stock

### 🌐 Live Dashboard (`index.html`)
- Interactive price trend charts (Chart.js)
- RSI gauge with signal detection
- Sector performance bar chart
- Monthly volume analysis
- Click-to-filter stock sidebar
- Full performance summary table
- Zero dependencies — opens directly in browser

### 📋 Power BI Guide
- Step-by-step import instructions
- 10+ DAX measures (returns, volatility, Sharpe, drawdown)
- 4 report page layouts with visual recommendations
- Conditional formatting & theming tips
- Publish to Power BI Service guide

---

## 🚀 Getting Started

### Run the EDA Script
```bash
git clone https://github.com/your-username/nse-stock-analysis
cd nse-stock-analysis
pip install pandas numpy openpyxl
python eda.py
```

### View the Dashboard
```bash
# Simply open in browser:
open index.html
# or double-click index.html
```

### Deploy to GitHub Pages
1. Go to repo Settings → Pages
2. Source: Deploy from branch `main`, folder `/` (root)
3. Your dashboard is live at `https://your-username.github.io/nse-stock-analysis/`

### Use with Power BI
1. Open Power BI Desktop
2. Get Data → CSV → `data/nse_cleaned.csv`
3. Follow `PowerBI/GUIDE.md` for full instructions

---

## 📈 Key Findings

| Stock | 3Y Return | Signal |
|-------|-----------|--------|
| ICICIBANK | +201% | 🔵 Neutral |
| SBIN | +140% | 🔵 Neutral |
| BHARTIARTL | +136% | 🔴 Overbought |
| TCS | +97% | 🔵 Neutral |
| HDFCBANK | +70% | 🟢 Oversold |
| INFY | -35% | 🔵 Neutral |

**Banking sector** outperformed all sectors with **+98.5% avg 3Y return**.

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Data generation, EDA, cleaning |
| Pandas | Data manipulation |
| NumPy | Statistical calculations |
| openpyxl | Excel report generation |
| Chart.js | Interactive dashboard charts |
| HTML/CSS/JS | Live dashboard (zero framework) |
| Power BI | Business intelligence reporting |

---

## 📄 Data Dictionary

| Column | Description |
|--------|-------------|
| Date | Trading date (business days) |
| Symbol | NSE stock symbol |
| Sector | Industry sector |
| Open/High/Low/Close | OHLC prices in ₹ |
| Volume | Daily trading volume |
| Turnover_Cr | Daily turnover in Crores |
| Daily_Return | Day-over-day return |
| MA_20/50/200 | Moving averages |
| RSI | Relative Strength Index (14-day) |
| Volatility_20d | 20-day rolling volatility |
| Signal | Oversold / Neutral / Overbought |
| Market_Cap_Cr | Market capitalisation in Crores |

---

## 👤 Author
Kaviya Nivashini V
---

*⭐ If this project helped you, please star it!*
