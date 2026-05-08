"""
AgentCX Phase 1 — Step 3: PostToolUse hook.

Hooks fire automatically after every tool call — the loop doesn't decide when.
pre_tool_gate: blocks tool execution if prerequisites aren't met.
on_post_tool_use: updates agent state after every tool call.
"""


class AgentState:
    """Holds state that persists across tool calls in a single agent run."""

    def __init__(self):
        self.verified_customer_id = None


def pre_tool_gate(tool_name: str, tool_input: dict, state: AgentState) -> dict | None:
    """
    Called before every tool execution.

    Returns None if the tool is allowed to proceed.
    Returns an error dict if the tool should be blocked.
    """
    if tool_name == "process_refund":
        if state.verified_customer_id is None:
            return {
                "error": "Gate blocked: cannot process refund before verifying customer. "
                         "Call get_customer first.",
                "isRetryable": False,
            }
    return None


def on_post_tool_use(tool_name: str, tool_result: dict, state: AgentState) -> None:
    """
    PostToolUse hook — fires after every tool call, blocked or not.
    Updates agent state based on tool results.

    EXAM RULE: This hook fires only for the agent it is registered on.
    In a multi-agent setup, register this on the subagent that calls the tools,
    not on the coordinator.
    """
    if tool_name == "get_customer" and "error" not in tool_result:
        state.verified_customer_id = tool_result["customer_id"]
        print(f"  [hook] verified_customer_id set → {state.verified_customer_id}")
