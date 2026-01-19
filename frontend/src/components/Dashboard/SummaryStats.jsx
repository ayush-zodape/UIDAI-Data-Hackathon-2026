import React from 'react';
import { TrendingUp, TrendingDown, Users, Calendar } from 'lucide-react';

const SummaryStats = ({ analysisResults }) => {
  if (!analysisResults) return null;
  
  const { total_records, date_range, overall_bli, top_problem_districts } = analysisResults;
  
  // Count risk levels
  const riskCounts = top_problem_districts.reduce((acc, d) => {
    acc[d.risk_level] = (acc[d.risk_level] || 0) + 1;
    return acc;
  }, {});
  
  const stats = [
    {
      label: 'Total Records',
      value: total_records.toLocaleString(),
      icon: Users,
      color: 'text-blue-600'
    },
    {
      label: 'Overall BLI',
      value: overall_bli.toFixed(4),
      icon: overall_bli > 0.3 ? TrendingUp : TrendingDown,
      color: overall_bli > 0.5 ? 'text-red-600' : overall_bli > 0.3 ? 'text-orange-500' : 'text-green-600'
    },
    {
      label: 'Date Range',
      value: `${date_range.start} to ${date_range.end}`,
      icon: Calendar,
      color: 'text-gray-600'
    },
    {
      label: 'Critical Districts',
      value: riskCounts['Critical'] || 0,
      icon: TrendingUp,
      color: 'text-red-600'
    }
  ];
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {stats.map((stat, index) => (
        <div key={index} className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">{stat.label}</p>
              <p className={`text-2xl font-bold ${stat.color}`}>{stat.value}</p>
            </div>
            <stat.icon className={`${stat.color}`} size={28} />
          </div>
        </div>
      ))}
    </div>
  );
};

export default SummaryStats;
