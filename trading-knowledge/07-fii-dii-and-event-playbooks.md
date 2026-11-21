# 07 — FII / DII Institutional Flows & Event Trading Playbooks

## 1. NSE Participant-Wise Open Interest (Published Daily After Market Close)

Every evening (~18:00–19:30 IST), NSE publishes **Participant-Wise Open Interest** across four categories. Remember: **total market Longs always equal total market Shorts (net = 0)** — the edge comes from seeing *who* is taking which side.

| Participant | Who They Are | How to Interpret Their Positioning |
| --- | --- | --- |
| **FII (Foreign Institutional Investors)** | Global hedge funds, sovereign funds, foreign desks | Biggest directional trend drivers in index futures and large-cap cash flows. |
| **DII (Domestic Institutional Investors)** | Indian mutual funds, insurance, pension funds | Structural cash buyers (SIP inflows); mostly hedge equity portfolios via index futures/puts rather than pure directional speculation. |
| **Pro (Proprietary Desks)** | Broker prop desks, market makers, quant HFT desks | Dominant intraday **option writers** and liquidity providers; sharp at capturing range/expiry decay. |
| **Client (Retail & HNIs)** | Individual traders, family offices | Frequently crowded on the wrong side at extremes; heavy retail call buying during downtrends or put buying during rallies often acts as a contrarian warning. |

### Key FII Metrics to Track Daily
1. **FII Cash Market Net Flow (₹ Crore):** Sustained multi-day FII cash buying/selling sets the multi-week trend.
2. **FII Index Futures Long/Short Ratio:**
   $$\text{FII Long \%} = \frac{\text{FII Index Futures Long}}{\text{FII Long} + \text{FII Short}} \times 100$$
   - **> 65–70% Long:** Strong institutional bullish regime (or approaching overbought above 80%).
   - **40–60%:** Neutral / two-way market.
   - **< 25–30% Long (heavily short):** Strong bearish pressure, **but** extreme shorts (< 15–20%) create fuel for violent **short-covering rallies** on any positive catalyst.
3. **FII Index Options Net Change (Call Long vs. Call Short, Put Long vs. Put Short):**
   - Look at *both* sides: FIIs often **buy index Puts as portfolio hedges** when buying cash stocks (don't automatically read FII Put buying as pure bearishness unless they are also selling Cash + shorting Index Futures!).

---

## 2. High-Impact Indian Market Event Playbooks

### A. RBI Monetary Policy (MPC — Every 2 Months, 10:00 AM IST Announcement)
- **Most Sensitive Index:** **BANKNIFTY** & **FINNIFTY** (followed by NIFTY).
- **Pre-Event (Day Before & 09:15–10:00):** IV rises; price often chops in a narrow range before 10:00 AM.
- **10:00 – 10:30 AM (Governor Statement + Press Q&A):** Violent 2-way whipsaws (300–600 pt swings in BANKNIFTY in minutes). Option bid-ask spreads widen drastically.
- **Rule:** Never hold naked unhedged directional options through the exact 10:00 AM headline. Wait for the **first 15–30 minutes after the announcement** for whipsaws to settle and trade the clean post-event trend (or use defined-risk Debit/Credit Spreads).

### B. US Federal Reserve (FOMC) & US CPI / Non-Farm Payrolls (NFP)
- Announced during Indian night hours (FOMC ~23:30 / 00:30 IST; US CPI/NFP ~18:00 / 19:00 IST).
- Directly causes **large overnight gaps** in NIFTY/IT/Banking via GIFT NIFTY.
- **Rule:** Avoid carrying unhedged overnight short options or heavy naked long options into FOMC/US CPI nights — overnight gap risk bypasses your stop-loss completely.

### C. Union Budget Day (February 1) & Election Result Days
- Extreme **India VIX spike** in the week prior, followed by **massive IV Crush** during/immediately after the speech.
- Option buyers frequently lose money *even if they predict the direction right* because IV drops 20–40% in hours.
- **Rule:** Prefer **defined-risk spreads** (Bull Call / Bear Put Spreads neutralize much of the Vega/IV crush) or wait for the next day when volatility normalizes.

### D. Index Heavyweight Earnings (HDFC Bank, ICICI Bank, Reliance, TCS, Infosys)
- Earnings released after market hours or on weekends cause sharp opening gaps in the specific sector and index.
- Always check the **weekly earnings calendar** for top 5 NIFTY/BANKNIFTY stocks before carrying overnight positions.

### E. MSCI / FTSE / NSE Semi-Annual Rebalancing Days
- Huge passive institutional basket orders execute in the **final 30 minutes (15:00 – 15:30 IST)** on rebalancing effective dates.
- Causes abrupt, seemingly "irrational" spikes in specific stocks and index closes — avoid blind mean-reversion fading in the last 30 minutes on rebalancing days.
