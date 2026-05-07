"""
AgentCX Phase 1 — Step 1: Agentic loop with stop_reason.
"""

import json
import os
from dotenv import load_dotenv
import anthropic

from agentcx.phase1_domain1.tools import TOOL_DEFINITIONS, TOOL_FUNCTIONS

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a customer support agent for an e-commerce company.
You have access to tools to look up customers, orders, and process refunds.
Always look up the customer and order before processing any refund."""


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

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

        # Execute all tool calls in this response
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_fn = TOOL_FUNCTIONS[block.name]
                result = tool_fn(**block.input)
                print(f"  [tool] {block.name}({block.input}) → {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

        # Append assistant response + tool results to messages
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    print("=== AgentCX Phase 1 — Agentic Loop ===\n")
    result = run_agent(
        "I'm customer C001. I'd like a refund for order ORD-100. It arrived damaged."
    )
    print(f"\nFinal answer: {result}")
