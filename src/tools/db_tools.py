"""SQLite database tools for the Text-to-SQL agent."""
import sqlite3
from typing import Dict, Any


def execute_query(sql_query: str, db_path: str = "data/ecommerce.db") -> Dict[str, Any]:
    """
    Execute a SQL query against the SQLite database.
    Only allows SELECT queries for safety.
    """
    cleaned = sql_query.strip()
    first_word = cleaned.split()[0].upper() if cleaned else ""

    if first_word in ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]:
        return {
            "results": None,
            "error": f"Query type '{first_word}' is not permitted. Only SELECT queries allowed."
        }

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(cleaned)
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return {"results": rows, "error": None}
    except sqlite3.Error as e:
        return {"results": None, "error": str(e)}
    except Exception as e:
        return {"results": None, "error": f"Unexpected error: {str(e)}"}


def get_schema_info(db_path: str = "data/ecommerce.db") -> str:
    """Get database schema for LLM prompts."""
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    tables = cursor.fetchall()
    conn.close()
    return "\n\n".join([t[0] + ";" for t in tables if t[0]])