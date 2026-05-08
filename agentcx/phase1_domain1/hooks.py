"""
AgentCX Phase 1 — Step 2: Prerequisite gate.

Intercepts tool calls before they reach tools.py.
Blocks process_refund until get_customer has run successfully.
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


def post_tool_update(tool_name: str, tool_result: dict, state: AgentState) -> None:
    """
    Called after every tool execution.
    Updates agent state based on tool results.
    """
    if tool_name == "get_customer" and "error" not in tool_result:
        state.verified_customer_id = tool_result["customer_id"]
