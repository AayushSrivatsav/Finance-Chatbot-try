import { useState, useCallback, useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import toast from 'react-hot-toast';

// API
import { sendChatMessage, getChatHistory, clearChatHistory } from '../api/chatApi';

export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [sources, setSources] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const queryClient = useQueryClient();
  const conversationIdRef = useRef(null);

  // Get chat history
  const { data: chatHistory, isLoading: historyLoading } = useQuery(
    ['chatHistory', conversationIdRef.current],
    () => getChatHistory(conversationIdRef.current),
    {
      enabled: !!conversationIdRef.current,
      onSuccess: (data) => {
        if (data?.messages) {
          setMessages(data.messages);
        }
        if (data?.sources) {
          setSources(data.sources);
        }
      },
    }
  );

  // Send message mutation
  const sendMessageMutation = useMutation(
    (message) => sendChatMessage(message, conversationIdRef.current),
    {
      onMutate: async (message) => {
        // Optimistically add user message
        const userMessage = {
          id: Date.now(),
          content: message,
          message_type: 'user',
          timestamp: new Date().toISOString(),
        };

        setMessages(prev => [...prev, userMessage]);
        setIsLoading(true);

        return { userMessage };
      },
      onSuccess: (response, message, context) => {
        // Add AI response
        const aiMessage = {
          id: Date.now() + 1,
          content: response.message,
          message_type: 'bot',
          timestamp: response.timestamp,
          sources: response.sources,
          confidence: response.confidence,
        };

        setMessages(prev => [...prev, aiMessage]);
        
        // Update sources
        if (response.sources) {
          setSources(prev => [...prev, ...response.sources]);
        }

        // Update conversation ID if provided
        if (response.conversation_id) {
          conversationIdRef.current = response.conversation_id;
        }

        setIsLoading(false);

        // Invalidate chat history query
        queryClient.invalidateQueries(['chatHistory', conversationIdRef.current]);
      },
      onError: (error, message, context) => {
        // Remove the user message on error
        setMessages(prev => prev.filter(msg => msg.id !== context.userMessage.id));
        setIsLoading(false);
        
        toast.error('Failed to send message. Please try again.');
        console.error('Chat error:', error);
      },
    }
  );

  // Clear chat mutation
  const clearChatMutation = useMutation(
    () => clearChatHistory(conversationIdRef.current),
    {
      onSuccess: () => {
        setMessages([]);
        setSources([]);
        conversationIdRef.current = null;
        queryClient.invalidateQueries(['chatHistory']);
        toast.success('Chat history cleared');
      },
      onError: (error) => {
        toast.error('Failed to clear chat history');
        console.error('Clear chat error:', error);
      },
    }
  );

  const sendMessage = useCallback(async (message) => {
    if (!message.trim()) return;

    try {
      await sendMessageMutation.mutateAsync(message);
    } catch (error) {
      // Error is handled in onError callback
      throw error;
    }
  }, [sendMessageMutation]);

  const clearChat = useCallback(async () => {
    try {
      await clearChatMutation.mutateAsync();
    } catch (error) {
      // Error is handled in onError callback
      throw error;
    }
  }, [clearChatMutation]);

  const addSystemMessage = useCallback((content) => {
    const systemMessage = {
      id: Date.now(),
      content,
      message_type: 'system',
      timestamp: new Date().toISOString(),
    };
    setMessages(prev => [...prev, systemMessage]);
  }, []);

  const updateMessage = useCallback((messageId, updates) => {
    setMessages(prev => 
      prev.map(msg => 
        msg.id === messageId ? { ...msg, ...updates } : msg
      )
    );
  }, []);

  const removeMessage = useCallback((messageId) => {
    setMessages(prev => prev.filter(msg => msg.id !== messageId));
  }, []);

  const getConversationId = useCallback(() => {
    return conversationIdRef.current;
  }, []);

  const setConversationId = useCallback((id) => {
    conversationIdRef.current = id;
  }, []);

  return {
    // State
    messages,
    sources,
    isLoading: isLoading || historyLoading,
    
    // Actions
    sendMessage,
    clearChat,
    addSystemMessage,
    updateMessage,
    removeMessage,
    
    // Conversation management
    getConversationId,
    setConversationId,
    
    // Mutations
    sendMessageMutation,
    clearChatMutation,
  };
}; 