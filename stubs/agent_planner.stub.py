from typing import Any

from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate

from app.ai.agents.base_agent import BaseAgent
from {{ llm_import }}


class {{ class_name }}(BaseAgent):
    """{{ class_name }} - Planner agent for complex task decomposition."""

    def __init__(self, model: str = "{{ model_name }}"):
        super().__init__(name="{{ snake_name }}")
        self.llm = {{ llm_class }}(model=model, temperature=0.7)
        
        # Planning prompt
        self.planning_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert task planner. Break down complex tasks into clear, actionable steps.
For each step, provide:
1. Step number
2. Action to take
3. Expected outcome
4. Dependencies (if any)

Format your response as a structured plan."""),
            ("human", "Task: {task}\n\nCreate a detailed plan to accomplish this task.")
        ])
        
        # Execution prompt
        self.execution_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are executing step {step_number} of a plan: {step_description}"),
            ("human", "{input}")
        ])
        
        self.planning_chain = self.planning_prompt | self.llm
        self.execution_chain = self.execution_prompt | self.llm

    async def run(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the planner agent logic.
        
        Args:
            input_data: Input data containing 'task' and optional 'execute_plan'
            
        Returns:
            dict: Agent execution result with plan and optional execution results
        """
        task = input_data.get("task", "")
        execute_plan = input_data.get("execute_plan", False)
        
        # Generate plan
        plan_response = await self.planning_chain.ainvoke({"task": task})
        plan = plan_response.content
        
        result = {
            "status": "success",
            "plan": plan,
            "model": self.llm.model_name,
            "task": task
        }
        
        # Optionally execute the plan
        if execute_plan:
            execution_results = []
            # TODO: Parse plan and execute each step
            # This is a placeholder for plan execution logic
            result["execution_results"] = execution_results
            result["executed"] = True
        else:
            result["executed"] = False
        
        return result
    
    async def execute_step(self, step_number: int, step_description: str, input_data: str) -> str:
        """Execute a single step of the plan."""
        response = await self.execution_chain.ainvoke({
            "step_number": step_number,
            "step_description": step_description,
            "input": input_data
        })
        return response.content
