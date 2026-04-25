# 🤖 Text-to-SQL AI Agent

A production-grade AI agent that translates natural language into SQL queries using **LangGraph** orchestration, **Ollama** (Llama 3.2), and **SQLite**.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.1.9-green.svg)](https://langchain.com/langgraph)
[![Ollama](https://img.shields.io/badge/Ollama-Llama%203.2-orange.svg)](https://ollama.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Features

- **Natural Language to SQL** – Ask business questions in plain English
- **Self-Correcting Queries** – Automatically retries failed queries up to 3 times
- **Query Safety** – Blocks dangerous operations (DELETE, DROP, UPDATE, INSERT)
- **Real Database Queries** – Connected to a live SQLite e-commerce database
- **LLM-Powered Responses** – Natural language answers formatted by Ollama
- **Email Automation** – Send query results directly to your inbox
- **Chat Interface** – Clean Streamlit UI for interactive querying
- **Conversation State** – LangGraph manages multi-step workflows

---

## 🏗️ Architecture
---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Orchestration** | LangGraph (StateGraph with conditional edges) |
| **LLM** | Ollama + Llama 3.2 (3B parameters) |
| **Database** | SQLite (e-commerce schema with 5 tables) |
| **UI** | Streamlit (chat-based interface) |
| **Email** | SMTP (Gmail integration) |
| **Language** | Python 3.12 |

---

## 📂 Project Structure
---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+** – [Download](https://www.python.org/downloads/)
- **Ollama** – [Download](https://ollama.ai/download)
- **Git** – [Download](https://git-scm.com/downloads)

### 1. Clone the Repository

```bash
git clone https://github.com/Veyrahomes/text-to-sql-agent.git
cd text-to-sql-agent