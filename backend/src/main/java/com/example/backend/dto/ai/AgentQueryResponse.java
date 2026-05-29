package com.example.backend.dto.ai;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

/**
 * Maps to AI Server's AgentQueryResponse (Python Pydantic) — agent_schemas.py.
 *
 * Returned by POST /api/v1/query/agent/
 *
 * Fields MUST match AI Server:
 *   answer             : str
 *   todos_executed     : list[dict]
 *   research_findings  : list[dict]
 *   iterations         : int
 *   laws_consulted     : list[str]
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AgentQueryResponse {

    /** Final synthesized answer from the Master Lawyer Agent. */
    private String answer;

    /** List of TODO tasks the Master agent planned and executed. */
    @JsonProperty("todos_executed")
    private List<Map<String, Object>> todosExecuted;

    /** Raw findings collected by each Paralegal Agent (verbatim law text). */
    @JsonProperty("research_findings")
    private List<Map<String, Object>> researchFindings;

    /** Total number of agent iterations executed. */
    private int iterations;

    /** List of law UUIDs that were consulted during the query. */
    @JsonProperty("laws_consulted")
    private List<String> lawsConsulted;
}

