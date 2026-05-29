"""Agent API routes."""

from fastapi import APIRouter, Depends, Request
from rag_backend.presentation.schemas.agent_schemas import AgentQueryRequest, AgentQueryResponse

router = APIRouter(prefix="/api/v1/query/agent", tags=["Agent Query"])

def _get_agent_controller(request: Request):
    return request.app.state.agent_controller

@router.post("/", response_model=AgentQueryResponse)
async def query_agent(
    body: AgentQueryRequest,
    controller=Depends(_get_agent_controller),
):
    """Execute a Multi-Agent query and return the response."""
    return await controller.query_agent(body)
