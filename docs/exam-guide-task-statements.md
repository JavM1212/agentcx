# CCA-F Exam Guide — Complete Task Statements Reference

## Exam Structure
- Format: Multiple choice, 1 correct + 3 distractors per question
- Pass score: 720 / 1000 (scaled)
- 4 random scenarios from 6 total
- No penalty for guessing

## Domain Weights
- Domain 1: Agentic Architecture & Orchestration (27%)
- Domain 2: Tool Design & MCP Integration (18%)
- Domain 3: Claude Code Configuration & Workflows (20%)
- Domain 4: Prompt Engineering & Structured Output (20%)
- Domain 5: Context Management & Reliability (15%)

---

## Domain 1: Agentic Architecture & Orchestration (27%)

### Task Statement 1.1: Design and implement agentic loops for autonomous task execution

**Knowledge of:**
- The agentic loop lifecycle: sending requests to Claude, inspecting stop_reason ("tool_use" vs "end_turn"), executing requested tools, and returning results for the next iteration
- How tool results are appended to conversation history so the model can reason about the next action
- The distinction between model-driven decision-making (Claude reasons about which tool to call next based on context) and pre-configured decision trees or tool sequences

**Skills in:**
- Implementing agentic loop control flow that continues when stop_reason is "tool_use" and terminates when stop_reason is "end_turn"
- Adding tool results to conversation context between iterations so the model can incorporate new information into its reasoning
- Avoiding anti-patterns such as parsing natural language signals to determine loop termination, setting arbitrary iteration caps as the primary stopping mechanism, or checking for assistant text content as a completion indicator

### Task Statement 1.2: Orchestrate multi-agent systems with coordinator-subagent patterns

**Knowledge of:**
- Hub-and-spoke architecture where a coordinator agent manages all inter-subagent communication, error handling, and information routing
- How subagents operate with isolated context—they do not inherit the coordinator's conversation history automatically
- The role of the coordinator in task decomposition, delegation, result aggregation, and deciding which subagents to invoke based on query complexity
- Risks of overly narrow task decomposition by the coordinator, leading to incomplete coverage of broad research topics

**Skills in:**
- Designing coordinator agents that analyze query requirements and dynamically select which subagents to invoke rather than always routing through the full pipeline
- Partitioning research scope across subagents to minimize duplication (e.g., assigning distinct subtopics or source types to each agent)
- Implementing iterative refinement loops where the coordinator evaluates synthesis output for gaps, re-delegates to search and analysis subagents with targeted queries, and re-invokes synthesis until coverage is sufficient
- Routing all subagent communication through the coordinator for observability, consistent error handling, and controlled information flow

### Task Statement 1.3: Configure subagent invocation, context passing, and spawning

**Knowledge of:**
- The Task tool as the mechanism for spawning subagents, and the requirement that allowedTools must include "Task" for a coordinator to invoke subagents
- That subagent context must be explicitly provided in the prompt—subagents do not automatically inherit parent context or share memory between invocations
- The AgentDefinition configuration including descriptions, system prompts, and tool restrictions for each subagent type
- Fork-based session management for exploring divergent approaches from a shared analysis baseline

**Skills in:**
- Including complete findings from prior agents directly in the subagent's prompt (e.g., passing web search results and document analysis outputs to the synthesis subagent)
- Using structured data formats to separate content from metadata (source URLs, document names, page numbers) when passing context between agents to preserve attribution
- Spawning parallel subagents by emitting multiple Task tool calls in a single coordinator response rather than across separate turns
- Designing coordinator prompts that specify research goals and quality criteria rather than step-by-step procedural instructions, to enable subagent adaptability

### Task Statement 1.4: Implement multi-step workflows with enforcement and handoff patterns

**Knowledge of:**
- The difference between programmatic enforcement (hooks, prerequisite gates) and prompt-based guidance for workflow ordering
- When deterministic compliance is required (e.g., identity verification before financial operations), prompt instructions alone have a non-zero failure rate
- Structured handoff protocols for mid-process escalation that include customer details, root cause analysis, and recommended actions

**Skills in:**
- Implementing programmatic prerequisites that block downstream tool calls until prerequisite steps have completed (e.g., blocking process_refund until get_customer has returned a verified customer ID)
- Decomposing multi-concern customer requests into distinct items, then investigating each in parallel using shared context before synthesizing a unified resolution
- Compiling structured handoff summaries (customer ID, root cause, refund amount, recommended action) when escalating to human agents who lack access to the conversation transcript

### Task Statement 1.5: Apply Agent SDK hooks for tool call interception and data normalization

**Knowledge of:**
- Hook patterns (e.g., PostToolUse) that intercept tool results for transformation before the model processes them
- Hook patterns that intercept outgoing tool calls to enforce compliance rules (e.g., blocking refunds above a threshold)
- The distinction between using hooks for deterministic guarantees versus relying on prompt instructions for probabilistic compliance

**Skills in:**
- Implementing PostToolUse hooks to normalize heterogeneous data formats (Unix timestamps, ISO 8601, numeric status codes) from different MCP tools before the agent processes them
- Implementing tool call interception hooks that block policy-violating actions (e.g., refunds exceeding $500) and redirect to alternative workflows (e.g., human escalation)
- Choosing hooks over prompt-based enforcement when business rules require guaranteed compliance

### Task Statement 1.6: Design task decomposition strategies for complex workflows

**Knowledge of:**
- When to use fixed sequential pipelines (prompt chaining) versus dynamic adaptive decomposition based on intermediate findings
- Prompt chaining patterns that break reviews into sequential steps (e.g., analyze each file individually, then run a cross-file integration pass)
- The value of adaptive investigation plans that generate subtasks based on what is discovered at each step

**Skills in:**
- Selecting task decomposition patterns appropriate to the workflow: prompt chaining for predictable multi-aspect reviews, dynamic decomposition for open-ended investigation tasks
- Splitting large code reviews into per-file local analysis passes plus a separate cross-file integration pass to avoid attention dilution
- Decomposing open-ended tasks (e.g., "add comprehensive tests to a legacy codebase") by first mapping structure, identifying high-impact areas, then creating a prioritized plan that adapts as dependencies are discovered

### Task Statement 1.7: Manage session state, resumption, and forking

**Knowledge of:**
- Named session resumption using --resume <session-name> to continue a specific prior conversation
- fork_session for creating independent branches from a shared analysis baseline to explore divergent approaches
- The importance of informing the agent about changes to previously analyzed files when resuming sessions after code modifications
- Why starting a new session with a structured summary is more reliable than resuming with stale tool results

**Skills in:**
- Using --resume with session names to continue named investigation sessions across work sessions
- Using fork_session to create parallel exploration branches (e.g., comparing two testing strategies or refactoring approaches from a shared codebase analysis)
- Choosing between session resumption (when prior context is mostly valid) and starting fresh with injected summaries (when prior tool results are stale)
- Informing a resumed session about specific file changes for targeted re-analysis rather than requiring full re-exploration

---

## Domain 2: Tool Design & MCP Integration (18%)

### Task Statement 2.1: Design effective tool interfaces with clear descriptions and boundaries

**Knowledge of:**
- Tool descriptions as the primary mechanism LLMs use for tool selection; minimal descriptions lead to unreliable selection among similar tools
- The importance of including input formats, example queries, edge cases, and boundary explanations in tool descriptions
- How ambiguous or overlapping tool descriptions cause misrouting
- The impact of system prompt wording on tool selection

**Skills in:**
- Writing tool descriptions that clearly differentiate each tool's purpose, expected inputs, outputs, and when to use it versus similar alternatives
- Renaming tools and updating descriptions to eliminate functional overlap
- Splitting generic tools into purpose-specific tools with defined input/output contracts
- Reviewing system prompts for keyword-sensitive instructions that might override well-written tool descriptions

### Task Statement 2.2: Implement structured error responses for MCP tools

**Knowledge of:**
- The MCP isError flag pattern for communicating tool failures back to the agent
- The distinction between transient errors (timeouts, service unavailability), validation errors (invalid input), business errors (policy violations), and permission errors
- Why uniform error responses prevent the agent from making appropriate recovery decisions
- The difference between retryable and non-retryable errors

**Skills in:**
- Returning structured error metadata including errorCategory (transient/validation/permission), isRetryable boolean, and human-readable descriptions
- Including retriable: false flags and customer-friendly explanations for business rule violations
- Implementing local error recovery within subagents for transient failures, propagating to the coordinator only errors that cannot be resolved locally
- Distinguishing between access failures and valid empty results

### Task Statement 2.3: Distribute tools appropriately across agents and configure tool choice

**Knowledge of:**
- Giving an agent access to too many tools (e.g., 18 instead of 4-5) degrades tool selection reliability
- Why agents with tools outside their specialization tend to misuse them
- Scoped tool access: giving agents only the tools needed for their role
- tool_choice configuration options: "auto", "any", and forced tool selection

**Skills in:**
- Restricting each subagent's tool set to those relevant to its role
- Replacing generic tools with constrained alternatives
- Providing scoped cross-role tools for high-frequency needs while routing complex cases through the coordinator
- Using tool_choice forced selection to ensure a specific tool is called first
- Setting tool_choice: "any" to guarantee the model calls a tool rather than returning conversational text

### Task Statement 2.4: Integrate MCP servers into Claude Code and agent workflows

**Knowledge of:**
- MCP server scoping: project-level (.mcp.json) for shared team tooling vs user-level (~/.claude.json) for personal/experimental servers
- Environment variable expansion in .mcp.json for credential management
- Tools from all configured MCP servers are discovered at connection time and available simultaneously
- MCP resources as a mechanism for exposing content catalogs to reduce exploratory tool calls

**Skills in:**
- Configuring shared MCP servers in project-scoped .mcp.json with environment variable expansion
- Configuring personal/experimental MCP servers in user-scoped ~/.claude.json
- Enhancing MCP tool descriptions to prevent the agent from preferring built-in tools over more capable MCP tools
- Choosing existing community MCP servers over custom implementations for standard integrations
- Exposing content catalogs as MCP resources

### Task Statement 2.5: Select and apply built-in tools effectively

**Knowledge of:**
- Grep for content search (searching file contents for patterns)
- Glob for file path pattern matching (finding files by name or extension)
- Read/Write for full file operations; Edit for targeted modifications using unique text matching
- When Edit fails due to non-unique text matches, using Read + Write as a fallback

**Skills in:**
- Selecting Grep for searching code content across a codebase
- Selecting Glob for finding files matching naming patterns
- Using Read + Write when Edit cannot find unique anchor text
- Building codebase understanding incrementally: Grep to find entry points, then Read to follow imports
- Tracing function usage across wrapper modules

---

## Domain 3: Claude Code Configuration & Workflows (20%)

### Task Statement 3.1: Configure CLAUDE.md files with appropriate hierarchy, scoping, and modular organization

**Knowledge of:**
- The CLAUDE.md configuration hierarchy: user-level (~/.claude/CLAUDE.md), project-level (.claude/CLAUDE.md or root CLAUDE.md), and directory-level (subdirectory CLAUDE.md files)
- User-level settings apply only to that user—not shared via version control
- The @import syntax for referencing external files
- .claude/rules/ directory for topic-specific rule files

**Skills in:**
- Diagnosing configuration hierarchy issues
- Using @import to selectively include relevant standards files
- Splitting large CLAUDE.md files into focused topic-specific files in .claude/rules/
- Using the /memory command to verify which memory files are loaded

### Task Statement 3.2: Create and configure custom slash commands and skills

**Knowledge of:**
- Project-scoped commands in .claude/commands/ (shared via version control) vs user-scoped commands in ~/.claude/commands/ (personal)
- Skills in .claude/skills/ with SKILL.md files that support frontmatter: context: fork, allowed-tools, argument-hint
- The context: fork frontmatter option for running skills in isolated sub-agent context
- Personal skill customization in ~/.claude/skills/

**Skills in:**
- Creating project-scoped slash commands in .claude/commands/
- Using context: fork to isolate verbose output skills
- Configuring allowed-tools in skill frontmatter
- Using argument-hint for required parameters
- Choosing between skills (on-demand) and CLAUDE.md (always-loaded)

### Task Statement 3.3: Apply path-specific rules for conditional convention loading

**Knowledge of:**
- .claude/rules/ files with YAML frontmatter paths fields containing glob patterns
- Path-scoped rules load only when editing matching files
- Glob-pattern rules vs directory-level CLAUDE.md files for cross-directory conventions

**Skills in:**
- Creating .claude/rules/ files with YAML frontmatter path scoping
- Using glob patterns for file-type conventions regardless of directory location
- Choosing path-specific rules over subdirectory CLAUDE.md when conventions span the codebase

### Task Statement 3.4: Determine when to use plan mode vs direct execution

**Knowledge of:**
- Plan mode for complex tasks: large-scale changes, multiple valid approaches, architectural decisions
- Direct execution for simple, well-scoped changes
- Plan mode enables safe codebase exploration before committing to changes
- The Explore subagent for isolating verbose discovery output

**Skills in:**
- Selecting plan mode for tasks with architectural implications
- Selecting direct execution for well-understood, clear-scope changes
- Using the Explore subagent to prevent context window exhaustion
- Combining plan mode for investigation with direct execution for implementation

### Task Statement 3.5: Apply iterative refinement techniques for progressive improvement

**Knowledge of:**
- Concrete input/output examples as most effective for communicating expected transformations
- Test-driven iteration: writing test suites first, then iterating by sharing test failures
- The interview pattern: having Claude ask questions before implementing
- When to provide all issues in a single message vs sequential fixes

**Skills in:**
- Providing 2-3 concrete input/output examples for transformation requirements
- Writing test suites before implementation, iterating by sharing failures
- Using the interview pattern for unfamiliar domains
- Addressing interacting issues together vs independent issues sequentially

### Task Statement 3.6: Integrate Claude Code into CI/CD pipelines

**Knowledge of:**
- The -p (--print) flag for non-interactive mode
- --output-format json and --json-schema for structured CI output
- CLAUDE.md for project context in CI-invoked Claude Code
- Session context isolation: same Claude session is less effective at self-review

**Skills in:**
- Running Claude Code in CI with -p flag
- Using --output-format json with --json-schema for machine-parseable output
- Including prior review findings to avoid duplicate comments
- Providing existing test files in context to avoid duplicate test suggestions
- Documenting testing standards in CLAUDE.md for CI quality

---

## Domain 4: Prompt Engineering & Structured Output (20%)

### Task Statement 4.1: Design prompts with explicit criteria for precision

**Knowledge of:**
- Explicit criteria over vague instructions
- General instructions like "be conservative" fail to improve precision
- High false positive rates undermine developer trust

**Skills in:**
- Writing specific review criteria defining what to report vs skip
- Temporarily disabling high false-positive categories
- Defining explicit severity criteria with concrete code examples

### Task Statement 4.2: Apply few-shot prompting for consistency and quality

**Knowledge of:**
- Few-shot examples as most effective for consistently formatted output
- Few-shot examples for demonstrating ambiguous-case handling
- Few-shot examples enable generalization to novel patterns
- Effectiveness for reducing hallucination in extraction tasks

**Skills in:**
- Creating 2-4 targeted few-shot examples for ambiguous scenarios
- Including examples demonstrating specific desired output format
- Providing examples distinguishing acceptable patterns from genuine issues
- Using examples for varied document structures
- Adding examples for correct extraction from varied formats

### Task Statement 4.3: Enforce structured output using tool use and JSON schemas

**Knowledge of:**
- Tool use with JSON schemas as most reliable for guaranteed schema-compliant output
- tool_choice: "auto" vs "any" vs forced tool selection
- Strict JSON schemas eliminate syntax errors but not semantic errors
- Schema design: required vs optional fields, enum + "other" patterns

**Skills in:**
- Defining extraction tools with JSON schemas as input parameters
- Setting tool_choice: "any" for guaranteed structured output with multiple schemas
- Forcing specific tools with tool_choice
- Designing optional/nullable fields to prevent hallucination
- Adding enum values like "unclear" and "other" + detail fields

### Task Statement 4.4: Implement validation, retry, and feedback loops

**Knowledge of:**
- Retry-with-error-feedback: appending validation errors to prompt on retry
- Limits of retry: ineffective when information is absent from source
- Feedback loop design with detected_pattern fields
- Semantic validation errors vs schema syntax errors

**Skills in:**
- Implementing follow-up requests with original document + failed extraction + specific errors
- Identifying when retries will be ineffective vs when they'll succeed
- Adding detected_pattern fields for false positive analysis
- Designing self-correction flows with calculated vs stated totals

### Task Statement 4.5: Design efficient batch processing strategies

**Knowledge of:**
- Message Batches API: 50% cost savings, up to 24-hour processing, no latency SLA
- Appropriate for non-blocking, latency-tolerant workloads
- Batch API does not support multi-turn tool calling within a single request
- custom_id fields for correlating request/response pairs

**Skills in:**
- Matching API approach to latency requirements
- Calculating batch submission frequency based on SLA constraints
- Handling batch failures by resubmitting failed documents via custom_id
- Using prompt refinement on samples before batch-processing

### Task Statement 4.6: Design multi-instance and multi-pass review architectures

**Knowledge of:**
- Self-review limitations: model retains reasoning context from generation
- Independent review instances more effective than self-review
- Multi-pass review: per-file local passes + cross-file integration passes

**Skills in:**
- Using a second independent Claude instance for review
- Splitting large reviews into focused per-file passes + integration passes
- Running verification passes with confidence self-reporting

---

## Domain 5: Context Management & Reliability (15%)

### Task Statement 5.1: Manage conversation context across long interactions

**Knowledge of:**
- Progressive summarization risks with numerical values and dates
- "Lost in the middle" effect
- Tool results accumulating tokens disproportionately
- Importance of passing complete conversation history

**Skills in:**
- Extracting transactional facts into persistent "case facts" blocks
- Trimming verbose tool outputs to relevant fields
- Placing key findings at beginning, detailed results with section headers
- Requiring subagents to include metadata in structured outputs
- Modifying upstream agents to return structured data instead of verbose content

### Task Statement 5.2: Design escalation and ambiguity resolution patterns

**Knowledge of:**
- Appropriate escalation triggers: customer requests for human, policy exceptions/gaps, inability to progress
- Escalating immediately for explicit human requests vs offering to resolve straightforward issues
- Sentiment-based escalation and self-reported confidence are unreliable
- Multiple customer matches require clarification, not heuristic selection

**Skills in:**
- Adding explicit escalation criteria with few-shot examples
- Honoring explicit customer requests immediately
- Acknowledging frustration while offering resolution
- Escalating when policy is ambiguous
- Asking for additional identifiers for multiple matches

### Task Statement 5.3: Implement error propagation across multi-agent systems

**Knowledge of:**
- Structured error context enabling intelligent coordinator recovery
- Distinction between access failures and valid empty results
- Why generic error statuses hide valuable context
- Why silently suppressing errors or terminating entire workflows are both anti-patterns

**Skills in:**
- Returning structured error context with failure type, what was attempted, partial results, and alternatives
- Distinguishing access failures from valid empty results
- Having subagents implement local recovery first
- Structuring synthesis output with coverage annotations

### Task Statement 5.4: Manage context in large codebase exploration

**Knowledge of:**
- Context degradation in extended sessions
- The role of scratchpad files for persisting findings
- Subagent delegation for isolating verbose exploration
- Structured state persistence for crash recovery

**Skills in:**
- Spawning subagents for specific investigation questions
- Maintaining scratchpad files recording key findings
- Summarizing findings before spawning sub-agents for next phase
- Designing crash recovery using structured manifests
- Using /compact during extended exploration

### Task Statement 5.5: Design human review workflows and confidence calibration

**Knowledge of:**
- Aggregate accuracy may mask poor performance on specific types
- Stratified random sampling for error rate measurement
- Field-level confidence scores calibrated with labeled validation sets
- Validating accuracy by document type and field before automating

**Skills in:**
- Implementing stratified random sampling of high-confidence extractions
- Analyzing accuracy by document type and field
- Having models output field-level confidence scores with calibrated thresholds
- Routing low-confidence extractions to human review

### Task Statement 5.6: Preserve information provenance in multi-source synthesis

**Knowledge of:**
- Source attribution lost during summarization
- Structured claim-source mappings
- Handling conflicting statistics with source annotation
- Temporal data requiring publication/collection dates

**Skills in:**
- Requiring subagents to output structured claim-source mappings
- Structuring reports distinguishing well-established from contested findings
- Completing analysis with conflicting values explicitly annotated
- Requiring publication/data collection dates
- Rendering different content types appropriately in synthesis

---

## Exam Scenarios

### Scenario 1: Customer Support Resolution Agent
Agent handles returns, billing disputes, account issues. MCP tools: get_customer, lookup_order, process_refund, escalate_to_human. Target: 80%+ first-contact resolution.
Domains: 1, 2, 5

### Scenario 2: Code Generation with Claude Code
Team uses Claude Code for code generation, refactoring, debugging, documentation. Custom slash commands, CLAUDE.md configs, plan mode.
Domains: 3, 5

### Scenario 3: Multi-Agent Research System
Coordinator delegates to web search, document analysis, synthesis, and report subagents. Produces comprehensive cited reports.
Domains: 1, 2, 5

### Scenario 4: Developer Productivity with Claude
Agent helps engineers explore codebases, understand legacy systems. Built-in tools + MCP servers.
Domains: 2, 3, 1

### Scenario 5: Claude Code for Continuous Integration
Automated code reviews, test generation, PR feedback in CI/CD. Structured output, actionable feedback, minimize false positives.
Domains: 3, 4

### Scenario 6: Structured Data Extraction
Extract from unstructured documents, validate with JSON schemas, handle edge cases, integrate with downstream systems.
Domains: 4, 5

---

## Anti-Patterns Explicitly Named in Exam Guide

### Agentic Loop Anti-Patterns (Task 1.1):
1. Parsing natural language signals to determine loop termination
2. Setting arbitrary iteration caps as the primary stopping mechanism
3. Checking for assistant text content as a completion indicator

### Tool Design Anti-Patterns:
- Minimal tool descriptions leading to unreliable selection
- Giving agents too many tools (18 instead of 4-5)
- Agents with tools outside their specialization misusing them

### Error Handling Anti-Patterns:
- Uniform error responses ("Operation failed")
- Silently suppressing errors (empty results as success)
- Terminating entire workflows on single failures

### Context Anti-Patterns:
- Progressive summarization losing numerical values
- Not trimming verbose tool outputs
- Self-review in the same session (retains reasoning context)