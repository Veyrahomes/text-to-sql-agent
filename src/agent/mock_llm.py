"""Mock LLM for testing without Ollama."""
from typing import List, Optional
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.outputs import ChatGeneration, ChatResult

class MockChatModel(BaseChatModel):
    def _generate(self, messages: List[BaseMessage], stop: Optional[List[str]] = None, **kwargs) -> ChatResult:
        last = messages[-1].content.lower()
        db_keywords = ["customer", "order", "product", "sale", "revenue", "inventory", "stock", "spend"]
        if any(kw in last for kw in db_keywords):
            text = "YES"
        else:
            text = "NO"
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text))])
    @property
    def _llm_type(self) -> str:
        return "mock-chat-model"