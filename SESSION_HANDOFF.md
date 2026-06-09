# Session Handoff — Trading Workstation

Context dump so this work can resume in a **local Claude Code session**. Pull this branch,
read this file, and you're caught up.

## Mission & philosophy
- **Account: ~$50, Questrade margin account (Canada).** Goal at this stage is **reps + discipline, not profit.** Survive, journal, repeat. $50 is tuition for real emotional reps.
- Treat margin account like a **cash account**: position ≤ cash, no leverage, no shorting. (See `TRADING_SETUP.md`.)
- **Open gate:** confirm Questrade actually allows a $50 trade (historically ~$1,000 min to activate). VERIFY BEFORE TRADING.

## Tools / stack
- **Data:** Massive/Polygon API (free tier, 15-min delayed — fine for swing). Config in `.mcp.json`.
  Key lives in env var `POLYGON_API_KEY` (NOT committed). Endpoints `api.polygon.io` and `api.massive.com` both work.
- **News/sentiment:** Polygon `/v2/reference/news` (includes per-ticker sentiment) + web search.
- **Catalysts:** Google Calendar reminders already set (NVDA check, FOMC Jun 17, NVDA earnings Aug 26).
- **Journal:** Notion (system of record).

## Market regime (as of Jun 8–9, 2026)
- S&P 500 at record highs (~7,600), **Shiller P/E ~43** (historically extreme). Stretched + jittery.
- **Macro gauntlet:** CPI **Jun 10 8:30am ET** (hot, ~4.2% YoY), PPI Jun 11, FOMC + dot plot Jun 16–17.
- Geopolitics: Iran/Israel strikes → overnight gap risk.
- **Leaderless pullback:** entire mega-cap tech complex (GOOGL/MSFT/NVDA/META/NFLX/PLTR) has
  **negative relative strength vs QQQ.** Defensive tape → trade small or sit out.

## Trade candidates (real data, last session)
- **GOOGL** $363.31 — pullback to rising 50d ($356), bounced off $358. BUT it's a **laggard**
  (weak RS, below 20d). Entry $363–365 on green confirm · Stop $353 · T1 $383 · T2 $408 · R:R 2.0–4.3.
- **MSFT** $411.74 — best-of-breed: above 50d ($409), best RS of the group, R:R 5.56.
  Sitting on 50d/10d-low support. Caveat: nearby target (20d ~$422) is close, so reward is back-loaded.

## Current decision
**ARMED, not firing.** Defensive regime + CPI in <24h + laggards → the disciplined play is
**WAIT for CPI (Jun 10) to clear**, then re-evaluate. Cash is a position.

## Still-open blind spots (do before entering)
- Volume analysis of the pullback (light = healthy, heavy = distribution).
- Volatility regime (VIX) → stop width.
- Options-implied move around CPI → expected gap size.

## Non-negotiable rules
1. No trade unless **R:R ≥ 2**. 2. Define stop+target before entry; confirm live price in broker.
3. Never hold through earnings. 4. Flat/tiny into CPI/PPI/FOMC. 5. No margin/leverage/shorting.

## How to resume locally
```bash
git clone <repo-url> && cd The-one-
git checkout claude/stock-trading-basics-af0149
export POLYGON_API_KEY="your_key"          # never commit this
# add Polygon MCP (see TRADING_SETUP.md), then launch Claude Code in this dir
```
Next action when you resume: **check the CPI print (Jun 10 8:30am ET), pull GOOGL/MSFT reaction
via the API, re-run the leader scan, and decide enter vs. keep waiting.**
