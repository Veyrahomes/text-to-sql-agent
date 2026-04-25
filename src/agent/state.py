"""LangGraph state definition for the Text-to-SQL agent."""
from typing import TypedDict, List, Optional, Annotated, Any
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_question: str
    is_db_related: Optional[bool]
    generated_sql: Optional[str]
    query_results: Optional[List[Any]]
    query_error: Optional[str]
    final_response: Optional[str]
    retry_count: int
    max_retries: int
    should_send_email: Optional[bool]
    email_recipient: Optional[str]
    email_subject: Optional[str]
    email_body: Optional[str]