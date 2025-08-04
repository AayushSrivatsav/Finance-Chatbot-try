import React, { useState } from 'react';
import { Globe, TrendingUp, TrendingDown, BarChart3, Activity } from 'lucide-react';

const MarketOverview = () => {
  const [selectedIndex, setSelectedIndex] = useState('SPY');

  const marketIndices = [
    {
      symbol: 'SPY',
      name: 'S&P 500',
      price: 4250.75,
      change: 45.20,
      changePercent: 1.08,
      volume: '2.5B',
      status: 'up'
    },
    {
      symbol: 'QQQ',
      name: 'NASDAQ-100',
      price: 15680.45,
      change: 125.30,
      changePercent: 0.81,
      volume: '1.8B',
      status: 'up'
    },
    {
      symbol: 'DIA',
      name: 'Dow Jones',
      price: 33450.20,
      change: -85.60,
      changePercent: -0.26,
      volume: '850M',
      status: 'down'
    },
    {
      symbol: 'IWM',
      name: 'Russell 2000',
      price: 1850.30,
      change: 32.15,
      changePercent: 1.77,
      volume: '650M',
      status: 'up'
    }
  ];

  const sectors = [
    { name: 'Technology', change: 2.1, status: 'up' },
    { name: 'Healthcare', change: 1.3, status: 'up' },
    { name: 'Financials', change: -0.8, status: 'down' },
    { name: 'Consumer Discretionary', change: 1.7, status: 'up' },
    { name: 'Energy', change: -1.2, status: 'down' },
    { name: 'Industrials', change: 0.9, status: 'up' },
    { name: 'Materials', change: 0.5, status: 'up' },
    { name: 'Utilities', change: -0.3, status: 'down' }
  ];

  const selectedIndexData = marketIndices.find(index => index.symbol === selectedIndex);

  return (
    <div className="h-full bg-black text-white p-6 overflow-y-auto">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">Market Overview</h1>
            <p className="text-gray-400">Real-time market data and trends</p>
          </div>
          <div className="flex items-center space-x-3">
            <Globe className="w-8 h-8 text-blue-400" />
            <Activity className="w-8 h-8 text-green-400" />
            <BarChart3 className="w-8 h-8 text-purple-400" />
          </div>
        </div>

        {/* Market Indices */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {marketIndices.map((index) => (
            <div
              key={index.symbol}
              onClick={() => setSelectedIndex(index.symbol)}
              className={`p-4 rounded-lg cursor-pointer transition-colors border ${
                selectedIndex === index.symbol
                  ? 'bg-blue-600 border-blue-500 text-white'
                  : 'bg-gray-800 border-gray-700 hover:bg-gray-700 text-white'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold">{index.symbol}</span>
                {index.status === 'up' ? (
                  <TrendingUp className="w-4 h-4 text-green-400" />
                ) : (
                  <TrendingDown className="w-4 h-4 text-red-400" />
                )}
              </div>
              <div className="text-sm text-gray-300 mb-1">{index.name}</div>
              <div className="text-lg font-bold">${index.price.toLocaleString()}</div>
              <div className={`text-sm ${
                index.status === 'up' ? 'text-green-400' : 'text-red-400'
              }`}>
                {index.status === 'up' ? '+' : ''}{index.change} ({index.changePercent}%)
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Selected Index Details */}
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-white mb-4">
              {selectedIndexData?.name} Details
            </h2>
            {selectedIndexData && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Current Price:</span>
                  <span className="text-2xl font-bold text-white">
                    ${selectedIndexData.price.toLocaleString()}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Change:</span>
                  <div className="text-right">
                    <div className={`text-lg font-semibold ${
                      selectedIndexData.status === 'up' ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {selectedIndexData.status === 'up' ? '+' : ''}{selectedIndexData.change}
                    </div>
                    <div className={`text-sm ${
                      selectedIndexData.status === 'up' ? 'text-green-400' : 'text-red-400'
                    }`}>
                      ({selectedIndexData.changePercent}%)
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Volume:</span>
                  <span className="text-white">{selectedIndexData.volume}</span>
                </div>
                
                {/* Market Sentiment */}
                <div className="mt-6 p-4 bg-gray-700 rounded-lg">
                  <h3 className="font-semibold text-white mb-2">Market Sentiment</h3>
                  <div className="flex items-center space-x-2 mb-2">
                    <TrendingUp className="w-5 h-5 text-green-400" />
                    <span className="text-green-400 font-semibold">Bullish</span>
                    <span className="text-gray-400">(65% confidence)</span>
                  </div>
                  <p className="text-gray-300 text-sm">
                    Market showing positive momentum with strong institutional buying and 
                    improving economic indicators.
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Sector Performance */}
          <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
            <h2 className="text-xl font-semibold text-white mb-4">Sector Performance</h2>
            <div className="space-y-3">
              {sectors.map((sector) => (
                <div key={sector.name} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
                  <span className="text-white font-medium">{sector.name}</span>
                  <div className="flex items-center space-x-2">
                    {sector.status === 'up' ? (
                      <TrendingUp className="w-4 h-4 text-green-400" />
                    ) : (
                      <TrendingDown className="w-4 h-4 text-red-400" />
                    )}
                    <span className={`font-semibold ${
                      sector.status === 'up' ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {sector.status === 'up' ? '+' : ''}{sector.change}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Market Summary */}
        <div className="bg-gray-800 border border-gray-700 rounded-lg p-6">
          <h2 className="text-xl font-semibold text-white mb-4">Market Summary</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-2">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div className="text-2xl font-bold text-white">2,847</div>
              <div className="text-gray-400">Advancing Stocks</div>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-red-600 rounded-full flex items-center justify-center mx-auto mb-2">
                <TrendingDown className="w-6 h-6 text-white" />
              </div>
              <div className="text-2xl font-bold text-white">1,234</div>
              <div className="text-gray-400">Declining Stocks</div>
            </div>
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-2">
                <BarChart3 className="w-6 h-6 text-white" />
              </div>
              <div className="text-2xl font-bold text-white">4.2B</div>
              <div className="text-gray-400">Total Volume</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketOverview; 