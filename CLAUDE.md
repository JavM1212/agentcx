# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

This is the **AgentCX** project — a Customer Support Resolution Agent built in 5 phases to prepare Jahir for the CCA-F (Claude Certified Associate – Foundations) exam. Read `docs/CONTEXT.md` before any session to get the full study progress, exam results, and where to continue. The agent covers all 5 exam domains across 5 sequential phases, each in its own subdirectory.

## Setup

```bash
pip install -r requirements.txt
```

Requires an `.env` file with `ANTHROPIC_API_KEY` (never commit it). Use `python-dotenv` to load it.

## Running phases

The project uses a venv at `.venv/` with Python 3.13. A shell alias makes running modules easy.

**One-time setup:**
```bash
source ~/.zshrc   # loads the `run` alias
```

**Run any module:**
```bash
run agentcx.phase1_domain1.agent
run agentcx.phase1_domain1.coordinator
```

The `run` alias expands to `/Users/jahirvalverde/Developer/customer-support-agent/.venv/bin/python -m`.

No test framework is configured yet. Validation is done by running scripts and observing `stop_reason` behavior in real Claude API responses.

## Architecture

```
agentcx/
├── phase1_domain1/   ← Agentic loop, stop_reason, prerequisite gates, PostToolUse hooks, coordinator
├── phase2_domain2/   ← Tool descriptions, structured error responses, MCP config
├── phase3_domain3/   ← CLAUDE.md hierarchy, slash commands, CI/CD with -p flag
├── phase4_domain4/   ← Classifier (few-shot), extractor (JSON schema), validator (retry-with-error-feedback)
└── phase5_domain5/   ← Case facts block, escalation triggers, provenance/claim-source mappings
```

Each phase adds to the same Customer Support Agent. Phases are built sequentially — later phases depend on earlier ones.

## Teaching approach

- Explain concepts with analogies before showing code
- When introducing intentional bugs: show broken code, ask Jahir to identify the bug before running
- After each phase: give a short 5-question quiz on what was built
- Connect every code decision to the specific exam task statement it demonstrates (e.g., TS 1.1, TS 2.2)
- When Jahir gets something wrong: explain WHY before revealing the answer — never just correct silently
- Jahir controls pacing — don't rush to the next step

## Anti-patterns — always flag these explicitly

When you see or write code with these patterns, stop and call them out:

1. Loop termination based on `response.content[0].type == "text"` instead of `stop_reason`
2. `for i in range(N)` as the primary loop termination control
3. Prompt instruction used for business-critical enforcement (use hooks/gates)
4. `isRetryable: true` on validation, business, or permission errors
5. Subagent context assumed inherited (must be explicitly injected)
6. Batch API used in any blocking or SLA-constrained workflow
7. `fork_session` used where an independent session is needed (e.g., self-review)
8. Full tool API responses added to context without trimming
9. Aggregate accuracy reported without stratified field-level breakdown
10. Plain text passed between agents instead of structured claim-source mappings

## Key rules (exam-critical)

```
stop_reason == "end_turn"  → return final answer
stop_reason == "tool_use"  → execute tool, continue loop

PostToolUse hooks fire only for the agent they are registered on.
Register on the subagent that calls the tool — not the coordinator.

"Task" in allowedTools is MANDATORY for subagent spawning.

Batch API hard disqualifiers: SLA < 24h OR step 2 needs step 1's output.

Retry is pointless when information is absent from the source — accept null, escalate.

fork_session inherits base context. Use independent sessions for self-review.
```
