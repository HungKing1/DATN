package com.example.backend.dto.ai;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AgentQueryResponse {

    private String answer;

    @JsonProperty("todos_executed")
    private List<Map<String, Object>> todosExecuted;

    @JsonProperty("research_findings")
    private List<Map<String, Object>> researchFindings;

    private int iterations;
    @JsonProperty("laws_consulted")
    private List<String> lawsConsulted;
}
