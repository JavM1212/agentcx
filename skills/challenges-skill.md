name: ccaf-challenge-generator
description: Generate progressive-difficulty exam practice challenges for the Claude Certified Architect – Foundations (CCA-F) certification. Use this skill whenever the user wants exam prep challenges, practice questions, mock exam questions, study drills, or quiz questions for any CCA-F task statement. Also trigger when the user says things like "quiz me on", "test me on", "give me challenges for", "practice questions about", "prepare me for the exam", or references any CCA-F task statement number (e.g., "1.1", "2.3", "5.6"). This skill covers all 5 exam domains and all 24 task statements. Even if the user doesn't mention CCA-F explicitly but asks about Claude architecture exam prep, certification practice, or agentic system design questions — use this skill.
---

# CCA-F Challenge Generator

Generate 15 progressive-difficulty multiple-choice exam challenges for any single CCA-F task statement, matching the real exam format exactly.

## Before Generating Challenges

1. **Read the reference file** at `references/exam-guide-task-statements.md` to load the complete exam guide content including all task statements, knowledge areas, skills, anti-patterns, and exam scenarios.
2. **Identify the task statement** the user wants to practice. They may specify it by number (e.g., "1.1"), by topic name (e.g., "agentic loops"), or by describing what they want to study. Map it to the correct task statement.
3. **Extract the testable surface** — every bullet under "Knowledge of" and "Skills in" for that task statement is a potential question topic. Also pull in relevant anti-patterns and exam scenarios that involve this task statement.

## Challenge Generation Rules

### Format (Match Real Exam Exactly)
- Each challenge: 1 correct answer + 3 plausible distractors (A/B/C/D)
- All questions are scenario-based with realistic production context
- Single best answer format: "Select the single response that best completes the statement or answers the question"
- Distractors must be plausible to someone with incomplete knowledge — not obviously wrong

### Progressive Difficulty Curve
Generate 15 challenges following this difficulty ramp:

| Challenges | Difficulty | Star Rating | What's Tested |
|-----------|-----------|-------------|---------------|
| 1–3 | Foundational | ★☆☆☆☆ to ★★☆☆☆ | Direct recall of concepts, definitions, and basic principles from the Knowledge areas |
| 4–6 | Applied | ★★☆☆☆ to ★★★☆☆ | Applying concepts to straightforward scenarios. Recognizing correct implementations |
| 7–9 | Analytical | ★★★☆☆ to ★★★★☆ | Debugging scenarios, choosing between two plausible approaches, identifying anti-patterns in code |
| 10–12 | Synthesis | ★★★★☆ | Combining multiple concepts from the task statement. Multi-step reasoning. Tradeoff analysis |
| 13–15 | Expert | ★★★★★ | Edge cases, subtle distinctions, scenarios where 2+ options seem correct and you must pick the BEST one. Cross-references with other task statements |

### Distractor Design (Critical for Quality)
Distractors should represent common misconceptions and near-misses:
- **Partial truth**: Correct in some cases but not this specific scenario
- **Adjacent concept**: From a related task statement but wrong for this one
- **Over-engineered**: Technically works but violates the principle of proportional response
- **Anti-pattern dressed up**: Sounds professional but is explicitly named as an anti-pattern in the exam guide
- **Absolutist**: Uses words like "always" or "never" when the correct answer requires nuance

### Scenario Design
- Ground every question in one of the 6 exam scenarios (Customer Support Agent, Code Generation, Multi-Agent Research, Developer Productivity, CI/CD Integration, Structured Data Extraction) or a realistic production variant
- Include concrete details: tool names, error rates, log observations, code snippets, configuration files
- Higher difficulty questions should include code snippets, configuration examples, or API response payloads where relevant

### Answer Validation Feedback
When the user answers, provide:
1. **Correct/Incorrect** verdict
2. **Why the correct answer is correct** — tie back to specific exam guide language
3. **Why each wrong answer is wrong** — explain the specific flaw
4. **Exam Tip** — a memorable rule or pattern to remember for exam day
5. **Difficulty adjustment note** — if the user got it wrong, explain the concept before moving on

## Delivery Protocol

### One at a Time
- Send challenges **one at a time**
- Wait for the user's answer before revealing the explanation
- After explaining, immediately present the next challenge
- Show progress: "Challenge X / 15 — Difficulty: ★★★☆☆"

### Tracking
- Keep a running score (e.g., "Score: 8/10 so far")
- At the end of all 15, provide a summary:
  - Total score
  - Which knowledge areas were strong
  - Which knowledge areas need review
  - Specific concepts to revisit with page references to the exam guide

### Adaptive Behavior
- If the user gets 3+ wrong in a row, pause and teach the concept before continuing
- If the user gets all foundational questions right, acknowledge momentum
- If the user asks "why?" or "explain more" — go deeper, show code examples, reference the official docs

## Cross-Referencing
Higher-difficulty questions (10–15) should test how this task statement interacts with related ones. For example:
- Task 1.1 (agentic loops) + Task 1.5 (hooks) → "Your loop runs correctly but needs a compliance gate"
- Task 2.1 (tool descriptions) + Task 2.3 (tool distribution) → "Tools are well-described but too many are assigned"
- Task 4.3 (structured output) + Task 4.4 (validation/retry) → "Schema works but semantic errors persist"

Use the exam guide's own cross-references (each scenario lists its primary domains) to find natural intersections.

## Quality Checklist (Self-Verify Before Presenting Each Challenge)
Before presenting each challenge, verify:
- [ ] Question is scenario-based with production context
- [ ] Exactly 4 options (A, B, C, D)
- [ ] Exactly 1 correct answer
- [ ] All 3 distractors are plausible to someone with partial knowledge
- [ ] Difficulty matches the intended tier
- [ ] Question tests content from the specified task statement's Knowledge/Skills bullets
- [ ] No ambiguity — one answer is clearly best when you have full knowledge
- [ ] Code snippets (if any) are syntactically valid and realistic