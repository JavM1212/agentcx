"""
AgentCX Phase 1 — Step 3: PostToolUse hook wired into the agentic loop.
"""

import json
import os
from dotenv import load_dotenv
import anthropic

from agentcx.phase1_domain1.tools import TOOL_DEFINITIONS, TOOL_FUNCTIONS
from agentcx.phase1_domain1.hooks import AgentState, pre_tool_gate, on_post_tool_use

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a customer support agent for an e-commerce company.
You have access to tools to look up customers, orders, and process refunds.
Always look up the customer and order before processing any refund."""


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    state = AgentState()

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

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


if __name__ == "__main__":
    print("=== AgentCX Phase 1 — Step 3: PostToolUse Hook ===\n")
    result = run_agent(
        "I'm customer C001. I'd like a refund for order ORD-100. It arrived damaged."
    )
    print(f"\nFinal answer: {result}")
