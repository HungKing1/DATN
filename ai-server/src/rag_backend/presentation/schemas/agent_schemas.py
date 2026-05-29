"""Schemas for Agent API."""

from pydantic import BaseModel, Field


class AgentQueryRequest(BaseModel):
    """Request schema for Agent query."""

    question: str = Field(..., description="User's legal question.")
    max_iterations: int = Field(5, description="Maximum iterations for the master agent.")
    max_search_per_paralegal: int = Field(3, description="Maximum search iterations per paralegal.")


class AgentQueryResponse(BaseModel):
    """Response schema for Agent query."""

    answer: str
    todos_executed: list[dict]
    research_findings: list[dict]
    iterations: int
    laws_consulted: list[str] = Field(default_factory=list)
