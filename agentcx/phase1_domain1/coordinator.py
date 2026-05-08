"""
AgentCX Phase 1 — Step 4 (extended): Parallel subagents + dynamic selection.

TS 1.2: Hub-and-spoke, context isolation, parallel vs sequential, dynamic selection.
TS 1.3: Scoped allowedTools, explicit context injection.
"""

import json
import os
import threading
from dotenv import load_dotenv
import anthropic

from agentcx.phase1_domain1.tools import TOOL_DEFINITIONS, TOOL_FUNCTIONS
from agentcx.phase1_domain1.hooks import AgentState, pre_tool_gate, on_post_tool_use

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Scoped tool sets — each subagent only gets the tools it needs (TS 2.3)
LOOKUP_TOOLS = [t for t in TOOL_DEFINITIONS if t["name"] in ("get_customer", "get_order")]
POLICY_TOOLS = [t for t in TOOL_DEFINITIONS if t["name"] == "get_refund_policy"]
RESOLUTION_TOOLS = [t for t in TOOL_DEFINITIONS if t["name"] == "process_refund"]


def run_subagent(
    system_prompt: str,
    user_message: str,
    tools: list,
    initial_state: AgentState | None = None,
    prefill: str | None = None,
) -> tuple[str, AgentState]:
    """
    Runs a subagent with its own isolated context.
    Subagents start fresh — no inherited conversation history.
    The hook is registered here, on the subagent that calls the tools.

    prefill: optional assistant turn prefix to force output format (e.g. "{" for JSON).
    Returns (text_result, final_state) so the coordinator can pass
    programmatic state to the next subagent explicitly.
    """
    messages = [{"role": "user", "content": user_message}]
    if prefill:
        messages.append({"role": "assistant", "content": prefill})
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
            text = response.content[0].text
            return (prefill + text if prefill else text), state

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


def is_refund_request(user_message: str) -> bool:
    """
    Dynamic selection — coordinator decides which subagents to invoke.
    Simple keyword check for demo purposes.
    """
    keywords = ["refund", "return", "damaged", "broken", "charge"]
    return any(k in user_message.lower() for k in keywords)


def extract_category_hint(user_message: str) -> str:
    """Extract product category from user message for parallel policy lookup."""
    msg = user_message.lower()
    if any(w in msg for w in ["laptop", "phone", "monitor", "computer", "tablet"]):
        return "electronics"
    if any(w in msg for w in ["mouse", "keyboard", "cable", "charger", "headphone"]):
        return "accessories"
    return "default"


def run_coordinator(user_message: str) -> str:
    """
    Coordinator — hub-and-spoke with parallel subagents and dynamic selection.

    parallel:   lookup_agent + policy_agent run simultaneously (independent)
    sequential: resolution_agent runs after both finish (depends on their output)
    dynamic:    policy_agent only invoked for refund requests
    """
    results = {}

    def run_lookup():
        text, state = run_subagent(
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
        results["lookup_text"] = text
        results["lookup_state"] = state

    # Dynamic selection: only fetch policy for refund requests
    needs_refund = is_refund_request(user_message)
    category_hint = extract_category_hint(user_message)

    def run_policy():
        text, _ = run_subagent(
            system_prompt=(
                "You are a policy specialist. "
                "Look up the refund policy using get_refund_policy. "
                "Return ONLY a JSON object with the policy details. "
                "No explanation, no markdown, just the JSON."
            ),
            user_message=f"Look up the refund policy for category: {category_hint}",
            tools=POLICY_TOOLS,
            prefill="{",
        )
        results["policy_text"] = text

    # Launch parallel threads
    threads = []
    t1 = threading.Thread(target=run_lookup)
    threads.append(t1)

    if needs_refund:
        t2 = threading.Thread(target=run_policy)
        threads.append(t2)

    print("\n[coordinator] Launching parallel subagents...")
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(f"\n[coordinator] lookup_agent result:\n{results.get('lookup_text')}")
    if needs_refund:
        print(f"\n[coordinator] policy_agent result:\n{results.get('policy_text')}")

    # Build context for resolution_agent
    resolution_context = f"Case details:\n{results['lookup_text']}"
    if needs_refund and "policy_text" in results:
        resolution_context += f"\n\nRefund policy:\n{results['policy_text']}"
    resolution_context += f"\n\nOriginal request: {user_message}"

    print("\n[coordinator] Starting resolution_agent (sequential — depends on above)...")
    resolution_result, _ = run_subagent(
        system_prompt="You are a refund specialist. Process the refund based on the case details and policy provided.",
        user_message=resolution_context,
        tools=RESOLUTION_TOOLS,
        initial_state=results["lookup_state"],
    )

    return resolution_result


if __name__ == "__main__":
    print("=== AgentCX Phase 1 — Parallel Subagents + Dynamic Selection ===")
    result = run_coordinator(
        "I'm customer C001. I'd like a refund for order ORD-100. It arrived damaged."
    )
    print(f"\nFinal answer: {result}")
