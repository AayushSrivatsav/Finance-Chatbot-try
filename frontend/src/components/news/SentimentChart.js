import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const SentimentChart = ({ data = [] }) => {
  const COLORS = ['#10B981', '#6B7280', '#EF4444'];

  const chartData = [
    { name: 'Positive', value: data.filter(d => d.sentiment === 'positive').length, color: COLORS[0] },
    { name: 'Neutral', value: data.filter(d => d.sentiment === 'neutral').length, color: COLORS[1] },
    { name: 'Negative', value: data.filter(d => d.sentiment === 'negative').length, color: COLORS[2] }
  ].filter(item => item.value > 0);

  if (chartData.length === 0) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Sentiment Distribution
        </h3>
        <div className="text-center text-gray-500 dark:text-gray-400 py-8">
          <p>No sentiment data available</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Sentiment Distribution
      </h3>
      
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
      
      <div className="mt-4 grid grid-cols-3 gap-4 text-center">
        {chartData.map((item, index) => (
          <div key={item.name} className="flex flex-col items-center">
            <div 
              className="w-4 h-4 rounded-full mb-1"
              style={{ backgroundColor: item.color }}
            />
            <span className="text-sm font-medium text-gray-900 dark:text-white">
              {item.name}
            </span>
            <span className="text-xs text-gray-500 dark:text-gray-400">
              {item.value} articles
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SentimentChart; 