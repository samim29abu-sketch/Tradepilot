# 11 — Quantitative Edge, Backtesting & Trading Psychology

## 1. The Math of a Profitable Trading System

You do **not** need an 80% win rate to be consistently profitable. Profitability is governed by **Expectancy**:

$$\text{Expectancy (₹ per trade)} = (\text{Win Rate} \times \text{Avg Win}) - (\text{Loss Rate} \times \text{Avg Loss}) - \text{Avg Costs}$$

### Win Rate vs. Risk-to-Reward Breakeven Table (Before Costs)

| Risk : Reward Ratio | Minimum Win Rate to Break Even | Profitable Target Win Rate |
| --- | --- | --- |
| `1 : 1` | 50.0% | 58%+ |
| `1 : 1.5` | 40.0% | 48%+ |
| `1 : 2` | 33.3% | 42%+ |
| `1 : 3` | 25.0% | 33%+ |

### Key Performance Metrics to Track in Your Paper/Live Journal
- **Profit Factor:** $\frac{\text{Gross Profits}}{\text{Gross Losses}}$ → Aim for **> 1.5** (after realistic charges).
- **Maximum Drawdown (MDD):** Largest peak-to-trough drop in account equity.
- **Drawdown Recovery Math (Why Protecting Capital Matters Most):**

| Account Loss | Gain Needed Just to Break Even |
| --- | --- |
| -10% | +11.1% |
| -20% | +25.0% |
| -30% | +42.9% |
| -50% | **+100.0%** |
| -75% | **+300.0%** |

---

## 2. Backtesting & Paper-Trading Validation Rules

Before ever risking real money on a strategy tested in TradePilot:

1. **Minimum Sample Size:** Test at least **30–50 trades** across different market regimes (trending weeks, sideways weeks, high-VIX weeks, expiry days) before judging whether a setup has an edge.
2. **Account for Realistic Indian Friction:**
   - Subtract **~₹70–₹85 per lot round trip** (brokerage + 0.15% STT + NSE txn + stamp duty + GST) PLUS **1–2 points of slippage** per trade.
   - A scalping strategy making ₹150 gross per trade often loses money live once real charges and slippage are applied.
3. **Avoid Common Backtesting Traps:**
   - **Look-Ahead Bias:** Using the high/low of a candle before it actually closed.
   - **Overfitting (Curve-Fitting):** Tweaking 8 parameters (e.g., "13.5 EMA + RSI 61.3 between 10:17 and 11:43") until past data looks perfect — it will fail live. Keep setups simple (2–3 logical rules max).
   - **Survivorship / Cherry-Picking:** Only logging winning charts in hindsight while ignoring valid signals that failed.
4. **Paper-to-Live Transition Ladder:**
   - Stage 1: Profitable over **30+ paper trades** in TradePilot with strict rule adherence.
   - Stage 2: Transition to live trading with **1 single lot only** (minimum possible size) for 20+ trades to experience real emotional pressure and real fills.
   - Stage 3: Scale lot size **only** when account equity grows and journal shows ≥ 90% rule compliance.

---

## 3. Trading Psychology & Behavioral Safeguards

Most Indian F&O traders fail not because of charts, but because of **emotional execution errors**:

| Psychological Trap | How It Happens | Hard Counter-Rule |
| --- | --- | --- |
| **FOMO (Chasing)** | Missing a big green candle and buying late right into resistance | "If I missed the setup, the trade is gone. Wait for a retest or the next setup." |
| **Revenge Trading** | Taking an immediate unplanned trade right after a Stop-Loss to "make it back" | Mandatory **15-minute cooldown** after any losing trade; hard stop after 2 consecutive losses. |
| **Moving Stop-Loss Wider** | Dragging SL lower hoping price will bounce back | **Never widen an SL.** If invalidated, exit. Only ever move SL *in your favor*. |
| **Overtrading After a Big Win** | Feeling invincible after a +₹5,000 morning and giving it all back in midday chop | Lock profits: if up **+3% to +4% on the day**, cut size in half or stop for the day. |
| **Premature Profit Booking** | Cutting winners at +₹500 out of fear while letting losers run to -₹2,500 | Set automated **SL + Target** in TradePilot immediately upon entry and let the server manage the trade. |

---

## 4. Daily Trade Journal Template

Record every paper or live trade immediately after closing:

```markdown
### Trade #__ | Date: YYYY-MM-DD | Index: NIFTY / BANKNIFTY
- **Contract:** e.g. NIFTY 25000 CE (Expiry: YYYY-MM-DD)
- **Setup Type:** ORB / VWAP Pullback / PDH Sweep / Breakout+Retest / Spread
- **Higher TF Bias (15m/1H):** Bullish / Bearish / Range
- **Confluence Factors:** S/R level, Candle pattern, OI/PCR, Heavyweights, Straddle
- **Entry Price / Time:** ₹___ at __:__ IST | **Qty:** ___
- **Planned SL / Target:** SL ₹___ | Target ₹___ | **R:R:** 1:__
- **Exit Price / Time:** ₹___ at __:__ IST | **Exit Reason:** Target / SL / Trail / Time Stop / Manual
- **Gross P&L:** ₹___ | **Est. Charges:** ₹___ | **Net P&L:** ₹___
- **Rule Adherence (Yes/No):** Did I follow every rule?
- **Emotion State:** Calm / FOMO / Anxious / Revenge / Greedy
- **Lesson Learned:** One concrete sentence for next time.
```
