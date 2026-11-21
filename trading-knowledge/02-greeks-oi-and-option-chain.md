# 02 — Option Pricing, Greeks, IV & Option Chain Analysis

## 1. Option Anatomy & Moneyness

Suppose **NIFTY Spot = 25,000**:

| Classification | Call Option (`CE`) | Put Option (`PE`) | Composition of Premium |
| --- | --- | --- | --- |
| **ITM (In The Money)** | Strike < 25,000 (e.g., 24,800 CE) | Strike > 25,000 (e.g., 25,200 PE) | Intrinsic Value + Time Value |
| **ATM (At The Money)** | Strike ≈ 25,000 (25,000 CE) | Strike ≈ 25,000 (25,000 PE) | Almost 100% Time Value (highest liquidity & highest Theta/Gamma) |
| **OTM (Out of The Money)** | Strike > 25,000 (e.g., 25,200 CE) | Strike < 25,000 (e.g., 24,800 PE) | 100% Time Value — expires at **₹0** if spot doesn't cross strike |

### Intrinsic Value vs. Time Value
- **Call Intrinsic Value** = $\max(0, \text{Spot} - \text{Strike})$
- **Put Intrinsic Value** = $\max(0, \text{Strike} - \text{Spot})$
- **Time Value (Extrinsic Value)** = $\text{Option Premium} - \text{Intrinsic Value}$
- **Breakeven at Expiry:**
  - Long Call: $\text{Strike} + \text{Premium Paid}$
  - Long Put: $\text{Strike} - \text{Premium Paid}$

---

## 2. The Option Greeks (Practical Intraday Meaning)

| Greek | Measures | Range / Behavior | Practical Trading Impact |
| --- | --- | --- | --- |
| **Delta ($\Delta$)** | Option price change per +1 pt move in underlying | CE: `0` to `+1` (ATM ≈ `+0.50`)<br>PE: `-1` to `0` (ATM ≈ `-0.50`) | Roughly approximates probability of expiring ITM. Buy **Delta 0.50–0.65** (ATM / 1–2 strikes ITM) for cleaner directional moves. |
| **Gamma ($\Gamma$)** | Rate of change of Delta per 1 pt move in underlying | Highest at **ATM**; explodes on **expiry day** | Causes "gamma spikes" (hero-zero surges or instant wipeouts) on Tuesday NIFTY expiry. Dangerous for unhedged sellers. |
| **Theta ($\Theta$)** | Daily premium decay from passage of time | Negative for buyers, positive for sellers | Decay is **non-linear** — accelerates rapidly in the final 2–3 days before expiry. Weekend decay is often priced in Friday afternoon / Monday open. |
| **Vega ($\nu$)** | Premium change per +1% change in Implied Volatility (IV) | Highest at **ATM** & longer-dated expiries | Rising IV inflates both CE & PE premiums. Falling IV (**IV Crush**) can cause an option to **lose money even if direction is right**. |
| **Rho ($\rho$)** | Sensitivity to interest rates | Minor for weekly/monthly options | Mostly relevant for long-term options; explains futures premium over spot. |

---

## 3. Implied Volatility (IV) & India VIX

- **India VIX** measures the market's expected 30-day annualized volatility of NIFTY 50.
  - **Low VIX (< 12–13):** Calm/trending or slow grinding markets; cheap option premiums (favorable for option buyers on breakouts; tight ranges can hurt if choppy).
  - **Normal VIX (13–18):** Healthy intraday swings; balanced for both buyers and sellers.
  - **High VIX (> 20):** Fear, news, RBI policy, Union Budget, elections, global shocks. Wide candles, massive premiums — **never buy far-OTM options right before a known event** because IV collapses immediately after the announcement (**IV Crush**).
- **Rule of Thumb (Expected Daily Move from VIX):**
  $$\text{Approx. 1-Day Expected Move (\%)} \approx \frac{\text{India VIX}}{\sqrt{252}} \approx \frac{\text{India VIX}}{15.87}$$
  *Example:* If India VIX = 16, NIFTY's typical 1-day expected range is ~±1% (~±250 points at 25,000).

---

## 4. Reading the NSE Option Chain (OI, Change in OI, PCR, Max Pain)

**Core Rule of Indian Option Chain Analysis:** Always interpret Open Interest (**OI**) from the perspective of **Option Sellers (Writers)**, because writing options requires large institutional margin and high conviction.

- **Highest Call OI Strike** → Major **Resistance** (Call writers defending that ceiling).
- **Highest Put OI Strike** → Major **Support** (Put writers defending that floor).
- **Change in OI (Intraday):** Much more important for intraday trading than total OI.
  - Heavy **Put Writing (+PE OI)** at a strike while price rises = rising support (bullish conviction).
  - Heavy **Call Writing (+CE OI)** at a strike while price falls = strengthening resistance (bearish conviction).
  - **Short Covering / Trap (Unwinding):** When spot breaks above the highest Call OI strike and **Call OI starts dropping rapidly (`-CE OI`)**, trapped Call writers are forced to buy back — this triggers a **fast short-covering rally** (one of the best setups for Call buyers).

### Futures Price + OI 4-Quadrant Matrix

| Price | Open Interest (OI) | Market Interpretation | Bias |
| --- | --- | --- | --- |
| Rising | Rising | **Long Buildup** (fresh buyers entering) | Strongly Bullish |
| Falling | Rising | **Short Buildup** (fresh sellers entering) | Strongly Bearish |
| Rising | Falling | **Short Covering** (bears exiting shorts) | Bullish squeeze (watch for exhaustion) |
| Falling | Falling | **Long Unwinding** (bulls booking profit/exiting) | Bearish pullback |

### Put-Call Ratio (PCR)
$$\text{PCR (OI)} = \frac{\text{Total Put OI}}{\text{Total Call OI}}$$

| PCR Zone | Meaning | Actionable Context |
| --- | --- | --- |
| `< 0.60` | Oversold / Extreme Call writing | Bearish momentum, but watch for sharp short-covering bounce at support |
| `0.70 – 0.90` | Mildly bearish to neutral | Favour PE near resistance |
| `0.90 – 1.15` | Balanced / Range-bound | Sideways chop likely; avoid chasing breakouts |
| `1.15 – 1.40` | Bullish (strong Put writing support) | Favour CE on pullbacks to support/VWAP |
| `> 1.50` | Overbought / Extreme Put writing | Bullish trend, but high risk of sharp profit-booking pullback |

*Note: Intraday **Change-in-OI PCR** (nearby ±5 strikes around ATM) reacts faster than overall chain PCR.*

### Max Pain
- The strike price at which option buyers as a group lose the most money (and option writers keep the maximum premium) at expiry.
- Useful mainly in the final 1–2 days before expiry as a **magnet / drift zone** during range-bound days — **never fight a strong trend solely because of Max Pain**.

---

## 5. Strike Selection Guidelines (Option Buying)

1. **Best Default Strikes:** **ATM** or **1–2 strikes ITM** (Delta `0.50 – 0.65`). They move smoothly with spot and suffer far less percentage theta decay than OTM options.
2. **Avoid Deep OTM "Lottery Tickets":** Far OTM strikes (Delta < 0.20) require a massive, immediate move just to overcome theta and spread slippage.
3. **Check Liquidity:** Look for tight bid-ask spreads (≤ ₹0.25–₹1.00) and high volume/OI. Round-number strikes (e.g., NIFTY 25000, 25100) have the best liquidity.
4. **Expiry-Day Rule:** On expiry day, avoid buying the same-day expiring OTM options after 12:30 PM unless trading a confirmed breakout with strict SL. If holding a swing or cleaner intraday move, consider switching to the **next week's expiry** to avoid extreme gamma/theta whipsaws.
