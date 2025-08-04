import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth headers here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// News API endpoints
export const newsApi = {
  // Get latest news
  getLatestNews: (params = {}) => 
    api.get('/news/latest', { params }),

  // Get stock-specific news
  getStockNews: (symbol, params = {}) => 
    api.get(`/news/stock/${symbol}`, { params }),

  // Get news sources
  getNewsSources: () => 
    api.get('/news/sources'),

  // Get news categories
  getNewsCategories: () => 
    api.get('/news/categories'),

  // Search news
  searchNews: (query, params = {}) => 
    api.post('/news/search', { query, ...params }),
};

export default newsApi; 