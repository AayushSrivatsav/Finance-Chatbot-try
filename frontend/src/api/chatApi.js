import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Send a chat message
 * @param {string} message - The message content
 * @param {string} conversationId - Optional conversation ID
 * @returns {Promise<Object>} Response with AI reply
 */
export const sendChatMessage = async (message, conversationId = null) => {
  try {
    const response = await api.post('/chat/send', {
      message,
      conversation_id: conversationId,
    });
    return response;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw new Error(error.response?.data?.detail || 'Failed to send message');
  }
};

/**
 * Get chat history for a conversation
 * @param {string} conversationId - Conversation ID
 * @returns {Promise<Object>} Chat history
 */
export const getChatHistory = async (conversationId) => {
  try {
    const response = await api.get(`/chat/history/${conversationId}`);
    return response;
  } catch (error) {
    console.error('Error fetching chat history:', error);
    throw new Error(error.response?.data?.detail || 'Failed to fetch chat history');
  }
};

/**
 * Clear chat history for a conversation
 * @param {string} conversationId - Conversation ID
 * @returns {Promise<Object>} Success response
 */
export const clearChatHistory = async (conversationId) => {
  try {
    const response = await api.delete(`/chat/history/${conversationId}`);
    return response;
  } catch (error) {
    console.error('Error clearing chat history:', error);
    throw new Error(error.response?.data?.detail || 'Failed to clear chat history');
  }
};

/**
 * Get chat statistics
 * @returns {Promise<Object>} Chat statistics
 */
export const getChatStats = async () => {
  try {
    const response = await api.get('/chat/stats');
    return response;
  } catch (error) {
    console.error('Error fetching chat stats:', error);
    throw new Error(error.response?.data?.detail || 'Failed to fetch chat statistics');
  }
};

/**
 * Query RAG system directly
 * @param {string} query - The query to send to RAG
 * @param {number} topK - Number of top results to return
 * @param {boolean} includeSources - Whether to include sources
 * @returns {Promise<Object>} RAG response
 */
export const queryRAG = async (query, topK = 5, includeSources = true) => {
  try {
    const response = await api.post('/rag/query', {
      query,
      top_k: topK,
      include_sources: includeSources,
    });
    return response;
  } catch (error) {
    console.error('Error querying RAG:', error);
    throw new Error(error.response?.data?.detail || 'Failed to query RAG system');
  }
};

/**
 * Search for similar documents
 * @param {string} query - Search query
 * @param {number} topK - Number of results to return
 * @returns {Promise<Object>} Search results
 */
export const searchSimilar = async (query, topK = 5) => {
  try {
    const response = await api.get('/rag/search', {
      params: { query, top_k: topK },
    });
    return response;
  } catch (error) {
    console.error('Error searching similar documents:', error);
    throw new Error(error.response?.data?.detail || 'Failed to search documents');
  }
};

/**
 * Get RAG system statistics
 * @returns {Promise<Object>} RAG statistics
 */
export const getRAGStats = async () => {
  try {
    const response = await api.get('/rag/stats');
    return response;
  } catch (error) {
    console.error('Error fetching RAG stats:', error);
    throw new Error(error.response?.data?.detail || 'Failed to fetch RAG statistics');
  }
};

/**
 * Add documents to RAG system
 * @param {File} file - File to upload
 * @returns {Promise<Object>} Upload response
 */
export const addDocumentToRAG = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/rag/add-documents', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response;
  } catch (error) {
    console.error('Error adding document to RAG:', error);
    throw new Error(error.response?.data?.detail || 'Failed to add document');
  }
};

/**
 * Add text content to RAG system
 * @param {string} text - Text content to add
 * @param {Object} metadata - Optional metadata
 * @returns {Promise<Object>} Add response
 */
export const addTextToRAG = async (text, metadata = null) => {
  try {
    const response = await api.post('/rag/add-text', {
      text,
      metadata,
    });
    return response;
  } catch (error) {
    console.error('Error adding text to RAG:', error);
    throw new Error(error.response?.data?.detail || 'Failed to add text');
  }
};

/**
 * Clear RAG system
 * @returns {Promise<Object>} Clear response
 */
export const clearRAG = async () => {
  try {
    const response = await api.delete('/rag/clear');
    return response;
  } catch (error) {
    console.error('Error clearing RAG:', error);
    throw new Error(error.response?.data?.detail || 'Failed to clear RAG system');
  }
};

/**
 * Health check for RAG system
 * @returns {Promise<Object>} Health status
 */
export const getRAGHealth = async () => {
  try {
    const response = await api.get('/rag/health');
    return response;
  } catch (error) {
    console.error('Error checking RAG health:', error);
    throw new Error(error.response?.data?.detail || 'Failed to check RAG health');
  }
};

export default api; 