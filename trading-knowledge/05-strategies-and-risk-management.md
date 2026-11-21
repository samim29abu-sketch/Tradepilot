# 05 — Option Strategies, Execution & Risk Management

## 1. High-Probability Intraday Option Buying Setups (Price Action)

Option buyers fight **Theta decay** every minute, so you need **fast, clean directional expansion** — not slow drifting markets.

### Setup A: Opening Range Breakout (ORB) + Retest
- **Timeframe:** 5m / 15m (mark high and low of first 15 minutes: 09:15–09:30).
- **Condition:** Opening range is moderate (not an already-exhausted giant 200-pt NIFTY candle).
- **Trigger:** Strong 5m candle closes above ORB High (for CE) or below ORB Low (for PE) aligned with VWAP + rising Put/Call OI support.
- **Entry:** Break of trigger candle (or shallow retest of ORB line).
- **Stop-Loss:** Below the trigger candle / inside the ORB range (translated to option premium SL).
- **Target:** Minimum 1:2 R:R or next major S/R (PDH/PDL/round number).

### Setup B: Trend Pullback to VWAP / 20 EMA + S/R Flip
- **Context:** Clear intraday trend (HH/HL above VWAP for CE; LH/LL below VWAP for PE).
- **Trigger:** Price pulls back calmly on small candles to **VWAP / 20 EMA / broken level**, then prints a **Hammer, Bullish Engulfing, or Inside Bar breakout** (inverse for PE).
- **Why it works:** Tight stop-loss, trading *with* institutional flow, high R:R (often 1:2.5 to 1:3+).

### Setup C: Liquidity Sweep Reversal (PDH / PDL Stop Hunt)
- **Context:** Price pokes cleanly above PDH / Day High (or below PDL / Day Low) and immediately closes back inside with a sharp rejection wick.
- **Trigger:** Break of the sweep candle's opposite end.
- **Stop-Loss:** Just beyond the sweep wick extreme (very tight invalidation).
- **Target:** VWAP first (trail SL to breakeven), then opposite side of range / PDC.

### Setup D: Tight Consolidation / Buildup Breakout
- **Context:** Price compresses tightly for 4–8 candles (5m) right beneath a key resistance or right above a key support.
- **Trigger:** Expansion Marubozu closing out of the box + Call/Put OI unwinding on the trapped side.
- **Avoid:** Do not buy if the option premium is spiking abnormally while spot barely moves (IV spike trap).

---

## 2. Hedged Option Selling & Multi-Leg Strategies

When markets are **range-bound or High IV**, option selling / defined-risk spreads outperform naked option buying:

| Strategy | Market View | Construction | Risk / Reward Profile |
| --- | --- | --- | --- |
| **Bull Call Spread (Debit)** | Moderately Bullish | Buy ATM CE + Sell OTM CE | Defined max risk & reward; lowers cost & reduces theta decay vs. naked buying |
| **Bear Put Spread (Debit)** | Moderately Bearish | Buy ATM PE + Sell OTM PE | Defined max risk & reward; cushions IV crush |
| **Bull Put Spread (Credit)** | Neutral to Bullish | Sell OTM PE + Buy further OTM PE | Profits from upside, sideways, or small dip + theta decay; capped risk |
| **Bear Call Spread (Credit)** | Neutral to Bearish | Sell OTM CE + Buy further OTM CE | Profits from downside, sideways, or small rise + theta decay; capped risk |
| **Iron Condor** | Range-Bound | Bull Put Spread + Bear Call Spread | Defined-risk non-directional theta harvester; best on wide-CPR / high-IV range days |
| **Short Straddle / Strangle** | Tight Range | Sell ATM (or OTM) CE + PE | High theta decay, **unlimited risk if unhedged** — always add protective wings or strict SL |

*Note on Capital (2026):* A single hedged spread on NIFTY (lot size 65) generally needs ~₹30,000–₹60,000 margin depending on wing width, while naked selling needs ₹1.2L–₹1.8L+ (plus +2% ELM on expiry day).

---

## 3. Risk Management Rules (Calibrated for a ₹1,00,000 Account)

These rules match TradePilot's **₹1,00,000 paper account** and scale cleanly to live trading:

| Rule | Recommended Limit | Example on ₹1,00,000 Capital |
| --- | --- | --- |
| **Max Risk Per Trade** | **1% – 2%** of capital | **₹1,000 – ₹2,000** max loss per trade |
| **Max Daily Loss Limit** | **3% – 4%** of capital | **₹3,000 – ₹4,000** → **STOP trading for the day** |
| **Max Weekly Drawdown** | **8% – 10%** of capital | Pause & review journal before taking new trades |
| **Max Trades Per Day** | **2 – 3 quality setups** | Prevents overtrading & STT/brokerage bleed |
| **Minimum Risk-to-Reward** | **1 : 2** (never worse than 1 : 1.5) | Risk ₹1,500 to target at least ₹3,000 |
| **Position Sizing Formula** | $\text{Lots} = \left\lfloor \frac{\text{Max Risk (₹)}}{\text{SL Points} \times \text{Lot Size}} \right\rfloor$ | NIFTY (65 qty), SL = 20 pts → Risk/lot = ₹1,300 → **1 lot max** |
| **Capital Allocation Cap** | Never deploy > 25–30% of capital into one naked option buy | Protects against sudden news/gap spikes |

### Managing Active Trades (Trailing Stop-Loss Rules)
1. **Hard SL Immediately:** Never enter an option trade without a predefined Stop-Loss. Never "hope" or average down a losing option buy!
2. **At 1:1 Profit:** Move Stop-Loss to **Breakeven (+ charges)** — turns the trade into a risk-free runner.
3. **At 1:2 Profit:** Book 50% (if holding 2+ lots) or tighten Trailing SL below the last 5m swing low / 9 EMA.
4. **Time Stop:** If an option buy doesn't move in your favor within 3–5 candles (15–25 minutes), exit or tighten SL — stagnant price means guaranteed theta loss.

---

## 4. Pre-Trade Checklist (Run Before Every Entry)

- [ ] **Market Structure:** Is the 15m/5m trend clear, or is it sideways chop?
- [ ] **Location:** Is price at a real S/R zone (PDH/PDL/VWAP/Swing/OI wall) and NOT in no-man's land?
- [ ] **Trigger:** Did a clean candlestick or breakout + retest **close** confirm the move?
- [ ] **Option Chain Check:** Are OI/Change-in-OI and PCR supporting the direction (or showing unwinding)?
- [ ] **Strike & Liquidity:** ATM or 1–2 ITM strike selected with tight bid-ask spread?
- [ ] **Math Check:** Is SL defined on the chart, R:R ≥ 1:2, and rupee risk ≤ 2% of account?
- [ ] **Daily Limit:** Am I still within my daily trade count & daily max loss cap?

---

## 5. Mapping to TradePilot Paper Commands & Future Upgrades

### What You Can Already Do in TradePilot Today
Use the Automation Console in `index.html` / `app.js` to arm breakout or pullback paper trades with hard SL & Target:
- Immediate entry with SL & Target (example using 2026 NIFTY lot size 65):
  `BUY NIFTY 25000 CE QTY 65 SL 110 TARGET 160`
- Triggered breakout entry (arms on server and fills only when option crosses trigger):
  `BUY BANKNIFTY 54000 PE ABOVE 205 QTY 30 SL 175 TARGET 260`
- Emergency flat-all button / command:
  `EXIT ALL`

### Potential TradePilot Upgrades Based on This Knowledge Base
1. **Realistic Charges Simulator:** Deduct ₹20/order brokerage + 0.15% STT + NSE txn + stamp duty + GST on simulated trades so paper P&L reflects real net P&L.
2. **Daily Max Loss Kill-Switch:** Auto-lock new paper orders for the rest of the day once realized + open loss hits `-₹3,000` (configurable).
3. **Trailing Stop-Loss (TSL):** Automatically trail SL up/down as option LTP reaches 1:1 or moves by `X` points.
4. **Live Candle & S/R Engine:** Fetch Angel One `getCandleData` (5m/15m/Daily) to display PDH, PDL, ORB, VWAP, 20 EMA, and detect Hammer / Engulfing / Breakout signals automatically.
5. **Option Chain Enrichment:** Display **OI, Change in OI, PCR, IV, and Delta** alongside LTP in TradePilot's option chain.
