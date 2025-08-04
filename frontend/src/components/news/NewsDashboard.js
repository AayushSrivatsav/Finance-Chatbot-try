import React, { useState } from 'react';
import { TrendingUp, TrendingDown, Minus, Search, RefreshCw, ExternalLink, Globe, BarChart3, Newspaper } from 'lucide-react';

const NewsDashboard = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Mock news data
  const mockNews = [
    {
      id: 1,
      title: "Tech Stocks Rally on Strong Earnings Reports",
      description: "Major technology companies report better-than-expected quarterly results, driving market optimism and pushing indices higher.",
      url: "https://example.com/tech-rally",
      published_at: "2024-08-04T10:00:00Z",
      source: "Reuters",
      sentiment: "positive",
      category: "technology"
    },
    {
      id: 2,
      title: "Federal Reserve Signals Potential Rate Changes",
      description: "The Fed indicates possible adjustments to interest rates in response to economic indicators and inflation data.",
      url: "https://example.com/fed-rates",
      published_at: "2024-08-04T09:30:00Z",
      source: "Bloomberg",
      sentiment: "neutral",
      category: "economy"
    },
    {
      id: 3,
      title: "Oil Prices Decline Amid Supply Concerns",
      description: "Crude oil prices fall as concerns about global supply and demand dynamics weigh on market sentiment.",
      url: "https://example.com/oil-prices",
      published_at: "2024-08-04T08:45:00Z",
      source: "MarketWatch",
      sentiment: "negative",
      category: "energy"
    },
    {
      id: 4,
      title: "Healthcare Sector Shows Strong Growth",
      description: "Healthcare companies demonstrate robust performance with innovative treatments and strong pipeline developments.",
      url: "https://example.com/healthcare-growth",
      published_at: "2024-08-04T07:15:00Z",
      source: "CNBC",
      sentiment: "positive",
      category: "healthcare"
    },
    {
      id: 5,
      title: "Cryptocurrency Market Volatility Continues",
      description: "Digital assets experience significant price swings as regulatory developments and market sentiment remain uncertain.",
      url: "https://example.com/crypto-volatility",
      published_at: "2024-08-04T06:30:00Z",
      source: "Yahoo Finance",
      sentiment: "neutral",
      category: "crypto"
    }
  ];

  const categories = [
    { id: 'all', name: 'All Categories' },
    { id: 'technology', name: 'Technology' },
    { id: 'economy', name: 'Economy' },
    { id: 'energy', name: 'Energy' },
    { id: 'healthcare', name: 'Healthcare' },
    { id: 'crypto', name: 'Cryptocurrency' }
  ];

  // Filter news based on search and category
  const filteredNews = mockNews.filter(article => {
    const matchesSearch = article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         article.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || article.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // Calculate sentiment stats
  const sentimentStats = filteredNews.reduce((acc, article) => {
    acc[article.sentiment] = (acc[article.sentiment] || 0) + 1;
    return acc;
  }, { positive: 0, negative: 0, neutral: 0 });

  const handleRefresh = () => {
    // In a real app, this would refetch data
    console.log('Refreshing news...');
  };

  return (
    <div className="h-full bg-black text-white p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Financial News</h1>
            <p className="text-gray-400">Latest market news and insights</p>
          </div>
          <div className="flex items-center space-x-3">
            <Newspaper className="w-8 h-8 text-blue-400" />
            <BarChart3 className="w-8 h-8 text-green-400" />
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Total Articles</p>
                <p className="text-2xl font-bold text-white">{filteredNews.length}</p>
              </div>
              <Globe className="w-8 h-8 text-blue-400" />
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Positive</p>
                <p className="text-2xl font-bold text-green-400">{sentimentStats.positive}</p>
              </div>
              <TrendingUp className="w-8 h-8 text-green-400" />
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Negative</p>
                <p className="text-2xl font-bold text-red-400">{sentimentStats.negative}</p>
              </div>
              <TrendingDown className="w-8 h-8 text-red-400" />
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-400">Neutral</p>
                <p className="text-2xl font-bold text-gray-400">{sentimentStats.neutral}</p>
              </div>
              <Minus className="w-8 h-8 text-gray-400" />
            </div>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
            <div className="flex-1 max-w-md">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Search news..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                {categories.map(category => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
              
              <button
                onClick={handleRefresh}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <RefreshCw className="w-4 h-4" />
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </div>

        {/* News Grid */}
        <div className="space-y-4">
          {filteredNews.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-600 text-6xl mb-4">📰</div>
              <h3 className="text-xl font-semibold text-white mb-2">No news found</h3>
              <p className="text-gray-400">Try adjusting your search or filters.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredNews.map((article) => (
                <div
                  key={article.id}
                  className="bg-gray-800 border border-gray-700 rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
                >
                  <div className="p-4">
                    <div className="flex items-start justify-between mb-2">
                      <div className="flex items-center space-x-2 text-xs text-gray-400">
                        <span>{new Date(article.published_at).toLocaleDateString()}</span>
                      </div>
                      
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        article.sentiment === 'positive' ? 'text-green-400 bg-green-900' :
                        article.sentiment === 'negative' ? 'text-red-400 bg-red-900' :
                        'text-gray-400 bg-gray-700'
                      }`}>
                        {article.sentiment}
                      </span>
                    </div>
                    
                    <h3 className="font-semibold text-white mb-2 line-clamp-2">
                      {article.title}
                    </h3>
                    
                    <p className="text-sm text-gray-400 mb-3 line-clamp-3">
                      {article.description}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span className="text-xs text-gray-500">{article.source}</span>
                      </div>
                      
                      <a
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center space-x-1 text-xs text-blue-400 hover:text-blue-300 transition-colors"
                      >
                        <span>Read more</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default NewsDashboard; 