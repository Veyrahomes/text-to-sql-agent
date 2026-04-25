"""LangGraph graph assembly for the Text-to-SQL agent."""
from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent.nodes import (
    router_node,
    sql_generator_node,
    query_executor_node,
    response_formatter_node,
    fallback_node,
    email_node,
    should_query_database,
    should_retry_query,
)


def should_email(state: AgentState) -> str:
    """Conditional edge: send email or end?"""
    if state.get("should_send_email"):
        return "email_sender"
    return "end"


def build_graph():
    workflow = StateGraph(AgentState)

    # Add all nodes
    workflow.add_node("router", router_node)
    workflow.add_node("sql_generator", sql_generator_node)
    workflow.add_node("query_executor", query_executor_node)
    workflow.add_node("response_formatter", response_formatter_node)
    workflow.add_node("fallback_response", fallback_node)
    workflow.add_node("email_sender", email_node)

    # Edges
    workflow.add_edge(START, "router")

    workflow.add_conditional_edges(
        "router",
        should_query_database,
        {
            "sql_generator": "sql_generator",
            "fallback_response": "fallback_response",
        },
    )

    workflow.add_edge("sql_generator", "query_executor")

    workflow.add_conditional_edges(
        "query_executor",
        should_retry_query,
        {
            "sql_generator": "sql_generator",
            "response_formatter": "response_formatter",
        },
    )

    # After formatting, check if we should email
    workflow.add_conditional_edges(
        "response_formatter",
        should_email,
        {
            "email_sender": "email_sender",
            "end": END,
        },
    )

    workflow.add_edge("email_sender", END)
    workflow.add_edge("fallback_response", END)

    return workflow.compile()


graph = build_graph()