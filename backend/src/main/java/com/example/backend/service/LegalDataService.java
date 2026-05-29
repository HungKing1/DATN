package com.example.backend.service;

import com.example.backend.entity.Clause;
import com.example.backend.entity.Law;
import com.example.backend.entity.LegalTopic;
import com.example.backend.dto.response.legal.LegalDocumentSummaryResponse;
import com.example.backend.dto.response.legal.LegalDocumentDetailResponse;
import org.springframework.data.domain.Page;

import java.util.List;

public interface LegalDataService {
    List<Law> getLaws();
    List<LegalTopic> getTopics();
    List<Clause> getClausesByLaw(String lawId);
    Clause getClause(String id);

    Page<LegalDocumentSummaryResponse> getDocumentList(int page, int size);
    Page<LegalDocumentSummaryResponse> searchDocuments(String keyword, int page, int size);
    LegalDocumentDetailResponse getDocumentDetail(String soKyHieu);
}
