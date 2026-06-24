from typing import Any

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

from app.ai.agents.base_agent import BaseAgent
from {{ llm_import }}


class {{ class_name }}(BaseAgent):
    """{{ class_name }} - ReAct (Reasoning + Acting) agent implementation."""

    def __init__(self, model: str = "{{ model_name }}", tools: list = None):
        super().__init__(name="{{ snake_name }}")
        self.llm = {{ llm_class }}(model=model)
        self.tools = tools or []
        
        # ReAct prompt template
        self.prompt = PromptTemplate.from_template(
            """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
        )
        
        if self.tools:
            agent = create_react_agent(self.llm, self.tools, self.prompt)
            self.agent_executor = AgentExecutor(
                agent=agent, 
                tools=self.tools, 
                verbose=True,
                max_iterations=5,
                handle_parsing_errors=True
            )
        else:
            self.agent_executor = None

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the ReAct agent logic with reasoning and acting.
        
        Args:
            input_data: Input data containing 'input' and optional 'max_iterations'
            
        Returns:
            dict: Agent execution result with reasoning steps
        """
        user_input = input_data.get("input", "")
        max_iterations = input_data.get("max_iterations", 5)
        
        if not self.agent_executor:
            return {
                "status": "error",
                "message": "No tools configured for this ReAct agent",
                "model": self.llm.model_name
            }
        
        self.agent_executor.max_iterations = max_iterations
        
        result = await self.agent_executor.ainvoke({"input": user_input})
        
        return {
            "status": "success",
            "response": result.get("output", ""),
            "model": self.llm.model_name,
            "tools_available": len(self.tools),
            "reasoning_steps": result.get("intermediate_steps", [])
        }
