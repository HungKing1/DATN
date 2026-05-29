import { fetchApi } from './apiClient';
import { Notebook, Message, QueryMode } from '../types';

export const chatService = {
  // Notebook operations
  getNotebooks: () => fetchApi<Notebook[]>('/notebooks'),

  createNotebook: (title: string, emoji: string) =>
    fetchApi<Notebook>('/notebooks', {
      method: 'POST',
      body: JSON.stringify({ title, emoji })
    }),

  updateNotebook: (id: string, title: string) =>
    fetchApi<Notebook>(`/notebooks/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ title })
    }),

  deleteNotebook: (id: string) =>
    fetchApi<void>(`/notebooks/${id}`, {
      method: 'DELETE'
    }),

  // Chat/Messages operations
  getMessages: (notebookId: string) =>
    fetchApi<Message[]>(`/notebooks/${notebookId}/messages`),

  /**
   * Send a message with an explicit query mode.
   * @param notebookId - active notebook
   * @param content    - user message text
   * @param mode       - 'quick' → standard RAG | 'agent' → Multi-Agent LangGraph
   */
  sendMessage: (notebookId: string, content: string, mode: QueryMode = 'quick') =>
    fetchApi<Message>('/chat', {
      method: 'POST',
      body: JSON.stringify({ notebookId, content, mode })
    }),

  // Có thể dùng endpoint này để clear tin nhắn của 1 notebook bên trong DB
  clearChat: (notebookId: string) =>
    fetchApi<void>(`/notebooks/${notebookId}/messages`, {
      method: 'DELETE'
    })
};
