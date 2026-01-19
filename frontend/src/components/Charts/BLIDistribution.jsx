import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

const BLIDistribution = ({ districts }) => {
  // Take top 10 and format for chart
  const chartData = districts.slice(0, 10).map(d => ({
    name: d.district.length > 15 ? d.district.slice(0, 15) + '...' : d.district,
    fullName: d.district,
    bli: d.bli_score,
    color: d.color_code
  }));
  
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-bold text-gray-800 mb-4">
        BLI Distribution by District
      </h3>
      
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis type="number" domain={[0, 1]} />
          <YAxis
            type="category"
            dataKey="name"
            width={120}
            tick={{ fontSize: 11 }}
          />
          <Tooltip
            formatter={(value) => [value.toFixed(4), 'BLI Score']}
            labelFormatter={(label, payload) => payload[0]?.payload?.fullName || label}
          />
          <Bar dataKey="bli" name="BLI Score">
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      
      <div className="mt-4 flex justify-center space-x-4 text-sm">
        <span className="flex items-center">
          <span className="w-3 h-3 rounded bg-bli-low mr-1"></span> Low (&lt;0.1)
        </span>
        <span className="flex items-center">
          <span className="w-3 h-3 rounded bg-bli-medium mr-1"></span> Medium
        </span>
        <span className="flex items-center">
          <span className="w-3 h-3 rounded bg-bli-high mr-1"></span> High
        </span>
        <span className="flex items-center">
          <span className="w-3 h-3 rounded bg-bli-critical mr-1"></span> Critical
        </span>
      </div>
    </div>
  );
};

export default BLIDistribution;
