import streamlit as st
from src.agent.graph import graph
from src.agent.state import AgentState

# Page config
st.set_page_config(page_title="Text-to-SQL AI Agent", page_icon="🤖")
st.title("🤖 Text-to-SQL AI Agent")
st.caption("Ask questions about your e-commerce database in plain English")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about your database..."):

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            # Build state with all required fields
            state: AgentState = {
                "messages": [],
                "user_question": prompt,
                "is_db_related": None,
                "generated_sql": None,
                "query_results": None,
                "query_error": None,
                "final_response": None,
                "retry_count": 0,
                "max_retries": 3,
                "should_send_email": None,
                "email_recipient": None,
                "email_subject": None,
                "email_body": None,
            }

            result = graph.invoke(state)
            response = result.get("final_response", "No response generated.")

            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        # Show generated SQL in expandable section
        if result.get("generated_sql"):
            with st.expander("🔍 View Generated SQL"):
                st.code(result["generated_sql"], language="sql")

        # Show error if any
        if result.get("query_error"):
            with st.expander("⚠️ Query Error"):
                st.error(result["query_error"])

# Sidebar with info
with st.sidebar:
    st.header("About")
    st.write("""
    This AI agent translates natural language questions into SQL queries.
    
    **Capabilities:**
    - Query customers, orders, products
    - Find top spenders
    - Check inventory levels
    - Filter by country, status, date
    - Email reports (if configured)
    
    **Tech Stack:**
    - LangGraph (orchestration)
    - Ollama + Llama 3.2 (LLM)
    - SQLite (database)
    - Streamlit (UI)
    """)

    st.divider()
    st.caption("Built with LangGraph + Ollama + SQLite")