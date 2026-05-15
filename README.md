# claudelab

> A self-evolving Claude Code harness with **audit inflation cap**, **REJECTED archive**, and **closed-loop self-audit** — keep your meta-experiments out of your real projects.

## Why this exists

Claude Code's memory system (`MEMORY.md` + topic files) is great for project context. Once you start adding rules ("don't auto-commit", "always run typecheck before push"), tracking decisions ("we tried X, it didn't work"), and experimenting with new tools, three things go wrong:

1. **Audit inflation** — you spend more time documenting decisions than acting on them. Memory files multiply. Cross-references break. You re-propose the same rejected ideas.
2. **Project pollution** — meta-experiments ("let me test if this MCP works") leak into your real project's commit history and `_workspace/`.
3. **Rule drift** — you write a governance rule and bypass it the next day with "this time is different."

`claudelab` is a workbench pattern + tooling that solves these three:

- **Track separation** — your real projects, your meta-experiments, and your market-research drafts each follow different governance.
- **Audit inflation cap** — explicit per-session limit on new memory files. Forces you to stop documenting and start building.
- **REJECTED archive** — every rejected candidate is logged with reason + reversal trigger. No re-proposal without new evidence.
- **Closed-loop self-audit** — a script detects broken cross-refs, orphan files, and stale entries automatically. Self-evolving without drift.

## What's unique vs alternatives

| Feature | Self-evolving Obsidian + hooks | `everything-claude-code` | **claudelab** |
|---|---|---|---|
| Memory layer | ✓ | ✓ | ✓ |
| Auto-evolving | ✓ (hooks) | ✓ | **Manual gate** (intentional) |
| Audit inflation cap | ✗ | ✗ | **✓** |
| REJECTED archive | ✗ | ✗ | **✓** |
| Closed-loop self-audit | partial | partial | **✓** (script) |
| Track-separated governance | partial | ✗ | **✓** |
| Workbench pattern (lab/) | ✗ | ✗ | **✓** |

claudelab intentionally avoids automation (hooks) to keep audit inflation in check. **Trade-off explicit, not accidental**.

## Quick start (5 minutes)

```bash
# 1. clone
git clone https://github.com/<your-github>/claudelab.git ~/claudelab
cd ~/claudelab

# 2. find your Claude Code memory dir
# Claude Code stores memory at ~/.claude/projects/<sanitized-cwd>/memory/
# `sanitized-cwd` is your working directory with slashes replaced by dashes.
ls ~/.claude/projects/

# 3. copy the rule template into your memory dir
export CLAUDE_MEMORY_DIR=~/.claude/projects/<your-sanitized-cwd>/memory
cp templates/MEMORY_RULE.md $CLAUDE_MEMORY_DIR/feedback_claudelab.md

# 4. set up your workbench
mkdir -p ~/claudelab/{tools,case-studies}
cp tools/memory_health_check.py ~/claudelab/tools/
cp templates/REJECTED.md ~/claudelab/REJECTED.md

# 5. set up the slash command (edit paths inside first)
cp templates/slash_command.md ~/.claude/commands/claudelab.md
$EDITOR ~/.claude/commands/claudelab.md  # replace path placeholders

# 6. run first health check
CLAUDE_MEMORY_DIR=$CLAUDE_MEMORY_DIR python3 ~/claudelab/tools/memory_health_check.py
```

Then in Claude Code:

```
/claudelab
```

The agent reads your rules, lists current lab rounds, and proposes 2-4 candidates (with token estimates) for your next meta-experiment.

## Core concepts

### 5 layers

1. **Memory** (`MEMORY.md` + `feedback_*.md` / `project_*.md` / `reference_*.md`) — your rules and project state
2. **Slash command** (`/claudelab`) — entry point, auto-loads layers 1+3+4
3. **Lab folder** (`~/claudelab/<round-slug>/README.md`) — per-round experiment archive
4. **REJECTED.md** — rejected candidates with reason + reversal trigger
5. **health_check.py** — broken cross-ref / orphan / duplicate / LEGACY auto-detect

### Audit inflation cap

Per-session limit on new memory files (suggested: 3-5). When hit, only **explicit justified exceptions** (user decision / external audit / major incident) allow more. Prevents documentation overhead drowning your actual work.

### Token estimate discipline

Every lab round candidate must include token estimate (input/output/$). Real-world dogfood data calibrates the model over time. Forces you to weigh meta-experiment cost vs value before starting.

### Track-separated governance

Three default tracks, each with different rules:

- `your-projects/` — strict (no auto-commit, PMF gate, time cap)
- `~/claudelab/` — workbench (audit cap, REJECTED archive, lab-only churn)
- `~/claudelab/market-leads/` — market evidence archive (no immediate execution, criterion cross-check)

You define your own tracks in `feedback_claudelab.md`.

## Case studies

Two example rounds from real dogfood (see `case-studies/`):

- **01 fictional-tag-meaning** — `<fictional>` tag identity check via Anthropic alignment docs. ~$0.20.
- **02 anthropic-alignment-multi-agent** — read AI Organizations paper, applied findings to existing multi-agent setup. ~$0.50.

Six additional rounds (not published as case studies — too specific to the author's stack) demonstrated:

- Memory autoload verification (testing that new rules actually trigger in next session)
- Skills/Agents inventory (comparing Claude Code skills to find unused-but-valuable tools)
- `fewer-permission-prompts` skill application (3 narrow exact-form entries added + 22 wildcard entries cleaned up as a side effect)
- Memory health audit + token estimate model calibration (broken cross-refs auto-detected and fixed)
- Slash command self-evolution (adding auto-load paths so each round's discoveries propagate to the next session)

Total: 8 rounds across one session, ~$3.80 USD, zero impact on real project commits.

## Why no automation (hooks)?

`PostToolUse` hooks can auto-update memory files. We intentionally avoid this:

- Auto-memory creation = audit inflation automation
- Rules drift faster than humans notice
- "Sometimes" exceptions slip in without justification

claudelab keeps memory creation **manually gated** with explicit rules for bypass. See `templates/REJECTED.md` for the formal rejection of hooks-based automation.

## Repo structure

```
claudelab/
├── README.md                    ← you are here
├── LICENSE                      ← MIT
├── templates/
│   ├── MEMORY_RULE.md           ← copy into your Claude Code memory dir
│   ├── REJECTED.md              ← copy into your workbench
│   └── slash_command.md         ← copy into ~/.claude/commands/
├── tools/
│   └── memory_health_check.py   ← run periodically
└── case-studies/
    ├── 01-fictional-tag-meaning.md
    └── 02-anthropic-alignment-multi-agent.md
```

## Status

**Alpha — dormant after publish unless traction signals.** This is an experiment in transferable framework patterns. We don't promise support. PRs welcome but may sit.

If you find it useful, star the repo. If something is unclear or missing, open an issue.

## License

MIT. Use, fork, adapt to your own tracks.
