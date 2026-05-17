# Lucid Rejected Candidates Archive

> Prevents re-proposal. Every rejected candidate: rejection date + reason + reversal trigger.

## Why this file

- Same candidates resurface across sessions ("let me try Hooks again")
- Without an archive, you re-evaluate from scratch every time → audit inflation
- With this archive, the agent must read it before proposing → cross-check enforced
- Reversal triggers prevent "this rule is final forever" rigidity

## Format

```markdown
### <Candidate name>
- **Rejected**: YYYY-MM-DD
- **Reason**: why this isn't worth pursuing right now
- **Reversal trigger**: what observable signal would justify re-proposing
```

## Example entries

> Replace with your own. These are illustrative.

### Auto-update memory via hooks
- **Rejected**: 2026-XX-XX
- **Reason**: Hooks-based auto-memory creation is friction-low but defeats the audit inflation cap — rules silently accumulate without explicit review. Manual gate is the entire point of this framework.
- **Reversal trigger**: If manual memory creation overhead grows past 50% of session time on 3+ consecutive sessions, reconsider with a strict cap-equivalent in the hook.

### Path-scoped rule loading (per-directory rules)
- **Rejected**: 2026-XX-XX
- **Reason**: Cross-cutting rules (security, governance, no-debt etc.) apply to all tracks. Path-scoped loading would require duplicating them across every directory or risk drift.
- **Reversal trigger**: Specific rule sets that genuinely shouldn't load globally accumulate to 5+ items.

### Vercel-specific tooling integration
- **Rejected**: 2026-XX-XX
- **Reason**: Not used in current stack (Cloudflare).
- **Reversal trigger**: Stack migration to Vercel for any track.

### Generic agent harness framework (e.g., `harness:harness` skill)
- **Rejected**: 2026-XX-XX
- **Reason**: Setting up new domain harnesses risks proliferation of half-implemented projects (anti-pattern: "let me build a framework for X" before X has any users). Explicit user request only.
- **Reversal trigger**: User-specified new domain with concrete delivery target.

## Rules for adding entries

1. Anyone (user or agent) re-proposing a rejected candidate must cite a new reversal trigger or new evidence
2. "Just trying again" is not a valid trigger — be explicit about what changed
3. Old entries (>6 months) should be reviewed annually for stale reversal triggers
4. Do not delete entries; mark them as `[REVERSED: YYYY-MM-DD because X]` if you re-adopt
