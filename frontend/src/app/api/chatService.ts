import { fetchApi } from './apiClient';
import { Conversation, Message } from '../types';

export const chatService = {
  // Conversation operations
  getConversations: () => fetchApi<Conversation[]>('/conversations'),

  createConversation: (title: string) =>
    fetchApi<Conversation>('/conversations', {
      method: 'POST',
      body: JSON.stringify({ title })
    }),

  updateConversation: (id: string, title: string) =>
    fetchApi<Conversation>(`/conversations/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ title })
    }),

  deleteConversation: (id: string) =>
    fetchApi<void>(`/conversations/${id}`, {
      method: 'DELETE'
    }),

  // Chat/Messages operations
  getMessages: (conversationId: string) =>
    fetchApi<Message[]>(`/conversations/${conversationId}/messages`),

  /**
   * Send a message to Multi-Agent LangGraph pipeline.
   * @param conversationId - active conversation
   * @param content    - user message text
   */
  sendMessage: (conversationId: string, content: string) =>
    fetchApi<Message>('/chat', {
      method: 'POST',
      body: JSON.stringify({ conversationId, content })
    })
};
