# CCA-F Study Context — AgentCX Project

> This file gives Claude Code full context about Jahir's CCA-F certification preparation.
> Read this before starting any session. All communication must be in **English**.

---

## Who is Jahir

Preparing for the **CCA-F (Claude Certified Associate – Foundations)** certification exam.
Starting level: zero prior experience with Claude Agent SDK or LLMs in general.
Study style: conceptual explanation + code examples + analogies. No assumption of prior SDK experience.
Language: **always English**.

---

## Exam Structure

- Format: Multiple choice, 1 correct + 3 distractors
- Pass score: 720 / 1,000 (scaled)
- 4 random scenarios from 6 total
- No penalty for guessing
- 5 domains weighted by importance

### Domain Weights

| Domain | Weight | Task Statements |
|---|---|---|
| D1 — Agentic Architecture & Orchestration | 27% | 7 (1.1–1.7) |
| D2 — Tool Design & MCP Integration | 18% | 4 (2.1–2.4) |
| D3 — Claude Code Configuration & Workflows | 20% | 6 (3.1–3.6) |
| D4 — Prompt Engineering & Structured Output | 20% | 6 (4.1–4.6) |
| D5 — Context Management & Reliability | 15% | 6 (5.1–5.6) |

### 6 Exam Scenarios

1. Customer Support Resolution Agent (D1, D2, D5)
2. Code Generation with Claude Code (D3, D5)
3. Multi-Agent Research System (D1, D2, D5)
4. Developer Productivity with Claude Code (D2, D3, D1)
5. Claude Code for CI/CD (D3, D4)
6. Structured Data Extraction (D4, D5)

---

## Study Progress

### What has been fully studied (interactive sessions)

**Domain 1 — Agentic Architecture & Orchestration** ✅ Complete
- TS 1.1: Agentic loops, stop_reason, anti-patterns (3 anti-patterns with simulators)
- TS 1.2: Multi-agent hub-and-spoke, context isolation, parallel vs sequential, dynamic selection
- TS 1.3: Task tool, allowedTools, AgentDefinition, fork_session (dedicated simulator built)
- TS 1.4: Enforcement vs prompt-based, prerequisite gates, multi-concern decomposition, structured handoffs
- TS 1.5: PostToolUse hooks, tool call interception, hooks vs prompt instructions (full redo after timing confusion)
- TS 1.6: Prompt chaining vs dynamic adaptive decomposition, attention dilution, Explore subagent
- TS 1.7: --resume, fork_session, when to start fresh

**Domain 2 — Tool Design & MCP Integration** ✅ Complete
- TS 2.1: Tool descriptions, differentiation, splitting generic tools, system prompt keyword effects
- TS 2.2: isError flag pattern, 4 error categories, local recovery, empty results vs errors
- TS 2.3: Scoped allowedTools, constrained alternatives, tool_choice (auto/any/forced)
- TS 2.4: .mcp.json scoping, env var expansion, MCP resources, competing with built-in tools

**Domain 3 — Claude Code Configuration & Workflows** ✅ Complete
- TS 3.1: CLAUDE.md hierarchy (user/project/directory), @import, .claude/rules/
- TS 3.2: Slash commands, skills, SKILL.md frontmatter (context:fork, allowed-tools, argument-hint)
- TS 3.3: Path-specific rules with glob patterns, vs directory CLAUDE.md
- TS 3.4: Plan mode vs direct execution decision criteria
- TS 3.5: Iterative refinement — examples, test-driven iteration, interview pattern
- TS 3.6: CI/CD with -p flag, --output-format json, avoiding duplicates, session isolation

**Domain 4 — Prompt Engineering & Structured Output** ✅ Complete
- TS 4.1: Explicit criteria vs vague instructions, false positives, severity with examples
- TS 4.2: Few-shot prompting — consistency, ambiguous cases, hallucination reduction, 2-3 examples
- TS 4.3: tool_use with JSON schemas, required/nullable/enum+other patterns, tool_choice
- TS 4.4: Retry-with-error-feedback, when retries are ineffective, detected_pattern, self-correction
- TS 4.5: Batch API (50% cost, 24h window, no SLA, no multi-turn), custom_id, SLA math
- TS 4.6: Self-review limitations, independent instances, multi-pass review, confidence reporting

**Domain 5 — Context Management & Reliability** ✅ Complete
- TS 5.1: Progressive summarization risks, lost-in-the-middle, tool result trimming, case facts block
- TS 5.2: Escalation triggers (reliable vs unreliable), explicit requests, policy gaps, ambiguity
- TS 5.3: Structured error propagation, coverage annotations, local recovery first
- TS 5.4: Context degradation signals, scratchpad files, subagent delegation, crash recovery manifests
- TS 5.5: Aggregate accuracy trap, stratified sampling, field-level confidence scores
- TS 5.6: Claim-source mappings, conflicting statistics, temporal metadata, provenance

### Study materials generated

- `ccaf-study-1.6-to-3.6.pdf` — PDF study guide for TS 1.6–3.6 (mobile-friendly)
- `ccaf-study-4.1-to-5.6.pdf` — PDF study guide for TS 4.1–5.6 (mobile-friendly)

---

## Exam Results

### Mock Exam 1 (all domains, 20 questions, max difficulty)
**Score: 13/20 (65%) — Scaled: ~685/1000 — FAIL**

| Domain | Score |
|---|---|
| D1 — Agentic Architecture | 2/5 (40%) |
| D2 — Tool Design & MCP | 2/3 (67%) |
| D3 — Claude Code | 2/3 (67%) |
| D4 — Prompt Engineering | 2/3 (67%) |
| D5 — Context Management | 2/3 (67%) |
| Cross-Domain | 3/3 (100%) |

**Weak areas identified:**
- PostToolUse hook scoping (came up 3 times)
- "Task" in allowedTools mandatory for subagent spawning
- Batch API SLA disqualification rules
- Retry ineffectiveness when information is absent from source

### Mock Exam 2 (all domains, 20 questions, max difficulty)
**Score: 16/20 (80%) — Scaled: ~820/1000 — PASS ✅**

| Domain | Score |
|---|---|
| D1 — Agentic Architecture | 3/4 (75%) |
| D2 — Tool Design & MCP | 2/3 (67%) |
| D3 — Claude Code | 3/4 (75%) |
| D4 — Prompt Engineering | 3/3 (100%) |
| D5 — Context Management | 3/3 (100%) |
| Cross-Domain | 2/3 (67%) |

**Remaining weak areas:**
- MCP env var expansion: fix is always local shell env, never architectural changes to .mcp.json
- Session independence vs fork_session: fork inherits base context, independent sessions don't
- Batch API: both SLA AND multi-turn tool calling are hard disqualifiers
- Path-specific rules: fire based on active file, not the file being generated

---

## Key Concepts to Reinforce (before exam)

### The 5 rules Jahir still misses under pressure

```
1. PostToolUse hooks fire only for the agent they're registered on
   → Register on subagents that call the tools, not the coordinator

2. "Task" in allowedTools is MANDATORY for subagent spawning
   → Without it: coordinator cannot delegate, period

3. Batch API is disqualified when:
   → SLA < 24 hours (any blocking workflow)
   → Step 2 needs step 1's output (no multi-turn tool calling)

4. Retry is pointless when information is absent from the source document
   → Accept null, route to human review — never retry missing information

5. fork_session ≠ independent session
   → fork inherits base context → use separate sessions for self-review
```

---

## The AgentCX Project

### What we're building

A **Customer Support Resolution Agent** that covers all 6 exam scenarios.
Built in 5 phases — one per domain — each adding a new layer to the same codebase.

### Project structure

```
agentcx/
├── .env                      ← ANTHROPIC_API_KEY (never commit)
├── .gitignore
├── requirements.txt
├── CONTEXT.md                ← this file
├── README.md
│
├── phase1_domain1/           ← Agentic Architecture
│   ├── agent.py              ← agentic loop with stop_reason
│   ├── tools.py              ← simulated MCP tools
│   ├── hooks.py              ← prerequisite gates + PostToolUse
│   └── coordinator.py        ← multi-agent hub-and-spoke
│
├── phase2_domain2/           ← Tool Design & MCP Integration
│   ├── tool_definitions.py   ← well-described MCP tools
│   ├── error_responses.py    ← structured error patterns
│   └── mcp_config.py         ← .mcp.json equivalent
│
├── phase3_domain3/           ← Claude Code Configuration
│   ├── CLAUDE.md
│   ├── .claude/
│   │   ├── rules/
│   │   └── commands/
│   └── ci_pipeline.py        ← -p flag, non-interactive
│
├── phase4_domain4/           ← Prompt Engineering
│   ├── classifier.py         ← explicit criteria + few-shot
│   ├── extractor.py          ← JSON schema + tool_use
│   └── validator.py          ← retry-with-error-feedback
│
└── phase5_domain5/           ← Context Management
    ├── context_manager.py    ← case facts block + trimming
    ├── escalation.py         ← escalation patterns
    └── synthesis.py          ← provenance tracking
```

### Requirements

```
anthropic>=0.40.0
python-dotenv
pydantic
```

### Phase 1 — Step-by-step plan

**Step 1: Basic agentic loop with stop_reason**
- Build a real loop using `client.messages.create`
- Intentionally introduce the 2 anti-patterns (cap as primary, text type as termination)
- Jahir identifies and fixes them
- Run and see stop_reason behavior in real Claude responses

**Step 2: Add prerequisite gate**
- Block `process_refund` until `get_customer` has run
- Implement programmatic gate (not prompt instruction)
- Show that prompt instruction fails, gate doesn't

**Step 3: Add PostToolUse hook**
- Hook captures `verified_customer_id` from `get_customer` response
- Gate opens automatically when hook fires
- Demonstrate: hook missing → gate never opens → infinite loop

**Step 4: Multi-agent coordinator**
- Coordinator with `allowedTools: ["Task"]`
- Two subagents: lookup_agent + resolution_agent
- Context isolation: subagents start empty, coordinator must inject context
- Dynamic selection: simple queries don't invoke all subagents

---

## How to continue in Claude Code

When starting a new session in Claude Code, tell it:

```
"Read CONTEXT.md — it has my CCA-F study progress and the AgentCX project plan.
We're building a Customer Support Agent to practice for the exam.
Start where the context says we left off."
```

### Teaching approach Claude Code should follow

- Always English
- Explain concepts with analogies before showing code
- When introducing bugs: show the broken code, ask Jahir to identify the bug before running it
- After each phase: short 5-question quiz on what was just built
- Connect every code decision to the specific exam task statement it demonstrates
- When Jahir gets something wrong: explain WHY before moving on — never just reveal the answer
- Pacing: Jahir signals when ready to move on — don't rush

### Anti-patterns to always call out explicitly

When Jahir writes or accepts code with these patterns, stop and flag:
1. Loop termination based on text content instead of stop_reason
2. Arbitrary iteration cap as primary loop control
3. Prompt instruction for business-critical enforcement (use hooks/gates instead)
4. isRetryable: true on business/validation/permission errors
5. Subagent context assumed inherited (must be explicitly injected)
6. Batch API for any blocking or SLA-constrained workflow
7. fork_session used where independent session is needed
8. Full tool API responses added to context without trimming
9. Aggregate accuracy reported without stratified breakdown
10. Plain text passed between agents (use structured claim-source mappings)

---

## Quick Reference — Exam Day Cheat Sheet

### stop_reason decision tree
```python
if response.stop_reason == "end_turn":   # → return final answer
if response.stop_reason == "tool_use":   # → execute tool, continue loop
# NEVER: if response.content[0].type == "text": return
# NEVER: for i in range(N): as primary termination
```

### Hook registration rule
```
Hook fires only for the agent it's registered on.
Coordinator hook → fires for coordinator's tool calls only.
Subagent hook → fires for that subagent's tool calls only.
```

### Batch API go/no-go
```
✅ Use when: non-blocking + SLA > 24h + independent requests
❌ Never when: blocking workflow OR SLA < 24h OR step 2 needs step 1's output
```

### Retry effectiveness
```
✅ Retry works: format errors, structural errors, arithmetic mismatches
❌ Retry fails: information absent from source document
```

### Error categories
```
transient   → isRetryable: true  (timeout, service down)
validation  → isRetryable: false (bad input format)
business    → isRetryable: false (policy violation → escalate)
permission  → isRetryable: false (unauthorized)
```

### CLAUDE.md loading rules
```
~/.claude/CLAUDE.md              → always (user only)
root CLAUDE.md                   → always (everyone)
subdirectory CLAUDE.md           → when editing files in that directory
.claude/rules/ with paths:       → when active file matches glob
.claude/rules/ without frontmatter → always (like root CLAUDE.md)
```

### Escalation triggers
```
✅ Reliable: explicit human request, policy gap, cannot progress
❌ Unreliable: sentiment/frustration, self-reported low confidence, "too complex"
```

### Context management checklist
```
□ Case facts block extracted BEFORE summarizing
□ Tool responses trimmed to relevant fields only
□ Case facts placed at START of every prompt
□ Scratchpad files for extended sessions (>20 turns)
□ Independent sessions for self-review (not fork_session)
```
