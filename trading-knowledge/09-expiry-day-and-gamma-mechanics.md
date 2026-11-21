# 09 — Expiry-Day Dynamics & Gamma Mechanics

In 2026 Indian markets, **NIFTY** expires every **Tuesday** (weekly + monthly last Tuesday), **SENSEX** expires every **Thursday**, and **BANKNIFTY / FINNIFTY / MIDCPNIFTY** expire monthly on the **last Tuesday**.

Expiry day behaves completely differently from non-expiry days because **Theta** and **Gamma** both reach mathematical extremes.

---

## 1. The Four Phases of an Expiry Day (IST)

| Window (IST) | Market Behavior | Best Approach |
| --- | --- | --- |
| **09:15 – 10:30** | Overnight gap adjustment & initial range formation; premiums still carry noticeable time value. | Trade standard price action (ORB / PDH / PDL), keep normal risk. |
| **10:30 – 13:00** | **Theta Decay / Pinning Phase:** Writers aggressively sell ATM straddles/strangles; OTM options rapidly bleed toward ₹0. | Avoid buying OTM options; monitor the ATM Straddle chart for expansion vs. melt. |
| **13:00 – 14:45** | **Gamma Blast Window:** Remaining time value is tiny. A 40–60 pt NIFTY move causes ATM/near-OTM options to jump 2×–4× as trapped writers rush to cover! | Highest-reward directional window **ONLY** when spot breaks a major intraday high/low + OI unwinds rapidly. |
| **14:45 – 15:30** | **Settlement & Pinning Window:** Final 30-min weighted average close determines cash settlement; OTM premiums collapse to ₹0.05; deep ITM options trade purely at intrinsic value. | Square off all ITM options before 15:20 to avoid exercise STT/slippage; avoid new speculative bets after 15:00. |

---

## 2. Understanding Gamma Risk & Short-Covering Cascades

On expiry afternoon, near-ATM options have **massive Gamma** — Delta can jump from `0.25` to `0.85` within a 50-point NIFTY move.

### How an Expiry "Gamma Squeeze" Happens
1. Suppose NIFTY spends 3 hours trapped between `25,000` and `25,050`. Heavy Call OI builds at `25,050 CE` (trading at ₹12 at 1:30 PM) and Put OI at `25,000 PE`.
2. At 1:45 PM, NIFTY breaks decisively above `25,060` with strong heavyweights (`HDFCBANK`, `ICICIBANK`).
3. `25,050 CE` rapidly jumps from ₹12 → ₹28 → ₹55.
4. Option writers who sold `25,050 CE` for ₹12 hit their stop-losses and are forced to **buy back calls** (or buy NIFTY futures to delta-hedge).
5. Their forced buying accelerates the breakout even faster → `25,050 CE` rockets to ₹90+.

### Signs a Genuine Gamma Move Is Starting
- Spot breaks a **multi-hour intraday range** (after 13:00 IST) with a full-bodied 5m candle.
- **ATM Straddle Price** suddenly spikes above its intraday trendline / VWAP.
- **Change in OI** at the breached strike drops sharply (short covering confirmed).

---

## 3. Surviving Expiry Day (Strict Rules)

1. **Never Risk Large Capital on "Hero-Zero" OTM Lottery Trades:**
   - If you ever test an afternoon expiry breakout, risk **≤ 0.5% of account** (e.g., ₹500 on a ₹1,00,000 account) and accept upfront that the premium can go to ₹0 if the breakout fails.
2. **Switch to Next-Week Expiry for Clean Price Action:**
   - If you want to trade normal S/R and candlestick setups on Tuesday without extreme gamma whipsaws or instant theta wipeouts, simply select **next Tuesday's expiry** in TradePilot.
3. **Never Average Down an Expiring Option:**
   - An option bought at ₹40 that drops to ₹20 on expiry afternoon is usually headed to ₹0 — averaging down turns a small planned loss into an account-damaging blowup.
4. **Watch the Extra +2% ELM & No Calendar-Spread Margin Rule (2026):**
   - If selling options on expiry day, plan for the extra **2% Extreme Loss Margin (ELM)** and remember calendar spread margin relief no longer applies on the expiring leg (effective May 5, 2026).
5. **Close ITM Options Manually Before 15:25 IST:**
   - Do not let long ITM options expire into automatic exercise — square them off on the market to avoid **0.15% STT on intrinsic value** (post-April 2026) and settlement delays.
