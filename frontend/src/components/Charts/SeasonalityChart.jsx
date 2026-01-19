import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import { getSeasonality } from '../../services/api';

const SeasonalityChart = () => {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getSeasonality();
        setData(result);
      } catch (error) {
        console.error('Failed to fetch seasonality data:', error);
      }
    };
    fetchData();
  }, []);
  
  if (!data) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 h-80 flex items-center justify-center">
        <div className="animate-pulse text-gray-400">Loading seasonality data...</div>
      </div>
    );
  }
  
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-bold text-gray-800 mb-2">
        Update Seasonality Pattern
      </h3>
      <p className="text-sm text-gray-500 mb-4">
        Peak: <span className="text-green-600 font-semibold">{data.peak_month}</span> | 
        Low: <span className="text-red-600 font-semibold">{data.low_month}</span>
      </p>
      
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data.monthly_data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month_name" tick={{ fontSize: 10 }} />
          <YAxis tickFormatter={(val) => (val / 1000).toFixed(0) + 'K'} />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="bio_age_5_17"
            name="Biometric Updates"
            stroke="#22c55e"
            strokeWidth={2}
            dot={{ fill: '#22c55e' }}
          />
        </LineChart>
      </ResponsiveContainer>
      
      <div className="mt-4 p-3 bg-blue-50 rounded-lg text-sm text-blue-700">
        <strong>Insight:</strong> Plan intervention camps during {data.low_month} 
        when update rates are lowest.
      </div>
    </div>
  );
};

export default SeasonalityChart;
