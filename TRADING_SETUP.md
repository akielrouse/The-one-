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

## 2. Market data — Polygon.io MCP (free tier)

The free tier is **15-minute delayed** and rate-limited — **perfect for swing trading**
(we hold for days; we do not need tick data). See `.mcp.json` in this repo.

### Steps
1. Create a free API key at https://polygon.io (Dashboard → API Keys).
2. Install [`uv`](https://docs.astral.sh/uv/) (provides `uvx`).
3. Add the server to Claude Code (easiest — one line):
   ```
   claude mcp add polygon -e POLYGON_API_KEY=YOUR_KEY -- \
     uvx --from git+https://github.com/polygon-io/[email protected] mcp_polygon
   ```
   > Note: Polygon's MCP was rebranded to **Massive** (`massive-com/mcp_massive`).
   > `POLYGON_API_KEY` still works as a deprecated alias. If the pinned version above
   > breaks, switch to `git+https://github.com/massive-com/mcp_massive@latest` and key `MASSIVE_API_KEY`.
4. Or use the committed `.mcp.json` (project scope) and export your key:
   `export POLYGON_API_KEY=YOUR_KEY` before launching Claude Code.
5. **Never commit your API key.** `.mcp.json` uses `${POLYGON_API_KEY}` on purpose.

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
