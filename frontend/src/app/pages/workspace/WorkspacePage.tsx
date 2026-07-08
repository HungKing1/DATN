import { useEffect } from 'react';
import { useSearchParams } from 'react-router';
import { useApp } from '../../context/AppContext';
import { ChatPanel } from '../../components/ChatPanel';

export function WorkspacePage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const { activeConversationId, setActiveConversationId, conversations } = useApp();
  const chatId = searchParams.get('c');

  useEffect(() => {
    if (chatId && chatId !== activeConversationId) {
      const exists = conversations.some(c => c.id === chatId);
      if (exists) {
        setActiveConversationId(chatId);
      } else if (conversations.length > 0) {
        if (activeConversationId) {
          setSearchParams({ c: activeConversationId }, { replace: true });
        } else {
          setSearchParams({}, { replace: true });
        }
      } else {
        setActiveConversationId(chatId);
      }
    } else if (activeConversationId && activeConversationId !== chatId) {
      setSearchParams({ c: activeConversationId }, { replace: true });
    } else if (!chatId && !activeConversationId && conversations.length > 0) {
      if (searchParams.has('c')) {
        setSearchParams({}, { replace: true });
      }
    }
  }, [chatId, activeConversationId, setActiveConversationId, setSearchParams, conversations, searchParams]);

  return (
    <div className="flex flex-col h-full">

      <div className="flex-1 overflow-hidden">
        <ChatPanel />
      </div>
    </div>
  );
}
