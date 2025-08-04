import React from 'react';
import { Filter, Search, X } from 'lucide-react';

const NewsFilter = ({ filters, onFilterChange, onSearch, searchQuery, onClearFilters }) => {
  const categories = [
    'All',
    'Business',
    'Technology',
    'Markets',
    'Economy',
    'Politics',
    'Crypto'
  ];

  const sources = [
    'All Sources',
    'Reuters',
    'Bloomberg',
    'CNBC',
    'MarketWatch',
    'Yahoo Finance'
  ];

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 space-y-4">
      <div className="flex items-center space-x-2">
        <Filter className="w-5 h-5 text-gray-500 dark:text-gray-400" />
        <h3 className="font-semibold text-gray-900 dark:text-white">Filters</h3>
        {Object.values(filters).some(Boolean) && (
          <button
            onClick={onClearFilters}
            className="ml-auto flex items-center space-x-1 text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 transition-colors"
          >
            <X className="w-3 h-3" />
            <span>Clear all</span>
          </button>
        )}
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          placeholder="Search news..."
          value={searchQuery}
          onChange={(e) => onSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
        />
      </div>

      {/* Categories */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Category
        </label>
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => onFilterChange('category', category === 'All' ? '' : category)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                filters.category === category || (!filters.category && category === 'All')
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Sources */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Source
        </label>
        <div className="flex flex-wrap gap-2">
          {sources.map((source) => (
            <button
              key={source}
              onClick={() => onFilterChange('source', source === 'All Sources' ? '' : source)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                filters.source === source || (!filters.source && source === 'All Sources')
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {source}
            </button>
          ))}
        </div>
      </div>

      {/* Sentiment */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Sentiment
        </label>
        <div className="flex flex-wrap gap-2">
          {['All', 'Positive', 'Neutral', 'Negative'].map((sentiment) => (
            <button
              key={sentiment}
              onClick={() => onFilterChange('sentiment', sentiment === 'All' ? '' : sentiment.toLowerCase())}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                filters.sentiment === sentiment.toLowerCase() || (!filters.sentiment && sentiment === 'All')
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {sentiment}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default NewsFilter; 