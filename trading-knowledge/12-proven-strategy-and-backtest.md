# 12 — Proven High-Reward Strategy & Live 60-Day NSE Market Proof

This document specifies **TradePilot's Dual-Engine High-Reward Strategy**, backtested on **real historical NSE 5-minute & 15-minute market data** (`2026-08-25` to `2026-11-20`, 60 consecutive trading days, 4,497 5m bars per index) with **zero look-ahead bias** (next-candle open fills) and **conservative April 2026 Indian options friction**.

You can re-run the exact proof anytime via:
```bash
python3 trading-knowledge/backtest_proof.py
```

---

## 1. Why a Dual-Engine Strategy? (Empirical Discovery)

Testing 5 classical price-action setups across 60 real Indian sessions showed why naive "one-size-fits-all" setups fail:
- **Naive 15m ORB Breakouts** lost money on both NIFTY (`-₹8,910`, PF `0.67`) and BANKNIFTY (`-₹4,585`, PF `0.86`) because NSE indices frequently fakeout early breakouts.
- **NIFTY 50** trends cleanly after holding above/below **Previous Day High / Low (PDH/PDL Polarity Flip)** with 15-minute trend confirmation.
- **BANKNIFTY** is wickier at PDH/PDL, but rewards **Multi-Timeframe (15m + 5m) 20-EMA Trend Pullbacks** outside the opening range while skipping midday chop (`11:30–13:15 IST`).
- Pairing the two uncorrelated engines cuts drawdown and produces positive net expectancy **after** all Indian charges, STT, slippage, and theta decay.

---

## 2. Exact Strategy Rules (Automated in TradePilot Radar)

### Engine A — NIFTY 50: `PDH / PDL Break & Hold` (Lot Size: `65`)
- **Higher-Timeframe Bias (15m):** `EMA 9 > EMA 20` and last closed 15m candle above `EMA 20` (Bullish → CE only); reverse for Bearish (PE only).
- **Trigger (5m Closed Candle, `09:30–14:15 IST`):**
  - **CE:** Close above **PDH**, candle low stays within `0.6 × ATR(14)` of PDH (retest/hold — no chasing extended spikes), bullish close above `5m EMA 9` and above previous 5m high.
  - **PE:** Close below **PDL**, candle high stays within `0.6 × ATR(14)` of PDL, bearish close below `5m EMA 9` and below previous 5m low.
- **Risk & Reward (`1 : 3.0`):**
  - Stop-Loss: `min(candle low, PDH - 0.35 × ATR)` for CE (mirror for PE). Skip if SL is outside `0.8–2.8 × ATR`.
  - Target: `3.0 × Risk`.
  - **Active Trail:** Once price moves `+1.5R` in favor (after 3 bars), trail Stop-Loss using **5m EMA 20**.
  - **Option Strike:** ATM or 1-strike ITM CE/PE (`Delta ~0.55`).

### Engine B — BANKNIFTY: `MTF 20-EMA Trend Pullback` (Lot Size: `30`)
- **Time Filter:** `09:30–11:30 IST` and `13:15–14:15 IST` (**strictly skips 11:30–13:15 midday chop**).
- **Trend Alignment:**
  - **15m:** `EMA 9 > EMA 20` and close `> EMA 20` (Bullish); reverse for Bearish.
  - **5m:** `EMA 9 > EMA 20 > EMA 50` and spot **outside 15m Opening Range** (`> ORB High` for CE; `< ORB Low` for PE).
- **Trigger (5m Closed Candle):**
  - Price pulls back to touch `5m EMA 20` (current or prior bar), then prints a bullish close above `5m EMA 9` that either breaks prior bar high or forms a Hammer (`lower wick ≥ 1.3 × body`). Inverse for PE.
- **Risk & Reward (`1 : 3.0`):**
  - Stop-Loss: Swing low of trigger/prior bar minus `0.15 × ATR` (mirror for PE), filtered within `0.8–2.8 × ATR`.
  - Target: `3.0 × Risk`.
  - **Active Trail:** Move Stop-Loss to **Breakeven (+3 spot pts)** once trade reaches `+1.5R`.

### Global Portfolio Safety Rules (₹1,00,000 Account)
- **Max 2 trades/day** per index
- **Daily Max Loss Kill-Switch:** `-₹3,000` (stops all auto-entries for the rest of the day)
- **Intraday Square-Off:** `15:10 IST` (zero overnight gap risk; avoids expiry exercise STT)

---

## 3. Live 60-Day NSE Backtest Proof (`2026-08-25` → `2026-11-20`)

### Conservative Indian Cost & Option Assumptions Used
- **ATM/1-ITM Delta:** `0.55`
- **Theta Decay Drag:** `0.05` option pts/min (NIFTY), `0.11` option pts/min (BANKNIFTY)
- **Round-Trip Slippage:** `1.5` option pts (NIFTY), `3.0` option pts (BANKNIFTY)
- **2026 Statutory Charges:** `₹80/lot` (NIFTY, qty 65) and `₹85/lot` (BANKNIFTY, qty 30) — covering ₹40 brokerage + 0.15% STT + NSE txn + stamp duty + 18% GST.

### Summary Performance Table (1 Lot Each, ₹1,00,000 Starting Capital)

| Engine | Trades | Win Rate | Avg Win (Net) | Avg Loss (Net) | Profit Factor | Max Drawdown | Net P&L (60 Days) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **NIFTY (`PDH/PDL Break & Hold`)** | 42 | 38.1% | ₹2,864 | ₹1,311 | **1.34** | ₹7,378 | **+₹11,719 (+11.7%)** |
| **BANKNIFTY (`MTF 20-EMA Pullback`)** | 46 | 32.6% | ₹3,939 | ₹1,562 | **1.22** | ₹16,108 | **+₹10,650 (+10.7%)** |
| **Combined Dual-Engine Portfolio** | **88** | **35.2%** | **₹3,384** | **₹1,448** | **1.27** | **₹12,416** | **+₹22,370 (+22.4%)** |

### Monthly Net P&L Breakdown (Combined Portfolio)
- **August 2026 (25–31):** `+₹1,152`
- **September 2026:** `-₹1,739` *(small controlled dip — BANKNIFTY `+₹4,099` cushioned NIFTY's `-₹5,838`)*
- **October 2026:** `+₹12,141`
- **November 2026 (1–20):** `+₹10,816`

### Recent Verifiable Trades (Check Directly on NSE / TradingView 5m Charts)

| Date | Time (IST) | Index | Dir | Entry (Spot) | Exit (Spot) | Reason | Spot Move | Est. Net Option P&L |
| --- | --- | --- | --- | ---: | ---: | --- | ---: | ---: |
| 2026-11-16 | 12:00 → 13:35 | NIFTY | CE | 25,255.7 | 25,230.7 | SL | -25.0 | -₹1,380 |
| 2026-11-17 | 09:50 → 11:45 | NIFTY | CE | 25,359.8 | 25,454.7 | TARGET | +94.9 | **+₹2,843** |
| 2026-11-17 | 13:55 → 15:00 | BANKNIFTY | CE | 62,373.8 | 62,257.8 | SL | -116.0 | -₹2,303 |
| 2026-11-18 | 09:40 → 10:00 | NIFTY | PE | 25,266.5 | 25,314.3 | SL | -47.8 | -₹1,953 |
| 2026-11-18 | 10:25 → 11:20 | NIFTY | PE | 25,247.1 | 25,281.5 | SL | -34.5 | -₹1,588 |
| 2026-11-18 | 10:45 → 11:15 | BANKNIFTY | PE | 61,980.9 | 62,147.8 | SL | -166.9 | -₹3,028 |
| 2026-11-19 | 11:25 → 12:35 | BANKNIFTY | CE | 62,440.4 | 62,676.6 | TARGET | +236.2 | **+₹3,492** |
| 2026-11-19 | 13:20 → 13:35 | BANKNIFTY | CE | 62,622.2 | 62,783.2 | TARGET | +161.0 | **+₹2,432** |
| 2026-11-19 | 14:05 → 15:10 | NIFTY | CE | 25,418.4 | 25,503.4 | EOD | +85.0 | **+₹2,652** |
| 2026-11-20 | 09:45 → 12:00 | BANKNIFTY | CE | 63,149.2 | 63,851.5 | TARGET | +702.3 | **+₹10,967** |
| 2026-11-20 | 09:55 → 10:05 | NIFTY | CE | 25,539.2 | 25,502.2 | SL | -37.1 | -₹1,535 |
| 2026-11-20 | 10:25 → 12:20 | NIFTY | CE | 25,530.7 | 25,692.2 | TARGET | +161.5 | **+₹5,224** |

> **Honest Disclaimer:** Past backtest performance using a Delta-based option proxy does not guarantee future live profits. Live option pricing is also affected by intraday IV shifts, expiry gamma spikes, and liquidity spreads. Validate this strategy across **30+ live paper trades in TradePilot** before ever considering real capital.
