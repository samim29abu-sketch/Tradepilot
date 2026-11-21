"""Reproducible 60-day live NSE backtest proof for TradePilot Dual-Engine Options Strategy.

Fetches real 5-minute and 15-minute historical data for NIFTY 50 (^NSEI) and
BANKNIFTY (^NSEBANK), simulates ATM/1-ITM option buying (Delta 0.55) with
conservative theta decay, bid-ask slippage, and April 2026 Indian statutory
charges (brokerage + 0.15% STT + NSE txn + stamp duty + 18% GST).

Run:
    python3 trading-knowledge/backtest_proof.py
"""
from collections import defaultdict
import datetime as dt
import json
from urllib.request import Request, urlopen

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))


def fetch_bars(symbol, rng="60d", interval="5m"):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={rng}&interval={interval}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=20) as resp:
        data = json.load(resp)["chart"]["result"][0]
    ts = data["timestamp"]
    q = data["indicators"]["quote"][0]
    rows = []
    for i, t in enumerate(ts):
        o, h, l, c = q["open"][i], q["high"][i], q["low"][i], q["close"][i]
        if None in (o, h, l, c):
            continue
        d = dt.datetime.fromtimestamp(t, IST)
        rows.append({
            "date": d.strftime("%Y-%m-%d"),
            "time": d.strftime("%H:%M"),
            "o": float(o), "h": float(h), "l": float(l), "c": float(c),
        })
    return rows


def ema(vals, period):
    out, k = [], 2.0 / (period + 1)
    for i, v in enumerate(vals):
        out.append(v if i == 0 else v * k + out[-1] * (1.0 - k))
    return out


def atr(bars, period=14):
    trs, out = [], []
    for i, b in enumerate(bars):
        tr = b["h"] - b["l"] if i == 0 else max(
            b["h"] - b["l"], abs(b["h"] - bars[i - 1]["c"]), abs(b["l"] - bars[i - 1]["c"])
        )
        trs.append(tr)
        out.append(sum(trs) / len(trs) if i < period else (out[-1] * (period - 1) + tr) / period)
    return out


def simulate_option_pnl(index_name, spot_move, hold_mins, lot_size):
    delta = 0.55
    theta_per_min = 0.05 if index_name == "NIFTY" else 0.11
    slip_opt_pts = 1.5 if index_name == "NIFTY" else 3.0
    charges_inr = 80.0 if index_name == "NIFTY" else 85.0
    opt_pts = spot_move * delta - theta_per_min * hold_mins - slip_opt_pts
    return round(opt_pts * lot_size - charges_inr, 2)


def run_backtest(index_name, symbol, lot_size, mode, trail_mode):
    bars5 = fetch_bars(symbol, "60d", "5m")
    bars15 = fetch_bars(symbol, "60d", "15m")
    by_day5, by_day15 = defaultdict(list), defaultdict(list)
    for b in bars5:
        by_day5[b["date"]].append(b)
    for b in bars15:
        by_day15[b["date"]].append(b)
    days = sorted(set(by_day5) & set(by_day15))

    all15 = [b for d in days for b in by_day15[d]]
    e9_15, e20_15 = ema([b["c"] for b in all15], 9), ema([b["c"] for b in all15], 20)
    idx15 = {(b["date"], b["time"]): i for i, b in enumerate(all15)}

    all5 = [b for d in days for b in by_day5[d]]
    e9_5 = ema([b["c"] for b in all5], 9)
    e20_5 = ema([b["c"] for b in all5], 20)
    e50_5 = ema([b["c"] for b in all5], 50)
    a14_5 = atr(all5, 14)
    idx5 = {(b["date"], b["time"]): i for i, b in enumerate(all5)}

    daily = {
        d: {
            "o": by_day5[d][0]["o"],
            "h": max(x["h"] for x in by_day5[d]),
            "l": min(x["l"] for x in by_day5[d]),
            "c": by_day5[d][-1]["c"],
        }
        for d in days
    }

    trades = []
    for di in range(2, len(days)):
        day = days[di]
        prev = daily[days[di - 1]]
        pdh, pdl = prev["h"], prev["l"]
        db = by_day5[day]
        if len(db) < 25:
            continue
        orb_bars = [x for x in db if x["time"] < "09:30"]
        if not orb_bars:
            continue
        orb_h, orb_l = max(x["h"] for x in orb_bars), min(x["l"] for x in orb_bars)
        pos, taken, day_pnl = None, 0, 0.0

        for i in range(3, len(db) - 2):
            b, t = db[i], db[i]["time"]
            g5 = idx5[(day, t)]
            hh, mm = int(t[:2]), int(t[3:])
            prev15 = ((hh * 60 + mm - 15) // 15) * 15
            t15 = f"{prev15 // 60:02d}:{prev15 % 60:02d}"
            g15 = idx15.get((day, t15)) or idx15.get((days[di - 1], "15:15"))
            if g15 is None:
                continue

            if pos:
                hit_sl = (b["l"] <= pos["sl"]) if pos["dir"] == "CE" else (b["h"] >= pos["sl"])
                hit_tg = (b["h"] >= pos["tg"]) if pos["dir"] == "CE" else (b["l"] <= pos["tg"])
                if hit_sl:
                    mv = (pos["sl"] - pos["entry"]) if pos["dir"] == "CE" else (pos["entry"] - pos["sl"])
                    pnl = simulate_option_pnl(index_name, mv, (i - pos["idx"]) * 5, lot_size)
                    trades.append({**pos, "exit": pos["sl"], "exit_t": t, "reason": pos["sl_tag"], "pnl": pnl, "spot_mv": mv})
                    day_pnl += pnl
                    pos = None
                elif hit_tg:
                    mv = (pos["tg"] - pos["entry"]) if pos["dir"] == "CE" else (pos["entry"] - pos["tg"])
                    pnl = simulate_option_pnl(index_name, mv, (i - pos["idx"]) * 5, lot_size)
                    trades.append({**pos, "exit": pos["tg"], "exit_t": t, "reason": "TARGET", "pnl": pnl, "spot_mv": mv})
                    day_pnl += pnl
                    pos = None
                else:
                    if trail_mode == "be1.5" and pos["sl_tag"] == "SL":
                        fav = (b["h"] - pos["entry"]) if pos["dir"] == "CE" else (pos["entry"] - b["l"])
                        if fav >= pos["risk"] * 1.5:
                            pos["sl"] = pos["entry"] + (3.0 if pos["dir"] == "CE" else -3.0)
                            pos["sl_tag"] = "BE"
                    elif trail_mode == "ema20" and (i - pos["idx"]) >= 3:
                        fav = (b["c"] - pos["entry"]) if pos["dir"] == "CE" else (pos["entry"] - b["c"])
                        if fav >= pos["risk"] * 1.5:
                            new_sl = e20_5[g5]
                            if pos["dir"] == "CE" and new_sl > pos["sl"]:
                                pos["sl"], pos["sl_tag"] = new_sl, "TRAIL"
                            elif pos["dir"] == "PE" and new_sl < pos["sl"]:
                                pos["sl"], pos["sl_tag"] = new_sl, "TRAIL"
                    if t >= "15:10":
                        mv = (b["c"] - pos["entry"]) if pos["dir"] == "CE" else (pos["entry"] - b["c"])
                        pnl = simulate_option_pnl(index_name, mv, (i - pos["idx"]) * 5, lot_size)
                        trades.append({**pos, "exit": b["c"], "exit_t": t, "reason": "EOD", "pnl": pnl, "spot_mv": mv})
                        day_pnl += pnl
                        pos = None
                continue

            if taken >= 2 or day_pnl <= -3000 or t < "09:30" or t > "14:15":
                continue

            cur_atr = max(a14_5[g5], 10.0)
            body = abs(b["c"] - b["o"])
            bull, bear = b["c"] > b["o"], b["c"] < b["o"]
            up_w, lo_w = b["h"] - max(b["o"], b["c"]), min(b["o"], b["c"]) - b["l"]
            pb = db[i - 1]
            htf_bull = e9_15[g15] > e20_15[g15] and all15[g15]["c"] > e20_15[g15]
            htf_bear = e9_15[g15] < e20_15[g15] and all15[g15]["c"] < e20_15[g15]
            sig, sl = None, None

            if mode == "PDH_PDL_BREAK_HOLD":
                if htf_bull and b["c"] > pdh and b["l"] <= pdh + cur_atr * 0.6 and bull and b["c"] > e9_5[g5] and b["c"] > pb["h"]:
                    sig, sl = "CE", min(b["l"], pdh - cur_atr * 0.35)
                elif htf_bear and b["c"] < pdl and b["h"] >= pdl - cur_atr * 0.6 and bear and b["c"] < e9_5[g5] and b["c"] < pb["l"]:
                    sig, sl = "PE", max(b["h"], pdl + cur_atr * 0.35)
            elif mode == "MTF_EMA_PULLBACK_NOCHOP":
                if "11:30" <= t < "13:15":
                    continue
                if htf_bull and e9_5[g5] > e20_5[g5] > e50_5[g5] and b["c"] > orb_h:
                    touched = b["l"] <= e20_5[g5] * 1.0005 or pb["l"] <= e20_5[g5 - 1] * 1.0005
                    if touched and bull and b["c"] > e9_5[g5] and (b["c"] > pb["h"] or lo_w >= body * 1.3):
                        sig, sl = "CE", min(b["l"], pb["l"]) - cur_atr * 0.15
                elif htf_bear and e9_5[g5] < e20_5[g5] < e50_5[g5] and b["c"] < orb_l:
                    touched = b["h"] >= e20_5[g5] * 0.9995 or pb["h"] >= e20_5[g5 - 1] * 0.9995
                    if touched and bear and b["c"] < e9_5[g5] and (b["c"] < pb["l"] or up_w >= body * 1.3):
                        sig, sl = "PE", max(b["h"], pb["h"]) + cur_atr * 0.15

            if sig and sl is not None:
                entry = db[i + 1]["o"]  # Next candle open — zero look-ahead bias
                risk = (entry - sl) if sig == "CE" else (sl - entry)
                if cur_atr * 0.8 <= risk <= cur_atr * 2.8:
                    tg = entry + risk * 3.0 if sig == "CE" else entry - risk * 3.0
                    pos = {
                        "index": index_name, "date": day, "time": db[i + 1]["time"], "idx": i + 1,
                        "dir": sig, "setup": mode, "entry": round(entry, 2), "sl": round(sl, 2),
                        "tg": round(tg, 2), "risk": round(risk, 2), "sl_tag": "SL",
                    }
                    taken += 1
    return days, trades


def summarize(title, trades):
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] <= 0]
    net = sum(t["pnl"] for t in trades)
    gp = sum(t["pnl"] for t in wins)
    gl = abs(sum(t["pnl"] for t in losses))
    pf = gp / gl if gl else 99.0
    eq, peak, mdd = 100000.0, 100000.0, 0.0
    for t in trades:
        eq += t["pnl"]
        peak = max(peak, eq)
        mdd = max(mdd, peak - eq)
    by_month = defaultdict(float)
    for t in trades:
        by_month[t["date"][:7]] += t["pnl"]
    print(f"\n{title}")
    print(f"  Trades: {len(trades)} | Win Rate: {len(wins)/len(trades)*100:.1f}% | Net P&L: ₹{net:+,.0f} ({net/1000:+.1f}%) | PF: {pf:.2f} | Max DD: ₹{mdd:,.0f}")
    print(f"  Avg Win: ₹{gp/len(wins):,.0f} | Avg Loss: ₹{gl/len(losses):,.0f} | Expectancy: ₹{net/len(trades):+,.0f}/trade")
    print("  Monthly:", ", ".join(f"{m}: ₹{v:+,.0f}" for m, v in sorted(by_month.items())))


if __name__ == "__main__":
    days_n, tr_n = run_backtest("NIFTY", "%5ENSEI", 65, "PDH_PDL_BREAK_HOLD", "ema20")
    days_b, tr_b = run_backtest("BANKNIFTY", "%5ENSEBANK", 30, "MTF_EMA_PULLBACK_NOCHOP", "be1.5")
    combined = sorted(tr_n + tr_b, key=lambda x: (x["date"], x["time"]))
    print(f"Period: {days_n[0]} to {days_n[-1]} ({len(days_n)} trading days)")
    summarize("NIFTY — PDH/PDL Break & Hold (1:3 R:R + 5m EMA20 Trail)", tr_n)
    summarize("BANKNIFTY — MTF 20-EMA Pullback No-Chop (1:3 R:R + BE 1.5R)", tr_b)
    summarize("COMBINED DUAL-ENGINE PORTFOLIO (₹1,00,000 Account, 1 Lot Each)", combined)
    print("\nLast 12 Trades:")
    for t in combined[-12:]:
        print(f"  {t['date']} {t['time']}->{t['exit_t']} | {t['index']:9s} {t['dir']} | {t['setup']:23s} | {t['entry']:8.1f} -> {t['exit']:8.1f} ({t['reason']:6s}) | ₹{t['pnl']:+,.0f}")
