"""Ollama LLM integration for the Text-to-SQL agent."""
from langchain_ollama import ChatOllama
from src.tools.db_tools import get_schema_info


def create_llm(model: str = "llama3.2", temperature: float = 0.0):
    """Create a ChatOllama instance."""
    return ChatOllama(model=model, temperature=temperature)


def get_schema_info_str() -> str:
    """Get database schema as a string for prompts."""
    return get_schema_info()


SQL_PROMPT = """You are a SQL expert. Given this SQLite database schema:

{schema}

Generate a SELECT query to answer: "{question}"

Rules:
- Only SELECT queries
- No DELETE, INSERT, UPDATE, DROP
- Return ONLY the SQL, no explanation
- End with semicolon
- Include ALL relevant columns the user might want to see (not just one)
- For stock/inventory questions, use stock_quantity < 50 as "low stock"
- Use meaningful column aliases where helpful

SQL:"""


FORMAT_PROMPT = """Question: {question}
SQL: {sql}
Results: {results}

Write a friendly response that directly answers the question using the actual data.
If results are empty, say so clearly and suggest what might be available instead.
Mention specific names, numbers, and details from the results.
Do NOT include the SQL in your response."""