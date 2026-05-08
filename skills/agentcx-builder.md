---
name: agentcx-builder
description: Guide a CCA-F student through building the AgentCX project from scratch, phase by phase. Use this skill when the user wants to build the AgentCX customer support agent, practice CCA-F exam domains through code, or says things like "start the project", "build AgentCX", "let's code phase 1", or "guide me through the implementation". The skill teaches by asking conceptual questions before writing code, introducing intentional bugs for the student to find, and validating real Claude API responses at each step.
---

# AgentCX Builder

Guide a CCA-F student through building the AgentCX Customer Support Resolution Agent from scratch, one phase at a time. Each phase maps to a CCA-F exam domain. The student learns by doing — not by watching.

## Before Starting

1. **Read all reference files** in `docs/`:
   - `docs/CONTEXT.md` — student profile, study progress, exam results, weak areas
   - `docs/exam-guide-task-statements.md` — all 24 task statements, knowledge areas, skills

2. **Check what exists** — run `ls agentcx/` and read any existing phase files to determine where the student left off. Never rebuild what already works.

3. **Greet with context** — tell the student:
   - Which phase they're starting or continuing
   - Which exam task statements that phase covers
   - What they'll have built by the end

## Teaching Rules (Non-Negotiable)

- **Analogy before code** — every new concept gets a real-world analogy first
- **Question before implementation** — ask the student a conceptual question before writing each component. Wait for their answer. Evaluate it before proceeding.
- **One intentional bug per step** — introduce exactly one bug per code file, marked with a comment. Ask the student to find it before running. Never reveal it — wait for them to identify it.
- **Evaluate answers honestly** — if the student's answer is wrong, explain WHY before correcting. If partially right, acknowledge what's correct then fill the gap.
- **Student controls pacing** — never advance to the next step without the student signaling readiness
- **Connect to exam** — after each step, explicitly state which task statement(s) it demonstrates (e.g., "This is TS 1.1 — agentic loop termination")
- **Always English** — all communication in English regardless of what language the student uses

## Anti-Patterns to Flag Immediately

If you write or the student writes any of these, stop and call it out explicitly before continuing:

1. `for i in range(N)` as primary loop termination → TS 1.1
2. `response.content[0].type == "text"` as termination condition → TS 1.1
3. Prompt instruction for business-critical enforcement → TS 1.4
4. `isRetryable: true` on validation, business, or permission errors → TS 2.2
5. Subagent context assumed inherited (not explicitly injected) → TS 1.2
6. Batch API in blocking or SLA-constrained workflow → TS 4.5
7. `fork_session` used where independent session needed → TS 1.7
8. Full tool API response added to context without trimming → TS 5.1
9. Aggregate accuracy without stratified field-level breakdown → TS 5.5
10. Plain text between agents instead of structured claim-source mappings → TS 5.6

## Project Structure

```
agentcx/
├── phase1_domain1/   ← D1: Agentic Architecture & Orchestration (27%)
├── phase2_domain2/   ← D2: Tool Design & MCP Integration (18%)
├── phase3_domain3/   ← D3: Claude Code Configuration & Workflows (20%)
├── phase4_domain4/   ← D4: Prompt Engineering & Structured Output (20%)
└── phase5_domain5/   ← D5: Context Management & Reliability (15%)
```

## Phase 1 — Agentic Architecture (TS 1.1, 1.2, 1.3, 1.4, 1.5)

### Step 1 — Basic agentic loop (`agent.py`, `tools.py`)

**Concept to explain:** The agentic loop — Claude as a contractor who either says "done" or "I need a tool". `stop_reason` is the only reliable termination signal.

**Question to ask:** "Before I write the loop — what should the termination condition be, in one line of Python pseudocode?"

**Files to create:**
- `tools.py` — simulated customer support tools: `get_customer`, `get_order`, `process_refund` with Anthropic tool definitions
- `agent.py` — agentic loop with `while True` + `stop_reason`

**Intentional bugs to introduce in `agent.py`:**
- Bug 1: `for _ in range(3):` instead of `while True:` (anti-pattern #2)
- Bug 2: `if response.content[0].type == "text": return` instead of `if response.stop_reason == "end_turn"` (anti-pattern #1)

**Validation:** Run `python -m agentcx.phase1_domain1.agent`. Student should see tool calls printed and a final refund confirmation. Confirm `stop_reason` drove termination.

**Exam connection:** TS 1.1 — implement agentic loops using stop_reason as the termination signal.

---

### Step 2 — Prerequisite gate (`hooks.py`)

**Concept to explain:** Prompt instructions are probabilistic. Programmatic gates are deterministic. A gate blocks a tool call at the boundary — no bypassing possible.

**Question to ask:** "Should the gate check happen inside `process_refund()` in `tools.py`, or in a separate interception layer? Why does it matter?"

**Files to create/modify:**
- `hooks.py` — `AgentState` class, `pre_tool_gate`, `post_tool_update`
- `agent.py` — wire gate into the tool execution loop

**Intentional bug:** Pass `AgentState()` (new instance) instead of `state` to `post_tool_update` — gate never opens because state is always reset.

**Validation:** Run with a message that skips `get_customer`. Should see `[gate] process_refund BLOCKED`. Then run normal flow — gate opens after `get_customer` succeeds.

**Exam connection:** TS 1.4 — enforcement via programmatic gates, not prompt instructions.

---

### Step 3 — PostToolUse hook

**Concept to explain:** A hook fires unconditionally after every tool call. The loop doesn't decide when — it always fires. Logic inside the hook decides what to do per tool.

**Question to ask:** "Currently `post_tool_update` is called explicitly inside the else block. What's wrong with that compared to a real hook?"

**Modification:** Move `on_post_tool_use` call outside the `if gate_error / else` block so it fires after every tool call regardless of gate outcome. Rename to make hook intent explicit.

**Intentional bug:** Call `on_post_tool_use` inside the `else` block only — fires only on success, never on gate block.

**Validation:** Run agent. Should see `[hook] verified_customer_id set → C001` printed after `get_customer` succeeds.

**Exam connection:** TS 1.5 — PostToolUse hooks, registration rule (hooks fire only for the agent they're registered on).

---

### Step 4 — Multi-agent coordinator (`coordinator.py`)

**Concept to explain:** Hub-and-spoke — coordinator routes, subagents execute. Subagents start with empty context; coordinator must explicitly inject what they need.

**Question to ask:** "If subagents don't inherit context, how does `resolution_agent` know which customer and order to refund?"

**Files to create:**
- `coordinator.py` — `run_subagent()` + `run_coordinator()` with two subagents:
  - `lookup_agent`: scoped to `get_customer` + `get_order`
  - `resolution_agent`: scoped to `process_refund`

**Intentional bug:** Pass `user_message` instead of `f"Case details:\n{lookup_result}\n\nOriginal request: {user_message}"` to `resolution_agent` — subagent has no context to work with.

**Validation:** Run `python -m agentcx.phase1_domain1.coordinator`. Should see both subagents run sequentially, with coordinator injecting lookup results before resolution.

**Exam connection:** TS 1.2 — hub-and-spoke, context isolation, explicit injection. TS 1.3 — `allowedTools` scoping per subagent.

---

## Phase 2 — Tool Design & MCP Integration (TS 2.1, 2.2, 2.3, 2.4)

### Step 1 — Tool descriptions (`tool_definitions.py`)

**Concept:** Tool descriptions are the primary signal Claude uses to select tools. Vague descriptions cause wrong tool selection. Each tool should state: what it does, when to use it, what it returns.

**Question:** "What's the minimum a tool description needs to contain for Claude to reliably pick the right tool?"

**Files:** `tool_definitions.py` — rewrite tool definitions with explicit descriptions, differentiated purposes, and clear parameter docs.

**Exam connection:** TS 2.1 — tool descriptions, differentiation, splitting generic tools.

---

### Step 2 — Structured error responses (`error_responses.py`)

**Concept:** Errors fall into 4 categories with different retry behavior. The `isRetryable` flag tells the agent whether to retry or escalate.

**Question:** "A customer tries to refund an order they don't own. Which error category is that, and should it be retryable?"

**Error categories:**
```
transient   → isRetryable: true  (timeout, service unavailable)
validation  → isRetryable: false (bad input format)
business    → isRetryable: false (policy violation → escalate)
permission  → isRetryable: false (unauthorized)
```

**Files:** `error_responses.py` — error factory functions for all 4 categories.

**Exam connection:** TS 2.2 — isError flag pattern, 4 error categories, local recovery.

---

### Step 3 — MCP config (`mcp_config.py`)

**Concept:** `.mcp.json` scopes which tools are available per project. Env vars in MCP config are expanded from the local shell — never hardcode secrets in the config file.

**Question:** "If an MCP tool fails with 'API key not found', where is the fix — in `.mcp.json` or in the shell environment?"

**Files:** `mcp_config.py` — `.mcp.json` equivalent with env var expansion pattern.

**Exam connection:** TS 2.4 — `.mcp.json` scoping, env var expansion (fix is always local shell, never architectural changes to the config).

---

## Phase 3 — Claude Code Configuration (TS 3.1–3.6)

### Step 1 — CLAUDE.md hierarchy

**Concept:** Three levels load in order: user (`~/.claude/CLAUDE.md`) → project (root) → directory (subdirectory). Each level can override or extend the previous.

**Files:** `phase3_domain3/CLAUDE.md` — directory-level instructions for the phase3 module.

**Exam connection:** TS 3.1 — CLAUDE.md hierarchy, @import, `.claude/rules/`.

---

### Step 2 — Slash command / skill

**Concept:** Skills are markdown files invoked with `/skill-name`. Frontmatter controls context forking, allowed tools, and argument hints.

**Files:** `skills/` — a slash command for the AgentCX workflow.

**Exam connection:** TS 3.2 — slash commands, SKILL.md frontmatter (`context:fork`, `allowed-tools`, `argument-hint`).

---

### Step 3 — CI/CD pipeline (`ci_pipeline.py`)

**Concept:** Claude Code runs non-interactively in CI with `-p` flag. `--output-format json` makes results parseable. Each CI run is an isolated session.

**Files:** `ci_pipeline.py` — demonstrates `-p` flag usage and session isolation.

**Exam connection:** TS 3.6 — CI/CD with `-p` flag, `--output-format json`, session isolation.

---

## Phase 4 — Prompt Engineering & Structured Output (TS 4.1–4.6)

### Step 1 — Classifier (`classifier.py`)

**Concept:** Explicit criteria + 2–3 few-shot examples reduce false positives and inconsistency. Vague instructions produce inconsistent classifications.

**Question:** "What's the difference between telling Claude 'classify urgent requests' vs providing explicit criteria with examples?"

**Files:** `classifier.py` — ticket classifier with explicit criteria + few-shot examples.

**Exam connection:** TS 4.1 + TS 4.2.

---

### Step 2 — Extractor (`extractor.py`)

**Concept:** JSON schema + `tool_use` forces structured output. `required` / `nullable` / `enum` patterns control what Claude can and cannot return.

**Files:** `extractor.py` — structured data extractor using tool_use with JSON schema.

**Exam connection:** TS 4.3 — tool_use with JSON schemas, required/nullable/enum patterns.

---

### Step 3 — Validator (`validator.py`)

**Concept:** Retry-with-error-feedback works for format/structural errors. It does NOT work when information is absent from the source document — retrying will never produce data that isn't there.

**Question:** "A customer's address is missing from the order record. Should we retry the extraction with error feedback?"

**Files:** `validator.py` — retry loop with error feedback, max retries, null acceptance.

**Exam connection:** TS 4.4 — retry-with-error-feedback, when retries are ineffective.

---

## Phase 5 — Context Management & Reliability (TS 5.1–5.6)

### Step 1 — Context manager (`context_manager.py`)

**Concept:** Case facts block — extract key facts BEFORE any summarization and place them at the START of every prompt. Tool results trimmed to relevant fields only.

**Files:** `context_manager.py` — case facts extraction + tool result trimming.

**Exam connection:** TS 5.1 — case facts block, lost-in-the-middle, tool result trimming.

---

### Step 2 — Escalation (`escalation.py`)

**Concept:** Reliable escalation triggers are explicit and objective. Unreliable triggers are subjective and gameable.

```
Reliable:   explicit human request, policy gap, cannot progress
Unreliable: sentiment/frustration, self-reported complexity, confidence claims
```

**Files:** `escalation.py` — escalation classifier with reliable vs unreliable trigger detection.

**Exam connection:** TS 5.2 — escalation triggers.

---

### Step 3 — Synthesis (`synthesis.py`)

**Concept:** Every claim returned to the user should have a source mapping. Conflicting data sources need temporal metadata to resolve. Provenance prevents hallucination from going undetected.

**Files:** `synthesis.py` — claim-source mappings, provenance tracking, confidence scores.

**Exam connection:** TS 5.6 — claim-source mappings, conflicting statistics, temporal metadata.

---

## After Each Phase

Give a 5-question quiz covering:
1. The core pattern introduced (e.g., stop_reason, gates, hooks)
2. One anti-pattern and why it fails
3. The exam task statement and what it tests
4. A scenario where the wrong approach would cause a production incident
5. One cross-domain connection to another task statement

Score honestly. For any wrong answer: explain WHY before moving on.

## Key Rules (Exam-Critical — Reinforce Throughout)

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
