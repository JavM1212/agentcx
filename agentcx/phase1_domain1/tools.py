"""
Simulated customer support tools for AgentCX Phase 1.
These mimic real MCP tools without needing a live database.
"""

CUSTOMERS = {
    "C001": {"name": "Alice Johnson", "email": "alice@example.com", "status": "active"},
    "C002": {"name": "Bob Smith", "email": "bob@example.com", "status": "active"},
}

ORDERS = {
    "ORD-100": {"customer_id": "C001", "item": "Laptop", "amount": 999.99, "status": "delivered"},
    "ORD-101": {"customer_id": "C002", "item": "Mouse", "amount": 29.99, "status": "delivered"},
}


def get_customer(customer_id: str) -> dict:
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        return {"error": f"Customer {customer_id} not found"}
    return {"customer_id": customer_id, **customer}


def get_order(order_id: str) -> dict:
    order = ORDERS.get(order_id)
    if not order:
        return {"error": f"Order {order_id} not found"}
    return {"order_id": order_id, **order}


def process_refund(order_id: str, reason: str) -> dict:
    order = ORDERS.get(order_id)
    if not order:
        return {"error": f"Order {order_id} not found"}
    return {
        "refund_id": f"REF-{order_id}",
        "order_id": order_id,
        "amount": order["amount"],
        "status": "approved",
        "reason": reason,
    }


# Tool definitions in Anthropic format
TOOL_DEFINITIONS = [
    {
        "name": "get_customer",
        "description": "Look up a customer by their ID. Returns name, email, and account status.",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string", "description": "The customer ID, e.g. C001"}
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "get_order",
        "description": "Look up an order by order ID. Returns item, amount, and delivery status.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID, e.g. ORD-100"}
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "process_refund",
        "description": "Process a refund for a delivered order. Requires order ID and reason.",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "The order ID to refund"},
                "reason": {"type": "string", "description": "Reason for the refund"},
            },
            "required": ["order_id", "reason"],
        },
    },
]

TOOL_FUNCTIONS = {
    "get_customer": get_customer,
    "get_order": get_order,
    "process_refund": process_refund,
}
