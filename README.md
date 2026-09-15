# TradePilot v3 — Live Options Paper Terminal

TradePilot v3 is an installable phone-first PWA for **paper trading NIFTY and BANKNIFTY options with a ₹1,00,000 simulated account**.

## What it does

- Installable PWA from GitHub Pages.
- NIFTY 50 and NIFTY BANK live index prices from Angel One SmartAPI through a private backend.
- Current NIFTY / BANKNIFTY option expiries and nearby CE/PE contracts from Angel One's scrip master + Market Quote API.
- Manual paper BUY / SELL / EXIT.
- Paper stop-loss and target monitoring.
- Multiple open positions, open P&L, realized P&L, available paper funds, order/trade book.
- Command automation such as:
  - `BUY NIFTY 25000 CE QTY 75 SL 110 TARGET 160`
  - `BUY BANKNIFTY 54000 PE ABOVE 205 QTY 30 SL 175 TARGET 260`
  - `EXIT ALL`
- Rules execute **only as simulated paper trades** against received market prices.
- Automation runs on the private backend, so armed rules can continue while the phone screen is closed (as long as the server stays online).

## Security / architecture

The GitHub Pages frontend is public static code, so **Angel One credentials must never be stored in it**. The `server/` folder contains the private market-data backend. Put credentials only in `server/.env` on a private host such as AWS Lightsail.

The backend intentionally has **no Angel One `placeOrder` route**. It reads market data only. Real-money execution is a separate future stage after paper testing.

## Private backend setup

```bash
cd server
npm install
cp .env.example .env
# fill .env privately
npm start
```

Required server-only fields:

- `ANGEL_API_KEY`
- `ANGEL_CLIENT_CODE`
- `ANGEL_PIN`
- `ANGEL_TOTP_SECRET`
- `ANGEL_PUBLIC_IP` (use the server's whitelisted static outbound IP)
- `FRONTEND_ORIGIN=https://samim29abu-sketch.github.io`
- `APP_ACCESS_TOKEN` — a long private key; enter the same key once in the phone app Connection screen

The phone PWA needs an **HTTPS** backend URL. For local development, `http://localhost:3000` is also accepted.

## Install on Android

Open the GitHub Pages site in Chrome. Use the **Install TradePilot** button when shown, or Chrome menu → **Add to Home screen / Install app**.

## Important

This version simulates orders. It must remain clearly marked as paper trading even though the UI resembles a broker terminal. Option-selling margin shown in the frontend is an estimate for paper-account bookkeeping, not Angel One SPAN/exposure margin.
