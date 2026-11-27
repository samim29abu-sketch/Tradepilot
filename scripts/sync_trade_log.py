#!/usr/bin/env python3
"""Sync live paper trades & daily 15:15 IST summaries from the TradePilot backend to GitHub."""
from collections import defaultdict
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "trading-knowledge" / "live-trades.json"
MD_PATH = ROOT / "trading-knowledge" / "live-proof-journal.md"
DEFAULT_BACKEND_URL = "https://tradepilot.16-4-2-101.sslip.io"
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
NSE_HOLIDAYS = {"2026-11-24", "2026-12-25"}
JOURNAL_NOTES_MARKER = "## Trade Notes & Model Audit"
JOURNAL_MANAGED_TAG = "<!-- AUTO-LOG-MANAGED -->"


def now_ist():
    return dt.datetime.now(IST)


def estimate_option_charges(buy_price, sell_price, qty):
    """Estimate April 2026 NSE options round-trip charges (INR)."""
    buy_val = max(0.0, float(buy_price)) * qty
    sell_val = max(0.0, float(sell_price)) * qty
    turnover = buy_val + sell_val
    brokerage = 40.0
    stt = sell_val * 0.0015
    exch_sebi = turnover * 0.00036
    stamp = buy_val * 0.00003
    gst = 0.18 * (brokerage + exch_sebi)
    return round(brokerage + stt + exch_sebi + stamp + gst, 2)


def infer_underlying(symbol):
    sym = str(symbol or "").upper()
    if sym.startswith("BANKNIFTY"):
        return "BANKNIFTY"
    if sym.startswith("NIFTY"):
        return "NIFTY"
    return ""


def infer_engine(symbol, source="MANUAL"):
    src = str(source or "MANUAL").upper()
    if src == "SCANNER":
        u = infer_underlying(symbol)
        if u == "BANKNIFTY":
            return "MTF 20-EMA Pullback"
        if u == "NIFTY":
            return "PDH/PDL Break & Hold"
        return "Scanner"
    if src == "RULE":
        return "Manual Rule"
    return "Manual"


def fmt_inr(val, signed=False):
    n = round(float(val or 0.0), 2)
    if n == 0:
        return "₹0.00"
    if n > 0:
        return f"+₹{n:,.2f}" if signed else f"₹{n:,.2f}"
    return f"-₹{abs(n):,.2f}"


def fmt_ist_hms(iso_str):
    s = str(iso_str or "")
    return s[11:19] if len(s) >= 19 and s[10] in ("T", " ") else (s or "—")


def backfill_trades_from_orders(orders):
    """Reconstruct closed trades chronologically from /api/paper/state orders."""
    open_q = defaultdict(list)
    trades = []
    for o in orders or []:
        sym = str(o.get("symbol") or "")
        if not sym:
            continue
        status = str(o.get("status") or "")
        pnl = o.get("pnl")
        qty = int(o.get("qty") or 0)
        price = float(o.get("price") or 0.0)
        if status == "FILLED" and pnl is None:
            open_q[sym].append(o)
            continue
        if pnl is None or qty <= 0:
            continue
        q_list = open_q[sym]
        match_i = next((i for i, e in enumerate(q_list) if int(e.get("qty") or 0) == qty), 0 if q_list else None)
        entry_o = q_list.pop(match_i) if match_i is not None else None
        if entry_o:
            entry_side = str(entry_o.get("side") or "BUY").upper()
            entry_price = round(float(entry_o.get("price") or price), 2)
            entry_time = str(entry_o.get("time") or o.get("time") or "")
            source = str(entry_o.get("source") or o.get("source") or "MANUAL")
        else:
            entry_side = "BUY"
            entry_price = round(price - (float(pnl) / qty), 2)
            entry_time = str(o.get("time") or "")
            source = str(o.get("source") or "MANUAL")
        exit_time = str(o.get("time") or "")
        exit_price = round(price, 2)
        gross = round(float(pnl), 2)
        if o.get("charges") is not None:
            charges = round(float(o["charges"]), 2)
        else:
            buy_p, sell_p = (entry_price, exit_price) if entry_side == "BUY" else (exit_price, entry_price)
            charges = estimate_option_charges(buy_p, sell_p, qty)
        pts = round((exit_price - entry_price) * (1 if entry_side == "BUY" else -1), 2)
        net = round(gross - charges, 2)
        tid = hashlib.sha1(f"{entry_time}|{exit_time}|{sym}|{qty}|{exit_price}".encode()).hexdigest()[:16]
        trades.append({
            "id": tid,
            "date": exit_time[:10] if len(exit_time) >= 10 else "",
            "entryTime": entry_time,
            "exitTime": exit_time,
            "symbol": sym,
            "underlying": infer_underlying(sym),
            "engine": infer_engine(sym, source),
            "source": source,
            "side": entry_side,
            "qty": qty,
            "entry": entry_price,
            "exit": exit_price,
            "pts": pts,
            "exitType": status or "EXIT",
            "grossPnl": gross,
            "charges": charges,
            "netPnl": net,
        })
    return trades


def compute_trade_metrics(trades):
    total = len(trades)
    wins = [t for t in trades if float(t.get("netPnl") or 0) > 0]
    losses = [t for t in trades if float(t.get("netPnl") or 0) <= 0]
    gross = round(sum(float(t.get("grossPnl") or 0) for t in trades), 2)
    charges = round(sum(float(t.get("charges") or 0) for t in trades), 2)
    net = round(sum(float(t.get("netPnl") or 0) for t in trades), 2)
    avg_win = round(sum(float(t["netPnl"]) for t in wins) / len(wins), 2) if wins else 0.0
    avg_loss = round(abs(sum(float(t["netPnl"]) for t in losses) / len(losses)), 2) if losses else 0.0
    win_sum = sum(float(t["netPnl"]) for t in wins)
    loss_sum = abs(sum(float(t["netPnl"]) for t in losses))
    peak, eq, max_dd, max_dd_pct = 100000.0, 100000.0, 0.0, 0.0
    for t in trades:
        eq += float(t.get("netPnl") or 0)
        if eq > peak:
            peak = eq
        dd = peak - eq
        if dd > max_dd:
            max_dd = dd
            max_dd_pct = (dd / peak) * 100.0 if peak > 0 else 0.0
    return {
        "completedTrades": total,
        "targetTrades": 30,
        "wins": len(wins),
        "losses": len(losses),
        "winRatePct": round((100.0 * len(wins) / total), 1) if total else 0.0,
        "grossRealized": gross,
        "estimatedCharges": charges,
        "netRealized": net,
        "returnPct": round((100.0 * net / 100000.0), 2),
        "avgWinNet": avg_win,
        "avgLossNet": avg_loss,
        "rewardRiskRatio": round(avg_win / avg_loss, 2) if (wins and losses and avg_loss > 0) else None,
        "profitFactor": round(win_sum / loss_sum, 2) if loss_sum > 0 else None,
        "maxDrawdownInr": round(max_dd, 2),
        "maxDrawdownPct": round(max_dd_pct, 2),
    }


def build_session_summary(date_str, trades, state, scanner_data=None, prev_session=None, now=None):
    cur = now or now_ist()
    day_trades = [t for t in trades if t.get("date") == date_str]
    wins = sum(1 for t in day_trades if float(t.get("netPnl") or 0) > 0)
    losses = len(day_trades) - wins
    gross = round(sum(float(t.get("grossPnl") or 0) for t in day_trades), 2)
    charges = round(sum(float(t.get("charges") or 0) for t in day_trades), 2)
    net = round(sum(float(t.get("netPnl") or 0) for t in day_trades), 2)
    cfg = state.get("scannerCfg") or {}
    daily = state.get("daily") or {}
    auto_on = bool(cfg.get("autoTrade", False))

    def idx_info(name):
        ix = ((scanner_data or {}).get("indices") or {}).get(name) or {}
        if ix.get("spot") is None:
            return None
        setups_today = sum(1 for s in (ix.get("recentSetups") or []) if s.get("date") == date_str)
        return {"spot": round(float(ix["spot"]), 2), "htfBias": ix.get("htfBias", "—"), "setupsToday": setups_today}

    prev = prev_session or {}
    nf = idx_info("NIFTY") or prev.get("nifty")
    bn = idx_info("BANKNIFTY") or prev.get("banknifty")
    if day_trades:
        note = f"{len(day_trades)} trade(s) completed ({wins}W/{losses}L)"
    elif not auto_on:
        note = "0 trades — Auto-Paper-Trade was OFF"
    else:
        note = "0 trades — no valid 1:3 R:R trigger"
    if daily.get("killSwitchHit") and daily.get("date") == date_str:
        note += " • kill-switch hit"
    return {
        "date": date_str,
        "recordedAt": prev.get("recordedAt") or cur.isoformat(),
        "tradesCount": len(day_trades),
        "wins": wins,
        "losses": losses,
        "grossPnl": gross,
        "charges": charges,
        "netPnl": net,
        "autoTrade": auto_on,
        "killSwitchHit": bool(daily.get("killSwitchHit") and daily.get("date") == date_str),
        "openPositions": len(state.get("positions") or []),
        "nifty": nf,
        "banknifty": bn,
        "note": note,
    }


def extract_preserved_notes(existing_md):
    if existing_md and JOURNAL_NOTES_MARKER in existing_md:
        idx = existing_md.index(JOURNAL_NOTES_MARKER)
        return existing_md[idx:].strip() + "\n"
    return (
        f"{JOURNAL_NOTES_MARKER}\n\n"
        "_Add manual trade observations or model audit notes below this heading — "
        "auto-sync always preserves this section._\n"
    )


def render_journal_markdown(payload, preserved_notes=None):
    m = payload["metrics"]
    trades = payload["trades"]
    sessions = payload["sessions"]
    cfg = payload["scannerConfig"]
    sync_ts = str(payload.get("updatedAt") or "")
    sync_disp = (sync_ts[:10] + " " + sync_ts[11:19] + " IST") if len(sync_ts) >= 19 else sync_ts
    auto_str = "ON" if cfg.get("autoTrade") else "OFF"

    wr_str = f"{m['wins']} W / {m['losses']} L ({m['winRatePct']:.1f}%)" if m["completedTrades"] else "0 W / 0 L (—)"
    avg_win_s = fmt_inr(m["avgWinNet"], signed=True) if m["wins"] else "—"
    avg_loss_s = fmt_inr(-m["avgLossNet"], signed=True) if m["losses"] else "—"
    rr_suffix = f" ({m['rewardRiskRatio']:.2f}×)" if m["rewardRiskRatio"] is not None else ""
    pf_str = f"{m['profitFactor']:.2f}" if m["profitFactor"] is not None else "—"
    ret_sign = "+" if m["returnPct"] > 0 else ""

    lines = [
        "# TradePilot Live Forward-Testing Proof Journal (Target: 30 Live Trades)",
        JOURNAL_MANAGED_TAG,
        "",
        "Real-time automated forward proof of **TradePilot Dual-Engine Strategy** executed against live **Angel One SmartAPI** option quotes on the ₹1,00,000 simulated paper account.",
        f"_Last auto-sync: `{sync_disp}` • Auto-Paper-Trade: `{auto_str}` • Machine-readable log: [`live-trades.json`](./live-trades.json)_",
        "",
        "## Live Running Scorecard",
        "",
        "| Metric | Live Result (So Far) | 30-Trade Proof Target |",
        "| --- | ---: | ---: |",
        f"| **Completed Live Trades** | **{m['completedTrades']} / {m['targetTrades']}** | 30+ |",
        f"| **Wins / Losses** | **{wr_str}** | ≥ 35% WR |",
        f"| **Gross Realized P&L** | **{fmt_inr(m['grossRealized'], signed=True)}** | — |",
        f"| **Est. 2026 Charges (Brokerage + 0.15% STT + Taxes)** | **{fmt_inr(-m['estimatedCharges'], signed=True)}** | — |",
        f"| **Net Realized P&L** | **{fmt_inr(m['netRealized'], signed=True)} ({ret_sign}{m['returnPct']:.2f}%)** | Positive (+8% to +15%+) |",
        f"| **Avg Win / Avg Loss (Net)** | **{avg_win_s} / {avg_loss_s}{rr_suffix}** | ≥ 1.8× |",
        f"| **Profit Factor (Net)** | **{pf_str}** | ≥ 1.25 |",
        f"| **Max Drawdown** | **{fmt_inr(m['maxDrawdownInr'])} ({m['maxDrawdownPct']:.1f}%)** | ≤ ₹15,000 (15%) |",
        "",
        "---",
        "",
        "## Live Verified Trade Log",
        "",
    ]
    if trades:
        lines.extend([
            "| # | Date | Entry → Exit (IST) | Instrument | Engine | Side | Qty | Entry (₹) | Exit (₹) | Pts | Exit Type | Gross P&L | Est. Charges | **Net P&L** |",
            "| ---: | --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: |",
        ])
        for i, t in enumerate(trades, 1):
            pts = float(t.get("pts") or 0.0)
            pts_s = f"{'+' if pts > 0 else ''}{pts:,.2f}"
            times = f"{fmt_ist_hms(t.get('entryTime'))} → {fmt_ist_hms(t.get('exitTime'))}"
            lines.append(
                f"| {i} | {t.get('date', '—')} | {times} | `{t.get('symbol', '—')}` | "
                f"{t.get('engine', '—')} | {t.get('side', 'BUY')} | {int(t.get('qty') or 0)} | "
                f"{float(t.get('entry') or 0):,.2f} | {float(t.get('exit') or 0):,.2f} | {pts_s} | "
                f"{t.get('exitType', 'EXIT')} | {fmt_inr(t.get('grossPnl'), signed=True)} | "
                f"{fmt_inr(t.get('charges'))} | **{fmt_inr(t.get('netPnl'), signed=True)}** |"
            )
    else:
        lines.append("_No closed paper trades logged yet._")

    lines.extend([
        "",
        "---",
        "",
        "## Daily Session Log (15:15 IST Auto-Check)",
        "",
    ])
    if sessions:
        lines.extend([
            "| Date | Trades | W / L | Net P&L | Auto-Trade | NIFTY (Spot / 15m Bias) | BANKNIFTY (Spot / 15m Bias) | Status |",
            "| --- | ---: | :---: | ---: | :---: | --- | --- | --- |",
        ])
        for s in sessions:
            nf = s.get("nifty") or {}
            bn = s.get("banknifty") or {}
            nf_s = f"{nf['spot']:,.1f} / {nf.get('htfBias', '—')}" if nf.get("spot") is not None else "—"
            bn_s = f"{bn['spot']:,.1f} / {bn.get('htfBias', '—')}" if bn.get("spot") is not None else "—"
            at_s = "ON" if s.get("autoTrade") else "OFF"
            lines.append(
                f"| {s.get('date', '—')} | {int(s.get('tradesCount') or 0)} | "
                f"{int(s.get('wins') or 0)} / {int(s.get('losses') or 0)} | "
                f"{fmt_inr(s.get('netPnl'), signed=True)} | {at_s} | {nf_s} | {bn_s} | "
                f"{s.get('note', '—')} |"
            )
    else:
        lines.append("_Daily 15:15 IST session summaries will appear here automatically on trading days._")

    lines.extend(["", "---", "", extract_preserved_notes(preserved_notes).rstrip(), ""])
    return "\n".join(lines)


def semantic_view(payload):
    if not isinstance(payload, dict):
        return None
    sessions = []
    for s in payload.get("sessions") or []:
        sessions.append({k: v for k, v in s.items() if k != "recordedAt"})
    return {
        "metrics": payload.get("metrics"),
        "trades": payload.get("trades"),
        "sessions": sessions,
        "scannerConfig": payload.get("scannerConfig"),
    }


def fetch_json(url, app_key, timeout=25):
    req = Request(url, headers={"X-TradePilot-Key": app_key, "Accept": "application/json", "User-Agent": "TradePilot-Sync/4"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def sync_files(state, scanner_data=None, json_path=JSON_PATH, md_path=MD_PATH, now=None, force_session=False):
    cur = now or now_ist()
    trades = list(state.get("trades") or [])
    if not trades and state.get("orders"):
        trades = backfill_trades_from_orders(state["orders"])

    existing_json = None
    if json_path.is_file():
        try:
            existing_json = json.loads(json_path.read_text(encoding="utf-8"))
        except ValueError:
            existing_json = None
    existing_md = md_path.read_text(encoding="utf-8") if md_path.is_file() else ""

    sessions_by_date = {}
    for s in (existing_json or {}).get("sessions") or []:
        if isinstance(s, dict) and s.get("date"):
            sessions_by_date[s["date"]] = dict(s)
    for d_str, s in (state.get("sessions") or {}).items():
        if isinstance(s, dict):
            sessions_by_date[d_str] = dict(s)

    today = cur.date().isoformat()
    is_trading_day = cur.weekday() < 5 and today not in NSE_HOLIDAYS
    if is_trading_day and (cur.time() >= dt.time(15, 15) or force_session):
        sessions_by_date[today] = build_session_summary(
            today, trades, state, scanner_data=scanner_data,
            prev_session=sessions_by_date.get(today), now=cur,
        )

    ordered_dates = sorted(sessions_by_date.keys())[-180:]
    sessions = [sessions_by_date[d] for d in ordered_dates]

    metrics = compute_trade_metrics(trades)
    cfg = state.get("scannerCfg") or {}
    acct = state.get("account") or {}
    net_equity = round(100000.0 + metrics["netRealized"] + float(acct.get("openPnl") or 0.0), 2)
    payload = {
        "schemaVersion": 1,
        "updatedAt": cur.isoformat(),
        "account": {
            "startingCapital": 100000,
            "equityGross": round(float(acct.get("equity") or (100000.0 + metrics["grossRealized"])), 2),
            "equityNet": net_equity,
            "grossRealized": metrics["grossRealized"],
            "estimatedCharges": metrics["estimatedCharges"],
            "netRealized": metrics["netRealized"],
            "returnPct": metrics["returnPct"],
            "openPositions": len(state.get("positions") or []),
        },
        "metrics": metrics,
        "scannerConfig": {
            "autoTrade": bool(cfg.get("autoTrade", False)),
            "maxDailyLoss": float(cfg.get("maxDailyLoss", 3000)),
            "maxDailyTrades": int(cfg.get("maxDailyTrades", 4)),
        },
        "trades": trades,
        "sessions": sessions,
    }

    already_managed = JOURNAL_MANAGED_TAG in existing_md
    if already_managed and semantic_view(existing_json) == semantic_view(payload):
        return {"changed": False, "trades": len(trades), "sessions": len(sessions), "commitMessage": ""}

    preserved = extract_preserved_notes(existing_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    md_path.write_text(render_journal_markdown(payload, preserved), encoding="utf-8")

    old_count = len((existing_json or {}).get("trades") or [])
    if len(trades) > old_count and trades:
        last = trades[-1]
        msg = f"Auto-log trade #{len(trades)}: {last['symbol']} ({fmt_inr(last['netPnl'], signed=True)} net)"
    elif today in sessions_by_date:
        s = sessions_by_date[today]
        msg = f"Auto-log daily session ({today}: {s['tradesCount']} trade{'s' if s['tradesCount'] != 1 else ''}, {fmt_inr(s['netPnl'], signed=True)})"
    else:
        msg = f"Auto-log TradePilot journal ({len(trades)} trades, {fmt_inr(metrics['netRealized'], signed=True)} net)"
    return {"changed": True, "trades": len(trades), "sessions": len(sessions), "commitMessage": msg}


def main():
    app_key = (os.environ.get("TRADEPILOT_APP_KEY") or "").strip()
    if not app_key:
        print(
            "Error: Missing GitHub Actions secret TRADEPILOT_APP_KEY.\n"
            "Add your TradePilot App Access Key under: Repo Settings -> Secrets and variables -> Actions -> New repository secret.",
            file=sys.stderr,
        )
        return 1
    backend_url = (os.environ.get("TRADEPILOT_BACKEND_URL") or DEFAULT_BACKEND_URL).strip().rstrip("/")
    force_session = os.environ.get("FORCE_SESSION", "0").strip() == "1"

    try:
        state = fetch_json(backend_url + "/api/paper/state", app_key)
    except HTTPError as e:
        if e.code == 401:
            print("Error: Backend returned HTTP 401 — check that TRADEPILOT_APP_KEY matches your TradePilot App Access Key.", file=sys.stderr)
        else:
            print(f"Error: Backend returned HTTP {e.code} on /api/paper/state.", file=sys.stderr)
        return 1
    except URLError as e:
        print(f"Error: Could not reach TradePilot backend ({type(e.reason).__name__}).", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: Failed to read paper state ({type(e).__name__}).", file=sys.stderr)
        return 1

    scanner_data = None
    try:
        scanner_data = fetch_json(backend_url + "/api/scanner", app_key)
    except Exception:
        scanner_data = None

    res = sync_files(state, scanner_data=scanner_data, force_session=force_session)
    if res["changed"]:
        print(f"Updated trade journal: {res['commitMessage']} ({res['trades']} trades, {res['sessions']} sessions).")
    else:
        print(f"Trade journal already up to date ({res['trades']} trades, {res['sessions']} sessions).")

    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out and res["commitMessage"]:
        with open(gh_out, "a", encoding="utf-8") as f:
            f.write(f"commit_message={res['commitMessage']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
