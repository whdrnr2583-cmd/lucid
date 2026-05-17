---
name: lucid-experiment-folder
description: Claude Code/API self meta-experiments stay in a separate Lucid workbench. Prevents project pollution + accumulates learning fragments in one place. Defines token-estimate disciplines and proactive proposal rules.
metadata:
  type: feedback
---

When working in a real project (your trading code, your SaaS, your client work, etc.) and you encounter **meta-level curiosity about Claude itself** — new features, unknown tags, slash command behavior, hook experiments, agent comparisons, model differences — **don't experiment in the real project**. Move to `~/<your-workspace>/lucid/` (a sibling workbench) and verify/archive there.

**Why:** Real projects are protected by their own governance — PMF gate, stop-loss, time cap. Meta-experiments are interesting but pollute the project's commit history, archive, and `_workspace/` if mixed in. Three concrete failure modes:
1. Audit inflation — meta-experiments expand the project's memory cap.
2. Cross-check noise — when reviewing real project decisions, you can't tell which entries are project-actual vs experimental.
3. Lost fragments — meta-learnings without a dedicated home just evaporate after a session ends.

**How to apply:**
- **Triggers**: new Claude Code feature release / MCP spec change / unknown tag (e.g., `<fictional>`) / slash command behavior hypothesis / hook experiment / agent comparison / which model is better — anything **Claude-meta**.
- **Don't touch real project code/archive**. Even a single-line test belongs in a separate location.
- **Entry**: `cd ~/<your-workspace>/lucid/`. Create subfolders by topic (e.g., `lucid/mcp-protocol-spec-check/`, `lucid/hook-experiments/`).
- **Output**: short `README.md` + experiment scripts/logs. Valuable findings get **promoted to memory** (reference or feedback type).
- **Real-project influence**: changes that should affect the real project (e.g., new MCP registration pattern) go through Lucid first, then PR-style into the project. Never experiment in the project directly.
- **Exception**: when the **real-project use itself is the learning event** (e.g., dogfooding your own tool's setup flow), do it in the project. Lucid is for project-unrelated meta curiosity only.

## Market evidence archive (added 2026-XX-XX)

Lucid is also a **verified market discovery archive**, not just a meta-experiment lab.

- **Trigger**: while working, you stumble onto (a) clear payment-verification signal for some market, (b) a candidate that passes your project-discovery criteria, (c) third-party payment data / news / customer quote making "people pay for this" undeniable.
- **Archive only, do not execute immediately**. Maintain your "no premature project launch" meta-rule — Lucid archive is future reference, NOT launch approval.
- **Location**: `lucid/market-leads/<short-slug>/README.md`. Include: discovery date, source, criteria cross-check, payment evidence, why this should NOT be folded into your existing tracks.
- **Reject cases**: simple idea / "this would be cool" intuition / ChatGPT-replicable wrapper / legal-medical-financial gray zones / capital-game categories. Don't archive these — keeps Lucid clean.
- User-discovered markets get the same archive treatment.

## Proactive proposal pattern (added 2026-XX-XX)

The rule is **bidirectional**. Not only the user proposes — the agent (Claude) can proactively propose **Lucid experiments** when encountering meta-curiosity during real work (new tools, suspected spec changes, behavior discrepancies, etc.).

- **Token estimate is mandatory** when proposing. Format: `Estimated input ~XK / output ~YK / total ~ZK ($A.AA on Opus 4.7).`
- **Estimation baselines** (rough, calibrate from your own dogfood):
  - Simple curiosity check (1-2 fetches + answer): 5-15K input, 1-3K output, ~10-20K total
  - Single code experiment (1 script + run + analysis): 15-30K input, 3-8K output, ~20-40K total
  - Skill invocation + analysis combined: 25-40K input, 5-10K output, **~30-50K total**
  - Memory audit + matrix generation: 15-25K input, 5-8K output, ~20-30K total
  - Hypothesis verification (multiple attempts + comparison): 30-80K input, 8-20K output, ~40-100K total
  - Large experiment (multi-agent / extended thinking): 100K+
- If estimate is ambiguous, give lower-upper bounds OR offer "step-by-step path vs single hypothesis check?" as a choice.
- If user declines or doesn't engage with the lab proposal, **return to real work immediately**. No lingering.

## Autonomy vs explicit-selection guide (added 2026-XX-XX)

| User utterance pattern | Agent behavior |
|---|---|
| Explicit pre-authorization ("do whatever you want" / "use your judgment" / "autonomous") | Propose candidates + recommend + **start immediately**. Rollback on reject. |
| Ambiguous ("what should we do?" / "/lucid") | Propose + recommend + **wait for explicit selection** |
| Single candidate named ("α 진행" / "do A") | Start immediately (still cross-check `REJECTED.md`) |
| Real-project impact possible | Always require explicit user authorization. Pre-authorization void. |
| Audit inflation cap hit + more documentation attempted | Require explicit user + justified exception (user decision / external audit response / major incident) |
| Time budget concern | Notify user before proceeding |
| Candidate is in `REJECTED.md` | Require new reversal trigger explicitly. User confirmation. |

## Related memory entries

- `feedback_audit_inflation_pmf_gate.md` — per-session archive cap. Lucid separation preserves the real-project cap.
- `feedback_no_portfolio.md` (your own version) — agent-initiated new project launches are nearly always rejected. Lucid is not a "new project," it's a learning fragment workbench. Product-track rules (payment, legal) don't apply.
- `feedback_rule_integrity.md` (your own version) — don't bypass this rule with "this time is different." Want to do Claude-meta work in the real project? Move to Lucid first.
