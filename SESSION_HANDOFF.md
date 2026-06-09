# Session Handoff — Trading Workstation

Context dump so this work can resume in a **local Claude Code session**. Pull this branch,
read this file, and you're caught up. **Last updated: 2026-06-09.**

## Mission & philosophy
- **Account: ~$50, Questrade margin account (Canada).** Goal at this stage is **reps + discipline, not profit.** Survive, journal, repeat. $50 is tuition for real emotional reps.
- Treat the margin account like a **cash account**: position ≤ cash, no leverage, no shorting. (See `TRADING_SETUP.md`.)
- **Open gate: CLEARED (2026-06-09).** Questrade API confirms the Margin account is **Active and funded** (~$50 CAD ≈ $35.83 USD); fractional orders available, the ~$1,000 activation minimum is not blocking. ⚠️ Buying power shows ~$166 CAD = **3.3× margin (borrowed) — ignore it; trade only the ~$50 cash.** Live read-only access via `qt.py` (which needed a browser User-Agent to clear Questrade's Cloudflare firewall).
- **Cost reality at $50 (this decides net P&L):** CAD→USD conversion is ~1.5% *each way* (~3% round trip). On a swing targeting +5–8% that's a third of the edge gone to FX. **Convert to USD once and hold USD between trades** (Norbert's Gambit later) so you're not paying FX every round trip. Require **R:R ≥ 2 _after_ the ~3% cost hurdle.**

## Tools / stack
- **Data:** Massive MCP (formerly Polygon), free tier, 15-min delayed — fine for swing. Installed via `uv tool install` (NOT the old broken `uvx --from` form); console cmd `mcp_massive`, key env `MASSIVE_API_KEY`. `.mcp.json` is fixed. Full setup + the gotcha in `TRADING_SETUP.md` §2.
- **News/sentiment:** Massive/Polygon `/v2/reference/news` (per-ticker sentiment) + web search.
- **Catalyst calendar:** **CPI (May) → Jun 10 8:30am ET** · **PPI Jun 11** · **FOMC + dot plot Jun 16–17** · NVDA earnings Aug 26. Google Calendar reminders set.
- **Journal:** Notion (system of record).

## Market regime (snapshot: Jun 8 2026 close — REFRESH at open / via live feed)
- **Not at record highs anymore — it flushed, then bounced.** S&P **7,405** (was ~7,600). Fri Jun 5 = −2.6% S&P / −4% Nasdaq semiconductor washout (~$1T off chips); Mon Jun 8 = chip-led bounce. Two-sided, jittery tape — not a trend.
- **Sentiment cautious, not euphoric:** Fear & Greed **~42 (Fear)**, VIX **18.9** (spiked Friday, now receding). A de-risked, nervous crowd = a coiled spring into the print.
- **The CPI setup (the crux):** consensus **+0.5% MoM / 4.2% YoY headline** ("highest since Apr 2023," energy/Iran-driven) **but core expected to COOL to +0.2% MoM.** Prediction markets ~**66% odds the print comes in ABOVE 4.2%.**
  - **Edge:** a hot *headline* is already feared/priced. **Core is the number that actually moves the tape.** Headline-hot + core-cool (0.2%) = "look-through" → relief/squeeze higher. Core re-accelerating (≥0.3%) = real risk-off, drags FOMC hawkish. **Watch CORE, not the headline the algos spike on first.**

## Trade candidates (re-scored vs live data, Jun 8 close)
- **GOOGL ~$368.53 — DROPPED from the long list.** Trading *below* its 5-, 50- (~$386) AND 200-day MAs; down 7 of the last 10 days off the May 18 ATH. The prior "buy the bounce off the rising 50d" thesis is **invalidated — price sliced through it.** Confirmed laggard. No long (and no shorting per rules).
- **MSFT ~$416.67 — the only valid long; play it at SUPPORT, not on the chase.**
  - Shelf: volume support **$407.78**, MA cluster **$414–423**.
  - **Preferred entry:** on a not-hot CPI, IF it holds $407.78 with a reversal candle → enter **~$410–412**, stop just under the shelf **~$405** (risk ≈ $6), T1 **$435**, T2 **$450** → **R:R ≈ 4 to T1.**
  - **Do NOT chase a $420+ reclaim** — reward-to-$435 collapses to ~1:1 and fails the R:R gate.
  - Next earnings late July (clear of this window). Levels are Jun 8 close — **confirm live before acting (rule #2).**

## Current decision — ARMED, not firing
**Be flat into CPI (rule #4).** The Monday bounce is not a reason to chase right before a binary print with ~66% hot odds. Cash is a position.
- **Post-8:30 on Jun 10 is the decision point** (the event is known once the number's out — entering *after* is not "into" the catalyst). Scenario plan for MSFT:
  1. **Cool / in-line (headline ≤4.2% AND core ≤0.2%):** relief/squeeze likely. Let the open settle (skip the first 1–5 min algo candle), then take the MSFT-at-support long if it sets up.
  2. **Hot headline / cool core (4.2%+ / core 0.2%):** "look-through" — messy, two-sided. No immediate entry; only act if MSFT defends $407.78 and reclaims $414 with strength.
  3. **Hot core (≥0.3%):** genuine risk-off, FOMC-hawkish risk. **No long.** MSFT likely loses $407.78 → next support lower. Stay flat.
- **Calendar trap:** a swing entered Jun 10 is only ~3 trading days from FOMC (Jun 16–17). Either scalp the relief and be **flat by Jun 13**, or **wait for the post-FOMC all-clear (Jun 17+)** for a cleaner multi-week hold. Don't hold into FOMC (rule #4).

## Behavioral traps (pre-committed)
- **Never** trade the first 1–5 min after 8:30 / 9:30 — algo noise, routinely reverses.
- Don't FOMO the "66% hot" narrative into a short — it's partly priced; a not-hot core squeezes *up*. Hold both scenarios until the data prints.
- Don't anchor to a thesis price has already invalidated (see GOOGL). Don't revenge-trade — costs punish churn; one clean rep > five mediocre ones.

## Still-open blind spots (do before entering)
- Volume on the pullback/bounce (light = healthy, heavy = distribution).
- VIX / options-implied move around CPI → expected gap size → stop width.
- Refresh ALL prices/levels at the open via the live Massive feed.

## Non-negotiable rules
1. No trade unless **R:R ≥ 2** (after the ~3% cost). 2. Define stop+target before entry; confirm live price in broker.
3. Never hold through earnings. 4. Flat/tiny into CPI/PPI/FOMC. 5. No margin / leverage / shorting.

## How to resume locally (Windows)
```powershell
# clone + branch already done at C:\dev\The-one- (branch claude/stock-trading-basics-af0149)
# one-time: install uv, then the data server (caches deps — avoids the 30s MCP timeout)
uv tool install "mcp_massive @ git+https://github.com/massive-com/mcp_massive@v0.10.0"
[Environment]::SetEnvironmentVariable('MASSIVE_API_KEY','<your_key>','User')   # never commit
# then, in a NEW terminal:
cd C:\dev\The-one- ; claude     # approve the project "massive" MCP server when prompted
```
**Next action on resume:** refresh MSFT/GOOGL + the indices via the live feed, read the **CPI print (Jun 10 8:30am ET — watch CORE)**, then execute the scenario plan above (enter vs. keep waiting). On CPI morning, `/browse` the live tape/sentiment to watch the reaction.
