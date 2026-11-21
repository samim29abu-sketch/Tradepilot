# TradePilot v4 — Live Options Paper Terminal & High-Reward Setup Radar

TradePilot v4 is an installable phone-first PWA for **paper trading NIFTY and BANKNIFTY options with a ₹1,00,000 simulated account**, now equipped with an automated **Dual-Engine High-Reward Setup Radar** backed by 60-day live NSE historical proof.

## What it does

- **Installable Phone App (PWA)** hosted on GitHub Pages (`https://samim29abu-sketch.github.io/Tradepilot/`).
- **Automated Daily Market Radar (Mon–Fri, 9:15 AM – 3:30 PM IST):** Continuously watches NIFTY 50 and BANKNIFTY 5m/15m price action on your private server:
  - **NIFTY Engine:** `PDH / PDL Break & Hold` (1:3 R:R + 5m EMA20 trailing stop)
  - **BANKNIFTY Engine:** `MTF 20-EMA Trend Pullback` (skips 11:30–13:15 midday chop, 1:3 R:R + Breakeven trail at 1.5R)
  - **Live Key Levels:** 15m Bias, PDH/PDL/PDC, 15m ORB, 5m EMA 20, ATR(14), and ATM Combined Straddle (`CE + PE`).
  - **1-Tap Arm** from your phone OR optional **Auto-Paper-Trade** mode with a `-₹3,000` daily max-loss kill switch, automatic breakeven trailing stop, and 15:10 IST intraday square-off.
  - **Optional Telegram Phone Alerts** whenever a live high-reward setup triggers.
- **Live 60-Day NSE Proof** documented in [`trading-knowledge/12-proven-strategy-and-backtest.md`](./trading-knowledge/12-proven-strategy-and-backtest.md) and reproducible via `python3 trading-knowledge/backtest_proof.py`.
- **Manual Paper Trading & Command Automation:**
  - `BUY NIFTY 25800 CE QTY 65 SL 110 TARGET 190`
  - `BUY BANKNIFTY 64600 PE ABOVE 205 QTY 30 SL 175 TARGET 295`
  - `EXIT ALL`
- **Realistic 2026 Cost Tracking:** Tracks estimated Indian charges (₹40 brokerage + 0.15% STT + NSE/SEBI/stamp + 18% GST) alongside paper P&L.

## Security / architecture

The GitHub Pages frontend is public static code, so **Angel One credentials must never be stored in it**. The private backend is bundled in [`install-tradepilot.py`](./install-tradepilot.py) and runs on your private host (e.g., AWS Lightsail) with credentials stored only in `.env`.

The backend intentionally has **no Angel One `placeOrder` route**. It reads market data only. Real-money execution is never triggered.

## Updating your private Lightsail backend

On your Lightsail host (as `admin`, not `sudo`):

```bash
curl -fsSL https://raw.githubusercontent.com/samim29abu-sketch/Tradepilot/main/install-tradepilot.py -o install-tradepilot.py
python3 install-tradepilot.py
```

Required server-only `.env` fields:
- `ANGEL_API_KEY`, `ANGEL_CLIENT_CODE`, `ANGEL_PIN`, `ANGEL_TOTP_SECRET`, `ANGEL_PUBLIC_IP`
- `FRONTEND_ORIGIN=https://samim29abu-sketch.github.io`
- `APP_ACCESS_TOKEN` (set during installer prompt; enter once in the phone app Connection screen)
- *(Optional)* `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` for instant Telegram phone alerts when a live setup fires.

## Install on Phone (Android / iPhone)

- **Android (Chrome):** Open `https://samim29abu-sketch.github.io/Tradepilot/` → tap **Install App** (or Chrome menu → **Add to Home screen / Install app**).
- **iPhone (Safari):** Open the site → Share button → **Add to Home Screen**.

## Trading Knowledge Base

The full 12-module Indian NSE options & price action knowledge base lives in [`trading-knowledge/`](./trading-knowledge/README.md).

## Important

This app simulates paper orders only. Past backtest performance does not guarantee future live results. Always validate setups across 30+ live paper trades before considering real capital.
