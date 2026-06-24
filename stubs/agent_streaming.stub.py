from typing import Any, AsyncIterator

from langchain_core.prompts import ChatPromptTemplate

from app.ai.agents.base_agent import BaseAgent
from {{ llm_import }}


class {{ class_name }}(BaseAgent):
    """{{ class_name }} - Streaming agent for real-time responses."""

    def __init__(self, model: str = "{{ model_name }}"):
        super().__init__(name="{{ snake_name }}")
        self.llm = {{ llm_class }}(model=model, streaming=True)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant."),
            ("human", "{input}")
        ])
        
        self.chain = self.prompt | self.llm

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the agent logic with streaming disabled (use stream() for streaming).
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            dict: Agent execution result
        """
        user_input = input_data.get("input", "")
        
        response = await self.chain.ainvoke({"input": user_input})
        
        return {
            "status": "success",
            "response": response.content,
            "model": self.llm.model_name
        }
    
    async def stream(self, input_data: dict[str, Any]) -> AsyncIterator[str]:
        """
        Stream the agent response in real-time.
        
        Args:
            input_data: Input data containing 'input'
            
        Yields:
            str: Chunks of the response as they are generated
        """
        user_input = input_data.get("input", "")
        
        async for chunk in self.chain.astream({"input": user_input}):
            if hasattr(chunk, 'content'):
                yield chunk.content
            else:
                yield str(chunk)
