# Trading Workstation Setup

A lean, zero-to-low-cost setup for disciplined **swing trading** (holding days to weeks),
built around a small starter account. Goal at this stage: **run the process and get
reps, not get rich.** Survive, journal, repeat.

---

## 1. Broker — Questrade (Canada)

- **Fractional shares:** ✅ Yes. Commission-free, from **$1**. Covers all S&P 500 +
  Nasdaq 100 names (NVDA, GOOGL, AMD, MSFT, etc.). This is what makes a small account viable.
- **Commissions:** $0 on stock buys/sells (full or fractional).
- **Watch-outs:**
  - **USD/CAD conversion.** Buying US stocks with CAD incurs an FX cost (~1.5%). For tiny
    sizes it's pennies, but it's real. (Advanced: "Norbert's Gambit" avoids it — ignore for now.)
  - **Account funding minimum.** Questrade has historically required ~$1,000 CAD to *start
    trading*. **Verify your account is actually fundable/tradeable at $50** before planning trades.
  - Real-time execution; fractional dividends paid automatically.

### Margin account rules (READ THIS)

A margin account is fine to use — but **treat it exactly like a cash account.** The margin
(leverage) feature is the #2 account-killer for beginners, right behind options. Perks worth
keeping: instant settlement (reuse sale proceeds immediately) and fractional shares.

1. **Position size ≤ your actual cash balance.** With $50, the most stock you ever hold is $50.
2. **Ignore "buying power."** Questrade may show a number larger than your deposit — that extra
   is *borrowed money*. Watch your **cash balance**, not buying power.
3. **Never short sell.** Margin accounts allow betting against stocks; shorting has unlimited
   loss potential. Long-only while learning.
4. **Never borrow / never use leverage.** It amplifies losses as much as gains, can trigger a
   margin call (forced sale at the worst moment), and charges interest.
5. Good news: the US **Pattern Day Trader** rule ($25k minimum) does **not** apply to Canadian
   Questrade accounts.

## 2. Market data — Massive MCP (free tier)

The free tier is **15-minute delayed** and rate-limited — **perfect for swing trading**
(we hold for days; we do not need tick data). See `.mcp.json` in this repo.

> **Heads-up (verified 2026-06-09):** Polygon's MCP was rebranded to **Massive**
> (`massive-com/mcp_massive`, current `v0.10.0`); console cmd `mcp_massive`, key env
> `MASSIVE_API_KEY` (`POLYGON_API_KEY` still works as a deprecated alias). The OLD
> `uvx --from git+...polygon-io/[email protected] mcp_polygon` form is **broken** — the bare
> `git+...` URL no longer parses under modern `uv`, and `uvx --from` re-downloads deps on
> every cold start, which can exceed Claude's 30-second MCP connection timeout. Use
> `uv tool install` (caches once) instead.

### Steps
1. Get a free API key (Massive/Polygon dashboard → API Keys). An existing Polygon key works
   as the `MASSIVE_API_KEY` *value*.
2. Install [`uv`](https://docs.astral.sh/uv/) (provides `uvx` + `uv tool`).
3. Install the server once — caches deps and puts `mcp_massive` on your PATH:
   ```
   uv tool install "mcp_massive @ git+https://github.com/massive-com/mcp_massive@v0.10.0"
   ```
4. Set your key (persistent, never committed). Windows PowerShell:
   ```
   [Environment]::SetEnvironmentVariable('MASSIVE_API_KEY','YOUR_KEY','User')
   ```
   (bash: `export MASSIVE_API_KEY=YOUR_KEY` before launching Claude Code)
5. Launch Claude Code **from this repo dir in a new shell**. The committed `.mcp.json`
   (project scope) runs `command: mcp_massive` with `${MASSIVE_API_KEY}` and loads on launch
   — approve the project server when prompted. (MCP servers load only on a fresh start.)
6. **Never commit your API key.** `.mcp.json` uses `${MASSIVE_API_KEY}` on purpose.

## 3. Journal — Notion (your system of record)

Every trade and every *watch* gets logged: thesis, entry, stop, target, R:R, outcome, lesson.
The journal is the actual product at this stage — the skill compounds, the $50 doesn't.

---

## The non-negotiable rules

1. **No trade unless Reward:Risk ≥ 2.** The math gates the trade, not the story.
2. **Always define stop + target BEFORE entering.** Confirm the live price in Questrade.
3. **Never hold a swing trade through earnings** unless deliberately betting on it.
4. **Be flat or tiny into major catalysts** (FOMC, CPI). Gaps blow through stops.
5. **One clean rep at a time.** Patience beats speed (see below).

## On "being as fast as institutions"

You can't, and you don't need to. Free data is delayed; institutions have microsecond
colocated feeds. But **speed only matters to high-frequency algos fighting over
milliseconds.** A swing trader holding for days competes on a totally different axis:
**patience, discipline, and picking spots where size/speed give big players no edge.**
Don't race Ferraris on their track — win on yours.
