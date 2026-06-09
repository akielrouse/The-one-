r"""
qt.py - Questrade READ-ONLY connector for the trading workstation.

READ-ONLY BY DESIGN. This script can ONLY read your account (balances, positions,
executions) and market data (quotes). It contains NO code to place, modify, or cancel
orders, transfer funds, or change anything in your account. You place every trade
yourself in Questrade. It is ~150 lines of Python stdlib with zero dependencies - read it.

Auth: Questrade OAuth2 manual refresh token.
  - You generate a refresh token in the Questrade App Hub (see SETUP) and save it in a
    token file OUTSIDE this repo:  ~/.questrade/token.json   (Windows: C:\Users\<you>\.questrade\token.json)
  - This script NEVER prints your token, and the token never goes near any chat/transcript.
  - Refresh tokens are SINGLE-USE and rotate on every refresh; this script persists the new
    one automatically. If it ever desyncs (HTTP 400), generate a fresh token from the portal.

SETUP (do this once, yourself - keep the token off any chat):
  1. App Hub -> API centre -> Activate API -> "Generate new token for manual authorization"
     https://apphub.questrade.com/UI/UserApps.aspx   (the token expires in 7 days if unused)
  2. Create the token file with this exact content (paste your refresh token in place):
         {"refresh_token": "PASTE_YOUR_REFRESH_TOKEN_HERE"}
     Path:  ~/.questrade/token.json   (Windows: C:\Users\<you>\.questrade\token.json)
  3. Run:  uv run --no-project python qt.py status

USAGE:
  python qt.py status                 # accounts + balances + the "$50 open gate" check
  python qt.py accounts               # list accounts
  python qt.py balances               # per-account balances
  python qt.py positions              # open positions
  python qt.py fills [N]              # executions in last N days (default 7) - for journaling
  python qt.py quotes MSFT GOOGL ...  # delayed quotes (may need the market-data agreement accepted)
  python qt.py ticket MSFT 410 405 435 [50]  # instant sized, rule-checked trade ticket (read-only)
"""

import json, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

TOKEN_PATH = Path.home() / ".questrade" / "token.json"
LOGIN_URL = "https://login.questrade.com/oauth2/token"
ACCESS_MARGIN = 60  # refresh if the cached access token expires within this many seconds
_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")  # Questrade is behind Cloudflare;
# the default urllib User-Agent gets a 403 / Cloudflare error 1010 (bot signature ban).


def _fail(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def _first_run_help():
    return (
        f"Need your Questrade refresh token in {TOKEN_PATH}\n"
        "(the file is missing, or still holds the PASTE_... placeholder)\n\n"
        "One-time setup (do this yourself - keep the token OFF any chat):\n"
        "  1. Questrade App Hub -> API centre -> Activate API ->\n"
        "     'Generate new token for manual authorization'\n"
        "     https://apphub.questrade.com/UI/UserApps.aspx  (expires in 7 days if unused)\n"
        f"  2. Create {TOKEN_PATH} containing exactly:\n"
        '       {"refresh_token": "PASTE_YOUR_REFRESH_TOKEN_HERE"}\n'
        "  3. Re-run this command.\n"
    )


def load_tokens():
    if not TOKEN_PATH.exists():
        _fail(_first_run_help())
    try:
        data = json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        _fail(f"Could not parse {TOKEN_PATH}: {e}")
    rt = data.get("refresh_token") or ""
    if not rt or rt.startswith("PASTE_"):   # missing or still the placeholder
        _fail(_first_run_help())
    return data


def save_tokens(data):
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = TOKEN_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(data), encoding="utf-8")
    tmp.replace(TOKEN_PATH)  # atomic replace so a rotated token is never half-written


def _http_get(url, headers=None):
    h = {"User-Agent": _UA}      # browser UA so Cloudflare doesn't 1010 us
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"HTTP {e.code} for {url.split('?')[0]}: {body}") from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from None


def refresh(tokens):
    """Redeem the single-use refresh token for an access token + api_server. Rotates the token."""
    q = urllib.parse.urlencode({"grant_type": "refresh_token",
                                "refresh_token": tokens["refresh_token"]})
    try:
        resp = _http_get(f"{LOGIN_URL}?{q}")
    except RuntimeError as e:
        if "HTTP 400" in str(e):
            _fail("Questrade rejected the refresh token (HTTP 400) - it was likely already used "
                  "or has expired. Generate a NEW token in the App Hub and replace the "
                  f'"refresh_token" value in {TOKEN_PATH}.')
        raise
    api = resp["api_server"].rstrip("/")
    if not api.endswith("/v1"):
        api += "/v1"
    new = {
        "refresh_token": resp["refresh_token"],   # NEW single-use token - must be persisted
        "access_token": resp["access_token"],
        "api_server": api,
        "access_expires_at": int(time.time()) + int(resp.get("expires_in", 1800)),
    }
    save_tokens(new)
    return new


def get_session():
    tokens = load_tokens()
    if (tokens.get("access_token") and tokens.get("api_server")
            and tokens.get("access_expires_at", 0) - ACCESS_MARGIN > int(time.time())):
        return tokens                 # cached access token still valid - no refresh, no rotation
    return refresh(tokens)


def api_get(path):
    s = get_session()
    url = f"{s['api_server']}/{path.lstrip('/')}"
    return _http_get(url, headers={"Authorization": f"Bearer {s['access_token']}"})


# ---- read-only commands (no order/transfer calls exist anywhere in this file) ----

def cmd_accounts():
    accts = api_get("accounts").get("accounts", [])
    for a in accts:
        print(f"  {str(a.get('type')):14} #{a.get('number')}  status={a.get('status')}  "
              f"primary={a.get('isPrimary')}")
    return accts


def cmd_balances():
    for a in api_get("accounts").get("accounts", []):
        bal = api_get(f"accounts/{a['number']}/balances")
        print(f"\nAccount #{a['number']} ({a.get('type')}):")
        for c in bal.get("combinedBalances", []):
            print(f"  [{c.get('currency')}] cash={c.get('cash')}  "
                  f"marketValue={c.get('marketValue')}  totalEquity={c.get('totalEquity')}  "
                  f"buyingPower={c.get('buyingPower')}")


def cmd_positions():
    for a in api_get("accounts").get("accounts", []):
        pos = api_get(f"accounts/{a['number']}/positions").get("positions", [])
        print(f"\nAccount #{a['number']}: {len(pos)} position(s)")
        for p in pos:
            print(f"  {str(p.get('symbol')):8} qty={p.get('openQuantity')}  "
                  f"avg={p.get('averageEntryPrice')}  mktVal={p.get('currentMarketValue')}  "
                  f"openPnl={p.get('openPnl')}")


def cmd_fills(days=7):
    now = time.time()
    end = time.strftime("%Y-%m-%dT00:00:00-00:00", time.gmtime(now + 86400))
    start = time.strftime("%Y-%m-%dT00:00:00-00:00", time.gmtime(now - days * 86400))
    for a in api_get("accounts").get("accounts", []):
        q = urllib.parse.urlencode({"startTime": start, "endTime": end})
        ex = api_get(f"accounts/{a['number']}/executions?{q}").get("executions", [])
        print(f"\nAccount #{a['number']}: {len(ex)} execution(s) in last {days}d")
        for e in ex:
            print(f"  {e.get('timestamp')}  {e.get('side')} {e.get('quantity')} "
                  f"{e.get('symbol')} @ {e.get('price')}  comm={e.get('commission')}")


def cmd_quotes(symbols):
    if not symbols:
        _fail("Usage: python qt.py quotes MSFT GOOGL ...")
    ids = []
    for sym in symbols:
        q = urllib.parse.urlencode({"prefix": sym})
        res = api_get(f"symbols/search?{q}").get("symbols", [])
        match = next((s for s in res if s.get("symbol", "").upper() == sym.upper()), None)
        if match:
            ids.append((sym, match["symbolId"]))
        else:
            print(f"  {sym}: not found")
    if not ids:
        return
    q = urllib.parse.urlencode({"ids": ",".join(str(i) for _, i in ids)})
    quotes = {qd["symbolId"]: qd for qd in api_get(f"markets/quotes?{q}").get("quotes", [])}
    for sym, sid in ids:
        qd = quotes.get(sid, {})
        print(f"  {sym:8} last={qd.get('lastTradePrice')}  bid={qd.get('bidPrice')}  "
              f"ask={qd.get('askPrice')}  vol={qd.get('volume')}  delay={qd.get('delay')}")


def cmd_status():
    accts = cmd_accounts()
    cmd_balances()
    print("\n- $50 open-gate check -")
    active = [a for a in accts if a.get("status") == "Active"]
    if active:
        print(f"  {len(active)} Active account(s). If the cash/buyingPower above reflects your "
              "real balance, you are funded to place a (fractional) order. The historical "
              "~$1,000 activation minimum is the one thing to confirm in the Questrade UI.")
    else:
        print("  No Active account found - likely not yet fundable/tradeable.")


def _num(x, name):
    try:
        return float(x)
    except (TypeError, ValueError):
        _fail(f"{name} must be a number, got: {x!r}")


def cmd_ticket(argv):
    """Instant, rule-checked trade ticket. READ-ONLY: it prints the order; you place it."""
    if len(argv) < 4:
        _fail("Usage: python qt.py ticket SYMBOL ENTRY STOP TARGET [cash]\n"
              "  e.g.  python qt.py ticket MSFT 410 405 435 50")
    sym = argv[0].upper()
    entry, stop, target = _num(argv[1], "ENTRY"), _num(argv[2], "STOP"), _num(argv[3], "TARGET")
    cash = _num(argv[4], "CASH") if len(argv) > 4 else 50.0

    shares = cash / entry if entry > 0 else 0.0
    risk = shares * (entry - stop)
    reward = shares * (target - entry)
    rr = (target - entry) / (entry - stop) if entry > stop else float("nan")
    f = 0.015  # CAD<->USD conversion, each way - only bites if you DON'T hold USD between trades
    rr_rt = ((reward - cash * f - shares * target * f)
             / (risk + cash * f + shares * stop * f)) if (risk + cash * f) > 0 else float("nan")

    print("\n=== TRADE TICKET  (read-only - YOU place it in Questrade) ===")
    print(f"  {sym}  LONG    cash ${cash:.2f}")
    print(f"  entry {entry:.2f}   stop {stop:.2f} ({(stop - entry) / entry * 100:+.1f}%)   "
          f"target {target:.2f} ({(target - entry) / entry * 100:+.1f}%)")
    print(f"  size  {shares:.4f} sh (${shares * entry:.2f})    risk ${risk:.2f}    reward ${reward:.2f}")
    print(f"  R:R {rr:.2f}   (assumes USD held between trades; ~0 per-trade FX)")
    print(f"  caution: converting CAD each trade (~3% round-trip) would cut R:R to {rr_rt:.2f} -> hold USD")

    print("  rule check:")
    ok = True
    for cond, label in (
        (entry > stop and target > entry, "stop < entry < target (long)"),
        (rr >= 2, f"R:R >= 2 ({rr:.2f})"),
        (shares * entry <= cash + 1e-9, "position <= cash"),
    ):
        ok = ok and bool(cond)
        print(f"    [{'PASS' if cond else 'FAIL'}] {label}")
    print(f"    [CONFIRM] not into earnings; flat into CPI/PPI/FOMC; live price at trigger (qt.py quotes {sym})")
    print(f"  VERDICT: {'GO - place it after the CONFIRM line' if ok else 'NO-GO - a hard rule failed above'}")
    print(f"  ORDER:  BUY {shares:.4f} {sym} @ limit {entry:.2f}    then a STOP sell @ {stop:.2f}\n")


def main():
    args = sys.argv[1:]
    cmd = args[0] if args else "status"
    try:
        if cmd == "status":
            cmd_status()
        elif cmd == "accounts":
            cmd_accounts()
        elif cmd == "balances":
            cmd_balances()
        elif cmd == "positions":
            cmd_positions()
        elif cmd == "fills":
            cmd_fills(int(args[1]) if len(args) > 1 else 7)
        elif cmd == "quotes":
            cmd_quotes(args[1:])
        elif cmd == "ticket":
            cmd_ticket(args[1:])
        elif cmd in ("-h", "--help", "help"):
            print(__doc__)
        else:
            _fail(f"Unknown command: {cmd}\n{__doc__}")
    except RuntimeError as e:
        _fail(str(e))


if __name__ == "__main__":
    main()
