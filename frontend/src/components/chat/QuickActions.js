import React from 'react';
import { TrendingUp, Newspaper, BarChart3, HelpCircle } from 'lucide-react';

const QuickActions = ({ onActionClick }) => {
  const actions = [
    {
      id: 'stock_recommendation',
      title: 'Stock Recommendation',
      description: 'Get AI-powered stock recommendations',
      icon: TrendingUp,
      color: 'text-green-400'
    },
    {
      id: 'latest_news',
      title: 'Latest News',
      description: 'Get the latest financial news',
      icon: Newspaper,
      color: 'text-blue-400'
    },
    {
      id: 'market_analysis',
      title: 'Market Analysis',
      description: 'Analyze market trends and indicators',
      icon: BarChart3,
      color: 'text-purple-400'
    },
    {
      id: 'help',
      title: 'Help',
      description: 'Learn how to use the chatbot',
      icon: HelpCircle,
      color: 'text-gray-400'
    }
  ];

  return (
    <div className="grid grid-cols-2 gap-3">
      {actions.map((action) => {
        const Icon = action.icon;
        return (
          <button
            key={action.id}
            onClick={() => onActionClick(action.id)}
            className="p-4 bg-gray-800 border border-gray-700 rounded-lg hover:bg-gray-700 transition-colors text-left"
          >
            <div className="flex items-center space-x-3">
              <Icon className={`w-6 h-6 ${action.color}`} />
              <div>
                <h4 className="font-medium text-white text-sm">
                  {action.title}
                </h4>
                <p className="text-xs text-gray-400 mt-1">
                  {action.description}
                </p>
              </div>
            </div>
          </button>
        );
      })}
    </div>
  );
};

export default QuickActions; 