# 10 — Position Adjustments, Hedging & Trade Management

Good traders don't just know how to enter — they know **exactly how to manage a trade when price moves against them or stalls**.

---

## 1. Managing Naked Option Buying Positions

For option buyers, **simplicity and speed** beat complex adjustments:
- **Never hedge a bad naked buy by randomly buying the opposite option** ("locking in a loss" while paying double theta & double brokerage). If your price-action invalidation level breaks, **take the Stop-Loss immediately**.
- **Converting a Winning Buy into a Free Spread:**
  - Suppose you bought `25,000 CE` at ₹120 and NIFTY rallies so it's now ₹200, approaching major resistance at `25,200`.
  - Option 1: Trail SL to ₹170 and let it run.
  - Option 2: Sell `25,200 CE` at ₹100 → locks in a Bull Call Spread with reduced risk and protects against pullback/theta while keeping upside to 25,200. *(Requires spread margin in live trading.)*
- **Partial Profit Booking (2+ Lots):**
  - Book 50% at 1:1.5 or 1:2 (first S/R wall), move SL on the remaining 50% to breakeven, and trail below each 5m Higher Low / 9 EMA.

---

## 2. Adjusting Option Selling & Multi-Leg Spreads

When selling options (Iron Condor, Short Strangle, Credit Spread), **define your adjustment trigger BEFORE entry** (e.g., when spot touches your short strike, or when tested leg Delta hits `0.30–0.35`, or when untested leg drops to 30% of tested leg's price).

### A. Rolling the Untested Side (Iron Condor / Short Strangle)
- **Scenario:** You sold `24,700 PE` + `25,300 CE` (with protective wings). NIFTY rallies toward `25,250`, putting pressure on `25,300 CE`, while `24,700 PE` has melted from ₹60 to ₹15.
- **Adjustment:** Close `24,700 PE` (lock ₹45 profit) and sell a closer strike like `25,000 PE` for ₹60.
- **Result:** You collect extra credit, pushing your upside breakeven higher and balancing net Delta closer to neutral — **without adding extra directional risk on the downside** (as long as you don't roll past the tested strike!).

### B. Converting an Iron Condor into an Iron Fly
- If the market keeps trending into your short Call (`25,300 CE`), you can roll the short Put all the way up to the **same strike (`25,300 PE`)**, forming an **Iron Fly** (short straddle + protective wings).
- Maximizes credit collected and widens your breakeven zone significantly.
- **Stop Rolling Rule:** Once you form an Iron Fly, **do not invert** (don't roll the Put *above* the Call) unless you are an experienced trader — if spot breaks out past the Iron Fly breakeven, **exit cleanly at your max loss limit**.

### C. Adjusting a Breached Credit Spread (e.g., Bull Put Spread)
- If NIFTY drops toward your short Put in a Bull Put Spread:
  1. **Add an opposite Bear Call Spread** above spot (converting it into an Iron Condor) to collect extra credit and cut max loss — *only* if price shows resistance overhead.
  2. **Roll Out in Time:** Close the current week's losing spread and open a wider/lower strike spread in **next week's expiry** for a net credit or minimal debit — only if your broader thesis still holds.
  3. **Hard Stop-Loss Exit:** If structural support breaks decisively (e.g., Daily/15m BOS down), simply **close the spread at 1.5×–2× initial credit received**. Small losses are infinitely easier to recover than over-adjusted disasters.

---

## 3. Golden Rules of Adjustments

1. **Every adjustment costs brokerage, STT (0.15% on sell side), and slippage** — never adjust more than 1–2 times on a single trade.
2. **Never turn a defined-risk trade into an undefined-risk trade** (never remove your protective hedge wing to "save" a losing position!).
3. **Never add more lots to a losing trade** (martingale / doubling down works until one trend day wipes out 6 months of profits).
4. **Max Loss Hard Exit Overrides Every Adjustment:** If total strategy MTM hits your pre-planned max loss (e.g., 2% of capital), hit `EXIT ALL` — no exceptions.
