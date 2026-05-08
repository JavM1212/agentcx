"""
AgentCX Phase 1 — Step 4: Multi-agent coordinator (hub-and-spoke).

TS 1.2: Hub-and-spoke pattern, context isolation, explicit context injection.
TS 1.3: Task tool, allowedTools, subagent spawning.
"""

import json
import os
from dotenv import load_dotenv
import anthropic

from agentcx.phase1_domain1.tools import TOOL_DEFINITIONS, TOOL_FUNCTIONS
from agentcx.phase1_domain1.hooks import AgentState, pre_tool_gate, on_post_tool_use

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Scoped tool sets — each subagent only gets the tools it needs (TS 2.3)
LOOKUP_TOOLS = [t for t in TOOL_DEFINITIONS if t["name"] in ("get_customer", "get_order")]
RESOLUTION_TOOLS = [t for t in TOOL_DEFINITIONS if t["name"] == "process_refund"]


def run_subagent(
    system_prompt: str,
    user_message: str,
    tools: list,
    initial_state: AgentState | None = None,
) -> tuple[str, AgentState]:
    """
    Runs a subagent with its own isolated context.
    Subagents start fresh — no inherited conversation history.
    The hook is registered here, on the subagent that calls the tools.

    Returns (text_result, final_state) so the coordinator can pass
    programmatic state to the next subagent explicitly.
    """
    messages = [{"role": "user", "content": user_message}]
    state = initial_state if initial_state is not None else AgentState()

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=system_prompt,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text, state

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":

                gate_error = pre_tool_gate(block.name, block.input, state)
                if gate_error:
                    print(f"  [gate] {block.name} BLOCKED → {gate_error['error']}")
                    result = gate_error
                else:
                    tool_fn = TOOL_FUNCTIONS[block.name]
                    result = tool_fn(**block.input)
                    print(f"  [tool] {block.name}({block.input}) → {result}")

                on_post_tool_use(block.name, result, state)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})


def run_coordinator(user_message: str) -> str:
    """
    Coordinator — hub-and-spoke pattern.
    Does NOT call tools directly. Routes to subagents and assembles results.
    Explicitly passes both text context AND programmatic state between subagents.
    """
    print("\n[coordinator] Starting lookup_agent...")
    lookup_result, lookup_state = run_subagent(
        system_prompt=(
            "You are a customer lookup specialist. "
            "Look up the customer and their order using the provided tools. "
            "Return ONLY a JSON object with these fields: "
            "customer_id, customer_name, order_id, item, amount, order_status. "
            "No explanation, no markdown, just the JSON."
        ),
        user_message=user_message,
        tools=LOOKUP_TOOLS,
    )
    print(f"\n[coordinator] lookup_agent result:\n{lookup_result}")

    # Explicitly inject both text context AND state into resolution_agent
    print("\n[coordinator] Starting resolution_agent...")
    resolution_result, _ = run_subagent(
        system_prompt="You are a refund specialist. Process the refund based on the case details provided.",
        user_message=f"Case details:\n{lookup_result}\n\nOriginal request: {user_message}",
        tools=RESOLUTION_TOOLS,
        initial_state=lookup_state,  # pass verified_customer_id across subagent boundary
    )
    print(f"\n[coordinator] resolution_agent result:\n{resolution_result}")

    return resolution_result


if __name__ == "__main__":
    print("=== AgentCX Phase 1 — Step 4: Multi-Agent Coordinator ===")
    result = run_coordinator(
        "I'm customer C001. I'd like a refund for order ORD-100. It arrived damaged."
    )
    print(f"\nFinal answer: {result}")
