# 01 — Indian Options Market Rules & Specifications (2026)

## 1. Indian Market Timings (IST — UTC+5:30)

| Session | Time (IST) | What Happens |
| --- | --- | --- |
| Pre-Open Session (Equity) | 09:00 – 09:08 | Order entry/modification for NSE/BSE equities |
| Pre-Open Matching | 09:08 – 09:15 | Equilibrium opening price discovery (no F&O trading yet) |
| **Normal Market (F&O + Equity)** | **09:15 – 15:30** | Continuous trading for NIFTY/BANKNIFTY options & equities |
| Opening Volatility Window | 09:15 – 09:30 | Wide spreads, overnight gap digestion, fakeouts common |
| Prime Morning Trend Window | 09:30 – 11:30 | Best intraday directional setups and clean volume |
| Midday Chop Window | 11:30 – 13:30 | Often range-bound; theta decay erodes option buyers |
| Afternoon / European Open Window | 13:30 – 15:15 | Second liquidity wave; strong expiry moves (14:00–15:15) |
| Intraday Auto-Square-Off (MIS) | ~15:15 – 15:20 | Brokers auto-close intraday margin positions |
| Closing Session | 15:30 – 16:00 | Weighted average close calculated (last 30 mins: 15:00–15:30) |

---

## 2. Indian Index Option Lot Sizes & Expiry Calendar (As of Nov 2026)

Following SEBI's periodic lot-size reviews (NSE circular Oct 2025) and the one-weekly-expiry-per-exchange framework:

| Index | Exchange | Symbol | Lot Size (Nov 2026) | Weekly Expiry | Monthly Expiry | Settlement |
| --- | --- | --- | --- | --- | --- | --- |
| **NIFTY 50** | NSE | `NIFTY` | **65** | Every **Tuesday** | Last **Tuesday** | Cash |
| **NIFTY BANK** | NSE | `BANKNIFTY` | **30** | Discontinued | Last **Tuesday** | Cash |
| **NIFTY Fin Services** | NSE | `FINNIFTY` | **60** | Discontinued | Last **Tuesday** | Cash |
| **NIFTY Midcap Select** | NSE | `MIDCPNIFTY` | **120** | Discontinued | Last **Tuesday** | Cash |
| **NIFTY Next 50** | NSE | `NIFTYNXT50` | **25** | Discontinued | Last **Tuesday** | Cash |
| **BSE SENSEX** | BSE | `SENSEX` | **20** *(25 from Jan 2027)* | Every **Thursday** | Last **Thursday** | Cash |
| **BSE BANKEX** | BSE | `BANKEX` | **30** | Discontinued | Last **Thursday** | Cash |

- **Holiday Rule:** If an expiry day falls on a trading holiday, expiry moves to the **previous trading day**.
- **European Style (`CE` / `PE`):** Indian index options are European-style — they can only be exercised on expiry day (though you can buy/sell them in the market anytime before 15:30 on expiry).
- **Stock Options Warning:** Individual stock options on NSE are **physically settled** on monthly expiry. Holding ITM stock options into expiry can trigger full delivery obligations and heavy margin penalties — always square off before expiry.
- **TradePilot Note:** TradePilot's backend reads `lotsize` dynamically from Angel One's daily `OpenAPIScripMaster.json`, so order validation stays aligned with NSE's live lot sizes even when circulars change.

---

## 3. SEBI F&O Rules Every Trader Must Know (2025–2026)

1. **One Weekly Expiry Per Exchange:** NSE runs weekly options on **NIFTY** (Tuesday); BSE runs weekly options on **SENSEX** (Thursday). BANKNIFTY, FINNIFTY, MIDCPNIFTY, and BANKEX are monthly only.
2. **Higher Contract Values (₹15L–₹20L notional):** Periodic lot-size revisions keep notional contract value within SEBI's target band, raising per-lot capital needs.
3. **100% Upfront Option Premium Collection:** Brokers must collect full option buying premium upfront — no intraday leverage for buying options.
4. **Expiry-Day Extra Margin (+2% ELM):** Short index options carry an additional **2% Extreme Loss Margin (ELM)** on expiry day.
5. **No Calendar Spread Margin Benefit on Expiry Day (effective May 5, 2026):** Selling an expiring option against a longer-dated hedge no longer gets reduced calendar-spread margin on the expiry day of the near leg.
6. **Intraday Position Limit Monitoring:** Exchanges take random intraday snapshots of net/gross open positions against client limits.
7. **SEBI Retail Algo Trading Framework (mandatory April 1, 2026):**
   - Live API orders must come from a **whitelisted static IP** with daily 2FA authentication.
   - Algo orders must be tagged with a broker/exchange **Algo ID**.
   - Personal scripts sending fewer than **10 orders per second (OPS)** per exchange generally do not require separate exchange strategy registration, though broker static-IP & API tagging rules still apply.
   - *TradePilot currently operates in paper-only mode (no `placeOrder` route), avoiding live execution risk during testing.*

---

## 4. Transaction Costs & Taxes in Indian Options (Effective April 1, 2026)

Understanding real costs is critical — frequent scalping can look profitable in zero-fee paper trading while losing money after taxes and charges.

| Charge Component | NSE Options Rate (2026) | Applied On |
| --- | --- | --- |
| **Brokerage** | Flat ₹20 per executed order (typical discount broker) | Both Buy & Sell orders (₹40 round trip) |
| **STT — Option Sale** | **0.15%** *(hiked from 0.10% on Apr 1, 2026)* | Sell-side option premium value |
| **STT — Option Exercise** | **0.15%** *(hiked from 0.125% on Apr 1, 2026)* | Intrinsic value (paid by buyer if ITM option is exercised instead of squared off) |
| **NSE Transaction Charge** | ~0.03503% (flat true-to-label structure) | Both Buy & Sell premium value |
| **Stamp Duty** | 0.003% (₹300 per crore) | Buy-side premium value only |
| **SEBI Turnover Fee** | 0.0001% (₹10 per crore) | Both Buy & Sell premium value |
| **IPFT (NSE)** | ~0.0005% on options premium (check latest NSE circular) | Both Buy & Sell premium value |
| **GST** | 18% | On (Brokerage + Exchange Txn + SEBI + IPFT) |

### Example Breakeven Cost (1 Lot NIFTY = 65 Qty)
- Buy 1 lot at ₹150 (value = ₹9,750), Sell 1 lot at ₹150 (value = ₹9,750):
  - Brokerage: ₹40.00
  - STT (0.15% on ₹9,750): ₹14.63
  - Exchange Txn + SEBI + IPFT (~0.036% on ₹19,500): ~₹7.02
  - Stamp Duty (0.003% on ₹9,750): ₹0.29
  - GST (18% on ₹47.02): ~₹8.46
  - **Total round-trip cost ≈ ₹70.40** → You need **~1.1 points** just to break even on 1 lot (plus bid-ask slippage of 0.5–2 points).
- **Exercise Trap Warning:** Always **square off ITM options before 15:30** on expiry day. If you buy a 25,000 CE for ₹10 and NIFTY settles at 25,015 (intrinsic value = ₹15), STT on exercise is 0.15% of intrinsic value (post-Budget 2026), and broker exercise charges/settlement slippage can eat the profit.

### Income Tax Treatment (India)
- F&O trading profits/losses are treated as **Non-Speculative Business Income** (ITR-3).
- STT, brokerage, internet, and trading-related expenses are deductible as business expenses.
- F&O losses can be set off against other business income (except salary) and carried forward for up to **8 assessment years** (if ITR is filed on time).

---

## 5. Angel One SmartAPI Data Available for TradePilot

Currently, TradePilot uses:
- `OpenAPIScripMaster.json` — daily instrument/token/lot-size directory.
- `POST /rest/secure/angelbroking/market/v1/quote/` (`mode: "FULL"`) — live LTP, net change, percent change, exchange timestamp, plus **OHLC, volume, OI, depth** when read from full quotes.

Additional SmartAPI endpoints that can power advanced TradePilot features:
- **Historical Candle API (`getCandleData`):** `ONE_MINUTE`, `THREE_MINUTE`, `FIVE_MINUTE`, `FIFTEEN_MINUTE`, `THIRTY_MINUTE`, `ONE_HOUR`, `ONE_DAY` candles for NSE indices & NFO contracts — ideal for auto-computing PDH/PDL, EMAs, VWAP, candlesticks, and S/R zones.
- **Option Greeks API (`/marketData/v1/optionGreek`):** Returns Delta, Gamma, Theta, Vega, and IV per strike/expiry.
- **Historical OI API / Market WebSocket v2:** Real-time streaming ticks and Open Interest buildup without polling delays.
