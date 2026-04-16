# 📊 Power BI Build Guide — NSE Stock Market Analytics

## Overview
This guide walks you through building a professional Power BI report using `data/nse_cleaned.csv`.

---

## STEP 1: Import Data
1. Open **Power BI Desktop**
2. Click **Get Data → Text/CSV**
3. Select `data/nse_cleaned.csv`
4. In Power Query Editor:
   - Change `Date` column type → **Date**
   - Change `Close`, `Open`, `High`, `Low`, `MA_20`, `MA_50`, `MA_200` → **Decimal Number**
   - Change `Volume` → **Whole Number**
   - Click **Close & Apply**

---

## STEP 2: Create a Date Table (Best Practice)
In **Modeling → New Table**:
```dax
DateTable = CALENDAR(DATE(2023,1,1), DATE(2026,3,31))
```
Then add columns:
```dax
Year = YEAR(DateTable[Date])
Month = MONTH(DateTable[Date])
MonthName = FORMAT(DateTable[Date], "MMM YYYY")
Quarter = "Q" & QUARTER(DateTable[Date]) & " " & YEAR(DateTable[Date])
```
Create relationship: `DateTable[Date]` → `nse_cleaned[Date]` (Many-to-One)

---

## STEP 3: DAX Measures

### Basic Measures
```dax
-- Latest Close Price
Latest Close = 
CALCULATE(LASTNONBLANK(nse_cleaned[Close], 1), ALLSELECTED(nse_cleaned))

-- Total Return %
Total Return % = 
VAR firstClose = CALCULATE(FIRSTNONBLANK(nse_cleaned[Close], 1))
VAR lastClose  = CALCULATE(LASTNONBLANK(nse_cleaned[Close], 1))
RETURN DIVIDE(lastClose - firstClose, firstClose) * 100

-- Average RSI
Avg RSI = AVERAGE(nse_cleaned[RSI])

-- Total Volume (Crores)
Total Volume Cr = SUM(nse_cleaned[Turnover_Cr])

-- Market Cap (Lakhs Cr)
Total Market Cap L Cr = 
DIVIDE(CALCULATE(LASTNONBLANK(nse_cleaned[Market_Cap_Cr], 1)), 100000)
```

### Advanced Measures
```dax
-- Annualised Volatility
Ann Volatility % = 
CALCULATE(STDEV.P(nse_cleaned[Daily_Return])) * SQRT(252) * 100

-- Sharpe Ratio (approx, risk-free = 6%)
Sharpe Ratio = 
VAR annReturn = AVERAGE(nse_cleaned[Daily_Return]) * 252
VAR annVol    = STDEV.P(nse_cleaned[Daily_Return]) * SQRT(252)
RETURN DIVIDE(annReturn - 0.06, annVol)

-- Max Drawdown %
Max Drawdown % = 
MINX(
  SUMMARIZE(nse_cleaned, nse_cleaned[Date], nse_cleaned[Symbol]),
  VAR curClose = nse_cleaned[Close]
  VAR maxClose = CALCULATE(MAX(nse_cleaned[Close]), 
                   nse_cleaned[Date] <= EARLIER(nse_cleaned[Date]))
  RETURN DIVIDE(curClose - maxClose, maxClose) * 100
)

-- Overbought Signals Count
Overbought Count = 
CALCULATE(COUNTROWS(nse_cleaned), nse_cleaned[Signal] = "Overbought")

-- Oversold Signals Count
Oversold Count = 
CALCULATE(COUNTROWS(nse_cleaned), nse_cleaned[Signal] = "Oversold")
```

---

## STEP 4: Report Pages & Visuals

### Page 1: Executive Dashboard
| Visual | Fields | Notes |
|--------|--------|-------|
| KPI Card | `Latest Close` | Format: ₹#,##0.00 |
| KPI Card | `Total Return %` | Format: +0.00% |
| KPI Card | `Avg RSI` | Format: 0.0 |
| KPI Card | `Total Market Cap L Cr` | Format: ₹0.0L Cr |
| Line Chart | Axis: Date, Values: Close | Group by Symbol |
| Slicer | Symbol | Multi-select |
| Slicer | Sector | Dropdown |
| Slicer | Date | Date range |

### Page 2: Stock Analysis (Drill-through)
| Visual | Fields |
|--------|--------|
| Candlestick Chart | Date, Open, High, Low, Close |
| Line Chart | MA_20, MA_50, MA_200 overlaid on Close |
| Bar Chart | Daily_Return by Month |
| Gauge | RSI (min=0, max=100, target=50) |
| Table | OHLCV + Technical indicators |

### Page 3: Sector Performance
| Visual | Fields |
|--------|--------|
| Clustered Bar | Total Return % by Sector |
| Treemap | Market_Cap_Cr by Sector, Symbol |
| Matrix | Sector × Year with Avg Return % |
| Scatter | Ann Volatility % vs Total Return % |

### Page 4: Risk Analysis
| Visual | Fields |
|--------|--------|
| Heatmap (Matrix) | RSI by Symbol × Month |
| Bar | Max Drawdown % by Symbol |
| Line | Volatility_20d over time |
| Decomposition Tree | Total Return % by Sector → Symbol |

---

## STEP 5: Formatting Tips
- **Theme**: Import a custom dark theme (JSON) or use Built-in: "Executive"
- **Font**: Segoe UI for all text
- **Colors**: Use conditional formatting on Return % (Green positive, Red negative)
- **Background**: Set canvas background to #1B2A4A for professional dark look
- **Borders**: Add subtle borders to all visuals

---

## STEP 6: Publish to Power BI Service
1. File → Publish → Select workspace
2. Go to app.powerbi.com
3. Create a **Dashboard** by pinning visuals
4. Set **Scheduled Refresh** (if connecting to live data later)

---

## DAX Reference — Quick Cheat Sheet
```dax
-- Filter to specific stock
TCS Return = CALCULATE([Total Return %], nse_cleaned[Symbol] = "TCS")

-- Year-over-year comparison
YoY Change = 
VAR curYear = CALCULATE([Total Return %], YEAR(nse_cleaned[Date]) = 2025)
VAR prevYear = CALCULATE([Total Return %], YEAR(nse_cleaned[Date]) = 2024)
RETURN curYear - prevYear

-- Top N stocks by return
Top5 Stocks = TOPN(5, VALUES(nse_cleaned[Symbol]), [Total Return %], DESC)
```

---

## Files to Use
| File | Purpose |
|------|---------|
| `data/nse_cleaned.csv` | Main data source for Power BI |
| `data/nse_raw.csv` | Raw data (optional, for comparison) |
| `data/NSE_Stock_Analysis_Report.xlsx` | Pre-built summary for reference |

---

*Guide prepared for: NSE Stock Market Analytics Portfolio Project*
*Data period: January 2023 – March 2026 | 15 Nifty 50 Stocks*
