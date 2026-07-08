import React, { createContext, useContext, useState, useCallback, useRef, useEffect } from 'react';
import { Message, Conversation } from '../types';

import { chatService } from '../api/chatApi';

import { useAuth } from './AuthContext';

interface ReferencePanelState {
  isOpen: boolean;
  soKyHieu: string;
  targetId: string;
}

interface AppContextValue {


  // Conversations
  conversations: Conversation[];
  activeConversationId: string;
  setActiveConversationId: (id: string) => void;
  createConversation: (title: string) => Promise<string | null>;
  renameConversation: (id: string, title: string) => Promise<void>;
  deleteConversation: (id: string) => Promise<void>;
  conversationMessages: Record<string, Message[]>;

  // Chat
  messages: Message[];
  isAIThinking: boolean;
  thinkingConversationId: string | null;
  streamingMsgId: string | null;
  streamingContent: string;
  sendMessage: (content: string) => Promise<void>;



  // Layout
  sidebarCollapsed: boolean;
  setSidebarCollapsed: (collapsed: boolean) => void;
  toggleSidebar: () => void;

  // Reference Panel
  referencePanel: ReferencePanelState;
  openReference: (soKyHieu: string, targetId: string) => void;
  closeReference: () => void;

}

const AppContext = createContext<AppContextValue | null>(null);

export function AppProvider({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();


  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string>('');
  const [conversationMessages, setConversationMessages] = useState<Record<string, Message[]>>({});

  const [thinkingConversationId, setThinkingConversationId] = useState<string | null>(null);
  const isAIThinking = thinkingConversationId !== null;
  const [streamingMsgId, setStreamingMsgId] = useState<string | null>(null);
  const [streamingContent, setStreamingContent] = useState('');


  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const [referencePanel, setReferencePanel] = useState<ReferencePanelState>({ isOpen: false, soKyHieu: '', targetId: '' });

  const openReference = useCallback((soKyHieu: string, targetId: string) => {
    setReferencePanel({ isOpen: true, soKyHieu, targetId });
  }, []);

  const closeReference = useCallback(() => {
    setReferencePanel(prev => ({ ...prev, isOpen: false }));
  }, []);

  const messageIdCounter = useRef(100);

  const messages = conversationMessages[activeConversationId] ?? [];

  useEffect(() => {
    if (!isAuthenticated) return;

    const fetchInitialData = async () => {
      try {
        const [conversationsData] = await Promise.all([
          chatService.getConversations().catch(() => [])
        ]);

        if (conversationsData.length > 0) {
          setConversations(conversationsData);
          setActiveConversationId(prev => prev ? prev : '');
        }
      } catch (e) {
        console.error("Failed to load initial data", e);
      }
    };

    fetchInitialData();
  }, [isAuthenticated]);

  useEffect(() => {
    if (activeConversationId && !conversationMessages[activeConversationId]) {
      chatService.getMessages(activeConversationId)
        .then(msgs => setConversationMessages(prev => ({ ...prev, [activeConversationId]: msgs })))
        .catch(() => setConversationMessages(prev => ({ ...prev, [activeConversationId]: [] })));
    }
  }, [activeConversationId, conversationMessages]);

  useEffect(() => {
    closeReference();
  }, [activeConversationId, closeReference]);


  const createConversation = useCallback(async (title: string) => {
    try {
      const newNb = await chatService.createConversation(title);
      setConversations(prev => [...prev, newNb]);
      setConversationMessages(prev => ({ ...prev, [newNb.id]: [] }));
      setActiveConversationId(newNb.id);
      return newNb.id;
    } catch (e) {
      console.error(e);
      return null;
    }
  }, []);

  const renameConversation = useCallback(async (id: string, title: string) => {
    try {
      const updated = await chatService.updateConversation(id, title);
      setConversations(prev => prev.map(nb => nb.id === id ? updated : nb));
    } catch (e) {
      console.error(e);
    }
  }, []);

  const deleteConversation = useCallback(async (id: string) => {
    try {
      await chatService.deleteConversation(id);
      setConversations(prev => {
        const remaining = prev.filter(nb => nb.id !== id);
        return remaining;
      });
      setConversationMessages(prev => {
        const next = { ...prev };
        delete next[id];
        return next;
      });
      setActiveConversationId(prev => {
        if (prev !== id) return prev;
        const remaining = conversations.filter(nb => nb.id !== id);
        return remaining.length > 0 ? remaining[0].id : '';
      });
    } catch (e) {
      console.error(e);
    }
  }, [conversations]);

  const sendMessage = useCallback(
    async (content: string) => {
      let targetNbId = activeConversationId;

      if (!targetNbId) {
        try {
          const words = content.trim().split(/\s+/);
          const shortTitle = words.slice(0, 6).join(' ') + (words.length > 6 ? '...' : '');
          const newNb = await chatService.createConversation(shortTitle);
          setConversations(prev => [...prev, newNb]);
          setConversationMessages(prev => ({ ...prev, [newNb.id]: [] }));
          setActiveConversationId(newNb.id);
          targetNbId = newNb.id;
        } catch (e) {
          console.error("Failed to auto-create conversation", e);
          return;
        }
      } else {
        const existingMessages = conversationMessages[targetNbId] || [];
        if (existingMessages.length === 0) {
          const words = content.trim().split(/\s+/);
          const shortTitle = words.slice(0, 6).join(' ') + (words.length > 6 ? '...' : '');

          chatService.updateConversation(targetNbId, shortTitle).then(updated => {
            setConversations(prev => prev.map(nb => nb.id === targetNbId ? updated : nb));
          }).catch(err => console.error("Lỗi khi update tên trên backend:", err));
        }
      }

      const userMsg: Message = {
        id: `msg-temp-${++messageIdCounter.current}`,
        role: 'user',
        content,
        timestamp: new Date().toISOString(),
      };

      setConversationMessages(prev => ({
        ...prev,
        [targetNbId]: [...(prev[targetNbId] ?? []), userMsg],
      }));
      setConversations(prev =>
        prev.map(nb => nb.id === targetNbId ? { ...nb, messageCount: nb.messageCount + 1 } : nb)
      );

      setThinkingConversationId(targetNbId);

      try {
        const responseMsg = await chatService.sendMessage(targetNbId, content);

        setThinkingConversationId(null);
        const uiAiMsg = { ...responseMsg, isStreaming: true };
        setConversationMessages(prev => ({
          ...prev,
          [targetNbId]: [...(prev[targetNbId] ?? []), uiAiMsg],
        }));


        setStreamingMsgId(responseMsg.id);
        setStreamingContent('');
        let idx = 0;
        const fullContent = responseMsg.content || '';
        const speed = 18;
        const charsPerTick = 4;

        const interval = setInterval(() => {
          idx += charsPerTick;
          setStreamingContent(fullContent.slice(0, idx));
          if (idx >= fullContent.length) {
            clearInterval(interval);
            setStreamingMsgId(null);
            setStreamingContent('');
            setConversationMessages(prev => ({
              ...prev,
              [targetNbId]: (prev[targetNbId] ?? []).map(m =>
                m.id === responseMsg.id ? { ...m, isStreaming: false } : m
              ),
            }));
          }
        }, speed);

      } catch (e) {
        console.error("Lỗi khi gửi tin nhắn", e);
        setThinkingConversationId(null);
      }
    },
    [activeConversationId]
  );

  const toggleSidebar = useCallback(() => setSidebarCollapsed(p => !p), []);


  return (
    <AppContext.Provider
      value={{

        conversations,
        activeConversationId,
        setActiveConversationId,
        createConversation,
        renameConversation,
        deleteConversation,
        conversationMessages,
        messages,
        isAIThinking,
        thinkingConversationId,
        streamingMsgId,
        streamingContent,
        sendMessage,

        sidebarCollapsed,
        setSidebarCollapsed,
        toggleSidebar,

        referencePanel,
        openReference,
        closeReference,

      }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be used within AppProvider');
  return ctx;
}
