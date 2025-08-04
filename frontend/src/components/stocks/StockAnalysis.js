import React, { useState } from 'react';
import { TrendingUp, BarChart3, Search, DollarSign, Activity } from 'lucide-react';

const StockAnalysis = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStock, setSelectedStock] = useState(null);

  const mockStocks = [
    { symbol: 'AAPL', name: 'Apple Inc.', price: 150.25, change: 2.5, changePercent: 1.67, volume: '50M' },
    { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 2750.80, change: -15.20, changePercent: -0.55, volume: '25M' },
    { symbol: 'MSFT', name: 'Microsoft Corp.', price: 320.45, change: 8.75, changePercent: 2.81, volume: '35M' },
    { symbol: 'TSLA', name: 'Tesla Inc.', price: 850.30, change: 25.10, changePercent: 3.04, volume: '40M' },
    { symbol: 'AMZN', name: 'Amazon.com Inc.', price: 3200.15, change: -45.85, changePercent: -1.41, volume: '30M' }
  ];

  const handleStockSelect = (stock) => {
    setSelectedStock(stock);
  };

  return (
    <div className="h-full bg-black text-white p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Stock Analysis</h1>
            <p className="text-gray-400">AI-powered stock analysis and recommendations</p>
          </div>
          <div className="flex items-center space-x-3">
            <BarChart3 className="w-8 h-8 text-blue-400" />
            <Activity className="w-8 h-8 text-green-400" />
          </div>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search stocks by symbol or name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Stock List */}
          <div className="lg:col-span-1">
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-4">
              <h2 className="text-xl font-semibold text-white mb-4">Popular Stocks</h2>
              <div className="space-y-3">
                {mockStocks
                  .filter(stock => 
                    stock.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
                    stock.name.toLowerCase().includes(searchQuery.toLowerCase())
                  )
                  .map((stock) => (
                    <div
                      key={stock.symbol}
                      onClick={() => handleStockSelect(stock)}
                      className={`p-3 rounded-lg cursor-pointer transition-colors ${
                        selectedStock?.symbol === stock.symbol
                          ? 'bg-blue-600 text-white'
                          : 'bg-gray-700 hover:bg-gray-600 text-white'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-semibold">{stock.symbol}</div>
                          <div className="text-sm text-gray-300">{stock.name}</div>
                        </div>
                        <div className="text-right">
                          <div className="font-semibold">${stock.price}</div>
                          <div className={`text-sm ${
                            stock.change >= 0 ? 'text-green-400' : 'text-red-400'
                          }`}>
                            {stock.change >= 0 ? '+' : ''}{stock.change} ({stock.changePercent}%)
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          </div>

          {/* Stock Details */}
          <div className="lg:col-span-2">
            {selectedStock ? (
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-white">{selectedStock.symbol}</h2>
                    <p className="text-gray-400">{selectedStock.name}</p>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-bold text-white">${selectedStock.price}</div>
                    <div className={`text-lg ${
                      selectedStock.change >= 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {selectedStock.change >= 0 ? '+' : ''}{selectedStock.change} ({selectedStock.changePercent}%)
                    </div>
                  </div>
                </div>

                {/* AI Analysis */}
                <div className="space-y-4">
                  <div className="bg-gray-700 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-white mb-2">AI Recommendation</h3>
                    <div className="flex items-center space-x-2 mb-2">
                      <TrendingUp className="w-5 h-5 text-green-400" />
                      <span className="text-green-400 font-semibold">BUY</span>
                      <span className="text-gray-400">(Confidence: 85%)</span>
                    </div>
                    <p className="text-gray-300 text-sm">
                      Strong fundamentals with positive technical indicators. Recent earnings beat expectations 
                      and the company shows solid growth potential in the current market environment.
                    </p>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-700 rounded-lg p-4">
                      <h4 className="font-semibold text-white mb-2">Technical Indicators</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-400">RSI:</span>
                          <span className="text-green-400">65 (Neutral)</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">MACD:</span>
                          <span className="text-green-400">Bullish</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Moving Avg:</span>
                          <span className="text-green-400">Above 50-day</span>
                        </div>
                      </div>
                    </div>

                    <div className="bg-gray-700 rounded-lg p-4">
                      <h4 className="font-semibold text-white mb-2">Key Metrics</h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-400">Volume:</span>
                          <span className="text-white">{selectedStock.volume}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">Market Cap:</span>
                          <span className="text-white">$2.5T</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-400">P/E Ratio:</span>
                          <span className="text-white">25.4</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 flex flex-col items-center justify-center h-64">
                <DollarSign className="w-16 h-16 text-gray-600 mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">Select a Stock</h3>
                <p className="text-gray-400 text-center">
                  Choose a stock from the list to view detailed analysis and AI recommendations.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StockAnalysis; 