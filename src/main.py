"""Main entry point for the Text-to-SQL agent."""
from src.agent.graph import graph
from src.agent.state import AgentState

def ask_question(question: str):
    print(f"\n{'='*50}\nUser: {question}\n{'='*50}")
    initial_state: AgentState = {
        "messages": [], "user_question": question, "is_db_related": None,
        "generated_sql": None, "query_results": None, "query_error": None,
        "final_response": None, "retry_count": 0, "max_retries": 3,
        "should_send_email": None, "email_recipient": None,
        "email_subject": None, "email_body": None,
    }
    result = graph.invoke(initial_state)
    if result.get("generated_sql"):
        print(f"\nSQL: {result['generated_sql']}")
    print(f"\nResponse: {result.get('final_response')}")
    return result

if __name__ == "__main__":
    print("TEXT-TO-SQL AI AGENT - Mock Mode\n")
    ask_question("Show me all customers in the USA")
    ask_question("Who spent the most?")
    ask_question("What is the weather?")
    print("\nDone!")