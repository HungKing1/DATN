import logging
from fastapi import HTTPException

from rag_backend.presentation.schemas.agent_schemas import AgentQueryRequest, AgentQueryResponse
from rag_backend.application.services.multi_agent_service import MultiAgentService

logger = logging.getLogger(__name__)

class AgentController:
    def __init__(self, multi_agent_service: MultiAgentService):
        self._multi_agent_service = multi_agent_service

    async def query_agent(self, body: AgentQueryRequest) -> AgentQueryResponse:
        try:
            result = await self._multi_agent_service.run(
                question=body.question
            )
            
            laws_consulted = set()
            for finding in result.get("research_findings", []):
                if finding.get("law_uuid"):
                    laws_consulted.add(finding["law_uuid"])
            
            return AgentQueryResponse(
                answer=result["answer"],
                todos_executed=result.get("todos_executed", []),
                research_findings=result.get("research_findings", []),
                iterations=result.get("iterations", 0),
                laws_consulted=list(laws_consulted)
            )
        except Exception as e:
            logger.error("Agent query failed: %s", e, exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))
