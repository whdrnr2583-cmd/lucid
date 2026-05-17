# Lucid workbench entry

> This slash command lets the agent proactively propose meta-experiments and archive selected ones in `~/<your-workspace>/lucid/<topic-slug>/`.

## Auto-loaded files

```
@~/.claude/projects/<your-sanitized-cwd>/memory/feedback_lucid.md
@~/<your-workspace>/lucid/README.md
@~/<your-workspace>/lucid/REJECTED.md
```

(Paths above are placeholders. Replace `<your-sanitized-cwd>` and `<your-workspace>` with actual values when installing.)

## On invocation (run in this order)

### 1. Workbench state check

```bash
ls -1 ~/<your-workspace>/lucid/ 2>/dev/null
```

Identify in-progress (README in progress) vs completed (final README + conclusion) rounds. If there's an in-progress round, notify the user first ("there's an open round X — continue or start new?").

**Memory health check recommended cadence**: every 5-10 rounds or on user request:

```bash
python3 ~/<your-workspace>/lucid/tools/memory_health_check.py
```

No automatic trigger (Hooks-based automation is in REJECTED.md per the audit-inflation-automation-risk rule). Compare against current round count and notify the user if cadence threshold is hit.

**REJECTED.md cross-check is mandatory** before proposing new candidates. If proposing a previously-rejected idea, explicitly cite a new reversal trigger.

### 2. Context recall

- What was the immediately preceding task in this session? — seed for candidate proposal
- Did anything Claude-meta surprising come up while working? (unknown tag/behavior/new feature/suspected spec change)
- Anything market-evidence-like that surfaced outside the main work?

### 3. Propose 2-4 candidates

Format for each candidate:

```
### α. <Name>

- **Goal**: ...
- **Method**: ...
- **Estimated**: input ~X-YK / output ~A-BK / total ~MK / **$N.NN** (Opus 4.7)
- **Output**: `lucid/<slug>/README.md`
- **Value**: ... (state why this stays out of real projects if applicable)
```

After all candidates, **give one honest recommendation** with reasoning. If something tempting is being intentionally excluded (mentioned but rejected), say so explicitly with the reason — typically: gated meta-rule violation, governance category violation, market-evidence absent, etc.

### 4. Wait for user choice

- "α 진행" / "do α" / "start β" / "propose more" / "skip" — explicit response required
- No response → return to the previous real-work task. No lingering.

### 5. On user selection — execute

```bash
mkdir -p ~/<your-workspace>/lucid/<topic-slug>
cd ~/<your-workspace>/lucid/<topic-slug>
```

Do the work. On completion, write `README.md` covering: goal, method, conclusion, token measurement vs estimate, memory-promotion decision.

Promote valuable findings to memory (reference or feedback type) **only with explicit user authorization**.

## Self-discipline (Claude reading this)

- **Real projects don't get touched**. Lucid outputs must go through PR-style movement, never edited in-project directly.
- **Time budget**: respect your user's weekly cap (default: ~10h). Include time estimate alongside token estimate when relevant.
- **No new-project launches** via Lucid. Candidates are fragments / experiments / market archives, never "launch this product."
- **Token estimate is mandatory**. If unsure, lower-upper bounds both.
- **Don't push** — user declines → immediate return to real work, no re-pitching the rejected candidate in the same round.
- **Cap candidates at 2-4** per round. 5+ overwhelms the user.

## Token estimate quick reference

See `lucid/README.md` for the full calibrated table. Summary:

| Category | Total | $ (Opus 4.7) |
|---|---|---|
| Simple curiosity (1-2 fetches) | ~10-20K | ~$0.20-0.50 |
| Single code experiment | ~20-40K | ~$0.60-1.20 |
| Skill invocation + analysis | ~30-50K | ~$0.85-1.50 |
| Memory audit + matrix | ~20-30K | ~$0.50-0.80 |
| Hypothesis verification (multi-step) | ~40-100K | ~$1.50-3.00 |
| Large experiment (multi-agent) | 120K+ | $3.50+ |

## Trigger keywords (user utterances likely to invoke this)

- "/lucid" or "lucid에서 뭐 해볼까"
- "anything you want to try?" / "what should we do in the lab?"
- "I found a definite market — what now?" → branches into `market-leads/`

## Never do

- Change real-project code/archive without explicit user authorization
- Propose candidates without a token estimate
- Launch new projects (meta-rule violation)
- Re-propose a candidate rejected earlier in the same round
- Propose 5+ candidates in one round
- Continue if actual token use exceeds 50% of estimate without notifying the user
- Skip the project-discovery cross-check when proposing market-evidence archives

## Round completion verification

For each finished round:

- [ ] `lucid/<slug>/README.md` written
- [ ] Token actual vs estimate compared (one line, rule verification)
- [ ] Memory promotion decision stated (Yes / No + reason)
- [ ] Real-project impact noted (if any, archive a PR-style migration candidate)
