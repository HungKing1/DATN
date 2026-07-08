package com.example.backend.service.impl;

import com.example.backend.dto.ai.AgentQueryRequest;
import com.example.backend.dto.ai.AgentQueryResponse;
import com.example.backend.dto.request.ChatRequest;
import com.example.backend.entity.Message;
import com.example.backend.entity.Conversation;
import com.example.backend.repository.MessageRepository;
import com.example.backend.repository.ConversationRepository;
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
    private final ConversationRepository conversationRepository;
    private final AiServerClient aiServerClient;

    @Override
    public Message processChat(String userId, ChatRequest request) {
        String conversationId = request.getConversationId();
        Conversation conversation;

        if (conversationId == null || conversationId.isEmpty()) {
            conversation = Conversation.builder()
                    .userId(userId)
                    .title("New Chat")
                    .build();
            conversation = conversationRepository.save(conversation);
            conversationId = conversation.getId();
        } else {
            conversation = conversationRepository.findById(conversationId)
                    .orElseThrow(() -> new IllegalArgumentException("Conversation not found"));
        }

        Message userMessage = Message.builder()
                .conversationId(conversationId)
                .role("user")
                .content(request.getContent())
                .build();
        messageRepository.save(userMessage);

        Message aiMessage = processAgentQuery(conversationId, request.getContent());

        aiMessage = messageRepository.save(aiMessage);
        Conversation latestConversation = conversationRepository.findById(conversationId)
                .orElseThrow(() -> new IllegalArgumentException("Conversation not found"));
        latestConversation.setMessageCount(latestConversation.getMessageCount() + 2);
        conversationRepository.save(latestConversation);

        return aiMessage;
    }

    private Message processAgentQuery(String conversationId, String content) {
        try {
            AgentQueryRequest agentRequest = AgentQueryRequest.builder()
                    .question(content)
                    .build();

            AgentQueryResponse agentResponse = aiServerClient.agentQuery(agentRequest);

            log.info("Multi-Agent RAG response generated for conversation: {}, iterations: {}",
                    conversationId, agentResponse != null ? agentResponse.getIterations() : 0);

            String answer = agentResponse != null ? agentResponse.getAnswer() : null;
            if (answer == null || answer.isBlank()) {
                answer = "Không tìm thấy thông tin phù hợp trong cơ sở dữ liệu luật.";
            }

            return Message.builder()
                    .conversationId(conversationId)
                    .role("ai")
                    .content(answer)

                    .build();

        } catch (Exception e) {
            log.error("AI Server unavailable (agent mode), returning fallback: {}", e.getMessage());
            return buildFallbackMessage(conversationId, content);
        }
    }

    private Message buildFallbackMessage(String conversationId, String content) {
        return Message.builder()
                .conversationId(conversationId)
                .role("ai")
                .content("⚠️ Hệ thống AI tạm thời không khả dụng. Vui lòng thử lại sau.\n\n"
                        + "Câu hỏi của bạn: \"" + content + "\"")

                .build();
    }
}
