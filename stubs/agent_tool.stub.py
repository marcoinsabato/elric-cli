from typing import Any

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.ai.agents.base_agent import BaseAgent
from {{ llm_import }}


class {{ class_name }}(BaseAgent):
    """{{ class_name }} - Tool-using agent implementation."""

    def __init__(self, model: str = "{{ model_name }}", tools: list = None):
        super().__init__(name="{{ snake_name }}")
        self.llm = {{ llm_class }}(model=model)
        self.tools = tools or []
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant with access to tools. Use them when needed."),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        if self.tools:
            agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
            self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        else:
            self.agent_executor = None

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the tool agent logic.
        
        Args:
            input_data: Input data containing 'input' and optional 'tools'
            
        Returns:
            dict: Agent execution result with tool usage information
        """
        user_input = input_data.get("input", "")
        
        if not self.agent_executor:
            return {
                "status": "error",
                "message": "No tools configured for this agent",
                "model": self.llm.model_name
            }
        
        result = await self.agent_executor.ainvoke({"input": user_input})
        
        return {
            "status": "success",
            "response": result.get("output", ""),
            "model": self.llm.model_name,
            "tools_used": len(self.tools)
        }
    
    def add_tool(self, tool):
        """Add a tool to the agent."""
        self.tools.append(tool)
        # Recreate agent executor with new tools
        agent = create_tool_calling_agent(self.llm, self.tools, self.prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
