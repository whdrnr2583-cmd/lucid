# `<fictional>` tag identity check

> First claudelab round / Trigger: user asked what `<fictional>` means after seeing an angle-bracket placeholder in their docs.

## Question

Is `<fictional>` a standard tag? An official wrapper used in Anthropic / Claude training data?

## Investigation (2 fetches)

1. [Modifying LLM Beliefs with Synthetic Document Finetuning (Anthropic, 2025)](https://alignment.anthropic.com/2025/modifying-beliefs-via-sdf/) — SDF uses **naturally-written documents**. No explicit `<fictional>` tag.
2. [Teaching Claude Why (Anthropic, 2026)](https://alignment.anthropic.com/2026/teaching-claude-why/) — references "fictional stories about AIs behaving admirably" but **no XML-style delimiter mentioned**.

## Conclusion

- **Not a standard HTML/XML tag** — browsers / parsers treat as unknown element (renders inner text only).
- **Not an explicit wrapper in Anthropic's training pipeline** — SDF uses plain documents.
- Where it might appear:
  1. ad-hoc markers in third-party evaluation / jailbreak datasets
  2. user/researcher-side fiction-vs-real demarcation conventions
  3. some system prompts using it as a scenario indicator
- **Angle-bracket placeholders like `<this client>` in user docs are separate** — a markdown/doc convention meaning "user fills in actual value here." LLMs usually interpret correctly but it's not spec-guaranteed.

## Token usage (rule verification)

| Item | Estimated | Actual |
|---|---|---|
| Total | 5-7K / $0.20 | ~6.5K |

First application of the claudelab rule — within estimate, terminated cleanly. Memory promotion not pursued (the check itself is sufficient evidence; doc improvements are a separate workstream).

## Follow-up candidates (deferred)

- Placeholder representation improvement in user docs — lower priority pre-traction
- A/B testing of placeholder vs auto-judgment prompt patterns — only if user-impact becomes clear
