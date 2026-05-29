package com.example.backend.service.impl;

import com.example.backend.dto.ai.AgentQueryRequest;
import com.example.backend.dto.ai.AgentQueryResponse;
import com.example.backend.dto.ai.RAGQueryRequest;
import com.example.backend.dto.ai.RAGResponse;
import com.example.backend.dto.request.ChatRequest;
import com.example.backend.entity.Message;
import com.example.backend.entity.Notebook;
import com.example.backend.repository.MessageRepository;
import com.example.backend.repository.NotebookRepository;
import com.example.backend.service.AiServerClient;
import com.example.backend.service.ChatService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class ChatServiceImpl implements ChatService {

    private final MessageRepository messageRepository;
    private final NotebookRepository notebookRepository;
    private final AiServerClient aiServerClient;

    @Override
    public Message processChat(String userId, ChatRequest request) {
        String notebookId = request.getNotebookId();
        Notebook notebook;

        if (notebookId == null || notebookId.isEmpty()) {
            notebook = Notebook.builder()
                    .userId(userId)
                    .title("New Chat")
                    .build();
            notebook = notebookRepository.save(notebook);
            notebookId = notebook.getId();
        } else {
            notebook = notebookRepository.findById(notebookId)
                    .orElseThrow(() -> new IllegalArgumentException("Notebook not found"));
        }

        // Save User Message
        Message userMessage = Message.builder()
                .notebookId(notebookId)
                .role("user")
                .content(request.getContent())
                .build();
        messageRepository.save(userMessage);

        // Route to correct AI Server pipeline based on mode
        boolean isAgentMode = "agent".equalsIgnoreCase(request.getMode());
        Message aiMessage = isAgentMode
                ? processAgentQuery(notebookId, request.getContent())
                : processQuickQuery(notebookId, request.getContent());

        aiMessage = messageRepository.save(aiMessage);

        // Update Notebook message count
        notebook.setMessageCount(notebook.getMessageCount() + 2);
        notebookRepository.save(notebook);

        return aiMessage;
    }

    // ─────────────────────────────────────────────────────────────
    // PRIVATE HELPERS
    // ─────────────────────────────────────────────────────────────

    /**
     * Standard RAG pipeline — calls POST /api/v1/query/ on AI Server.
     * Fast response: Query Rewrite → Hybrid Search → Rerank → LLM Generate.
     */
    private Message processQuickQuery(String notebookId, String content) {
        try {
            RAGQueryRequest ragRequest = RAGQueryRequest.builder()
                    .query(content)
                    .useReranker(true)
                    .useQueryRewrite(true)
                    .build();

            RAGResponse ragResponse = aiServerClient.query(ragRequest);

            List<Message.Citation> citations = ragResponse.getCitations() != null
                    ? ragResponse.getCitations().stream()
                        .map(c -> Message.Citation.builder()
                                .lawName(c.getSource())
                                .text(c.getContentSnippet())
                                .similarityScore(c.getRelevanceScore())
                                .build())
                        .collect(Collectors.toList())
                    : List.of();

            Double confidence = ragResponse.getCitations() != null && !ragResponse.getCitations().isEmpty()
                    ? ragResponse.getCitations().stream()
                        .mapToDouble(RAGResponse.RAGCitation::getRelevanceScore)
                        .average()
                        .orElse(0.0)
                    : null;

            log.info("Quick RAG response generated for notebook: {}", notebookId);
            return Message.builder()
                    .notebookId(notebookId)
                    .role("ai")
                    .content(ragResponse.getAnswer())
                    .citations(citations)
                    .confidence(confidence)
                    .suggestedQuestions(List.of(
                            "Bạn có thể giải thích thêm không?",
                            "Có điều luật nào liên quan khác không?"))
                    .build();

        } catch (Exception e) {
            log.error("AI Server unavailable (quick mode), returning fallback: {}", e.getMessage());
            return buildFallbackMessage(notebookId, content);
        }
    }

    /**
     * Multi-Agent RAG pipeline — calls POST /api/v1/query/agent on AI Server.
     * Deep reasoning: MasterLawyerAgent → parallel ParalegalAgents → synthesize.
     */
    private Message processAgentQuery(String notebookId, String content) {
        try {
            AgentQueryRequest agentRequest = AgentQueryRequest.builder()
                    .question(content)   // AI Server field is "question", not "query"
                    .build();

            AgentQueryResponse agentResponse = aiServerClient.agentQuery(agentRequest);

            log.info("Multi-Agent RAG response generated for notebook: {}, iterations: {}",
                    notebookId, agentResponse != null ? agentResponse.getIterations() : 0);

            String answer = agentResponse != null ? agentResponse.getAnswer() : null;
            if (answer == null || answer.isBlank()) {
                answer = "Không tìm thấy thông tin phù hợp trong cơ sở dữ liệu luật.";
            }

            return Message.builder()
                    .notebookId(notebookId)
                    .role("ai")
                    .content(answer)
                    .citations(List.of()) // Agent mode trả về raw text, không có structured citations
                    .confidence(null)
                    .suggestedQuestions(List.of(
                            "Phân tích thêm chi tiết điều luật này?",
                            "Có trường hợp ngoại lệ nào không?",
                            "Mức xử phạt cụ thể là gì?"))
                    .build();

        } catch (Exception e) {
            log.error("AI Server unavailable (agent mode), returning fallback: {}", e.getMessage());
            return buildFallbackMessage(notebookId, content);
        }
    }

    private Message buildFallbackMessage(String notebookId, String content) {
        return Message.builder()
                .notebookId(notebookId)
                .role("ai")
                .content("⚠️ Hệ thống AI tạm thời không khả dụng. Vui lòng thử lại sau.\n\n"
                        + "Câu hỏi của bạn: \"" + content + "\"")
                .confidence(0.0)
                .suggestedQuestions(List.of("Thử lại câu hỏi"))
                .build();
    }
}

