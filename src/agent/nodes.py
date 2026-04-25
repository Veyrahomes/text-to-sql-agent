"""LangGraph nodes powered by Ollama LLM."""
from typing import Dict, Any
from src.agent.state import AgentState
from src.agent.llm import create_llm, SQL_PROMPT, FORMAT_PROMPT, get_schema_info_str
from src.tools.db_tools import execute_query
from src.tools.email_tools import should_send_email

# Create LLM once at module level
llm = create_llm()


def router_node(state: AgentState) -> Dict[str, Any]:
    """Route the question: is it database-related? Should we email?"""
    question = state.get("user_question", "").lower()
    db_keywords = [
        "customer", "order", "product", "sale", "revenue",
        "inventory", "stock", "spend", "spent", "purchase", "supplier",
        "category", "price", "quantity", "status", "country",
        "email", "signup", "lifetime", "shipped", "delivered",
        "pending", "cancelled", "total", "amount", "most", "report"
    ]
    is_db_related = any(keyword in question for keyword in db_keywords)

    return {
        "is_db_related": is_db_related,
        "should_send_email": should_send_email(question),
        "retry_count": 0,
        "generated_sql": None,
        "query_results": None,
        "query_error": None,
        "final_response": None,
    }


def should_query_database(state: AgentState) -> str:
    """Conditional edge: go to SQL generator or fallback?"""
    return "sql_generator" if state.get("is_db_related") else "fallback_response"


def should_retry_query(state: AgentState) -> str:
    """Conditional edge: retry on error or proceed to formatting?"""
    if state.get("query_error") and state.get("retry_count", 0) < state.get("max_retries", 3):
        return "sql_generator"
    return "response_formatter"


def sql_generator_node(state: AgentState) -> Dict[str, Any]:
    """Generate SQL using Ollama LLM."""
    question = state.get("user_question", "")
    error = state.get("query_error", "")

    schema = get_schema_info_str()

    if error:
        prompt = f"{SQL_PROMPT.format(schema=schema, question=question)}\nPrevious query failed with error: {error}\nCorrected SQL:"
    else:
        prompt = SQL_PROMPT.format(schema=schema, question=question)

    response = llm.invoke(prompt)
    sql = response.content.strip()

    # Clean up markdown code blocks
    if sql.startswith("```"):
        parts = sql.split("```")
        if len(parts) >= 2:
            sql = parts[1]
            if sql.startswith("sql"):
                sql = sql[3:]
    sql = sql.strip().rstrip(";") + ";"

    retry_count = state.get("retry_count", 0) + 1 if error else 0
    return {"generated_sql": sql, "retry_count": retry_count}


def query_executor_node(state: AgentState) -> Dict[str, Any]:
    """Execute SQL against the real SQLite database."""
    sql = state.get("generated_sql", "")
    result = execute_query(sql)
    return {
        "query_error": result["error"],
        "query_results": result["results"],
    }


def response_formatter_node(state: AgentState) -> Dict[str, Any]:
    """Format results into natural language using Ollama."""
    question = state.get("user_question", "")
    sql = state.get("generated_sql", "")
    results = state.get("query_results")
    error = state.get("query_error")

    if error:
        response = f"I encountered an error while querying the database: {error}"
    elif results is None or len(results) == 0:
        prompt = FORMAT_PROMPT.format(
            question=question,
            sql=sql,
            results="[] (empty - no matching records found)"
        )
        response = llm.invoke(prompt).content.strip()
    else:
        prompt = FORMAT_PROMPT.format(
            question=question,
            sql=sql,
            results=str(results)
        )
        response = llm.invoke(prompt).content.strip()

    return {"final_response": response}


def fallback_node(state: AgentState) -> Dict[str, Any]:
    """Handle non-database questions."""
    return {
        "final_response": "I can only answer questions about customers, orders, products, inventory, and sales. Try asking something like 'Show me all customers in the USA' or 'Who spent the most?'"
    }


def email_node(state: AgentState) -> Dict[str, Any]:
    """Send query results via email if requested."""
    from src.tools.email_tools import send_email

    question = state.get("user_question", "")
    response = state.get("final_response", "")
    recipient = state.get("email_recipient", "wisdomcfriday1@gmail.com")

    subject = f"Query Results: {question[:50]}..."
    body = f"""Query: {question}

Results:
{response}

---
Sent by Text-to-SQL AI Agent
"""

    result = send_email(to_email=recipient, subject=subject, body=body)

    if result["success"]:
        return {"final_response": f"{response}\n\n📧 Results also emailed to {recipient}!"}
    else:
        return {"final_response": f"{response}\n\n⚠️ Failed to send email: {result['error']}"}