package com.example.backend.dto.ai;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Maps to AI Server's AgentQueryRequest (Python Pydantic) — agent_schemas.py.
 *
 * Sent to POST /api/v1/query/agent/ — triggers Multi-Agent LangGraph pipeline.
 *
 * Fields MUST match AI Server:
 * question : str (NOT "query"!)
 * max_iterations : int (default 5)
 * max_search_per_paralegal : int (default 3)
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AgentQueryRequest {

    /** The user's natural-language legal question. AI Server field: "question" */
    private String question;

    /**
     * Maximum iterations for the master agent. AI Server field: "max_iterations"
     */
    @Builder.Default
    @JsonProperty("max_iterations")
    private int maxIterations = 5;

    /**
     * Maximum search iterations per paralegal agent. AI Server field:
     * "max_search_per_paralegal"
     */
    @Builder.Default
    @JsonProperty("max_search_per_paralegal")
    private int maxSearchPerParalegal = 3;
}