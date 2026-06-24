from typing import Any

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.ai.agents.base_agent import BaseAgent
from {{ llm_import }}


class {{ class_name }}(BaseAgent):
    """{{ class_name }} - Chat agent with conversation memory."""

    def __init__(self, model: str = "{{ model_name }}", system_prompt: str = "You are a helpful AI assistant."):
        super().__init__(name="{{ snake_name }}")
        self.llm = {{ llm_class }}(model=model)
        self.system_prompt = system_prompt
        self.chat_history: list = []
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_prompt}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        self.chain = self.prompt | self.llm

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the chat agent logic with conversation memory.
        
        Args:
            input_data: Input data containing 'message' and optional 'clear_history'
            
        Returns:
            dict: Agent execution result with response and chat history
        """
        message = input_data.get("message", "")
        clear_history = input_data.get("clear_history", False)
        
        if clear_history:
            self.chat_history = []
        
        response = await self.chain.ainvoke({
            "system_prompt": self.system_prompt,
            "chat_history": self.chat_history,
            "input": message
        })
        
        # Update chat history
        self.chat_history.append(HumanMessage(content=message))
        self.chat_history.append(AIMessage(content=response.content))
        
        return {
            "status": "success",
            "response": response.content,
            "model": self.llm.model_name,
            "history_length": len(self.chat_history)
        }
    
    def clear_history(self):
        """Clear the conversation history."""
        self.chat_history = []
