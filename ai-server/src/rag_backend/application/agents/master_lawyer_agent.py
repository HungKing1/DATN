"""Master Lawyer Agent Node."""

from langchain_core.messages import SystemMessage
from rag_backend.domain.models.agent_state import DeepAgentState


class MasterLawyerAgent:
    def __init__(self, llm_provider, prompt_manager):
        self._llm = llm_provider.get_underlying_model()
        self._prompt_manager = prompt_manager
        
        from rag_backend.application.agents.agent_tools import (
            write_todos, read_todos, delegate_task, read_research_findings
        )
        self._tools = [write_todos, read_todos, delegate_task, read_research_findings]
        self._model_with_tools = self._llm.bind_tools(self._tools)

    async def run(self, state: DeepAgentState) -> dict:
        """Execute the master lawyer node."""
        system_prompt = self._prompt_manager.get_prompt("master_lawyer_system")
        
        # Only inject the system prompt at the beginning
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        
        response = await self._model_with_tools.ainvoke(messages)
        
        return {
            "messages": [response],
            "iteration_count": state["iteration_count"] + 1
        }
