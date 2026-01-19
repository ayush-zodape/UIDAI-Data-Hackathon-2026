import React, { useEffect, useState } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { getGapWidening } from '../../services/api';

const GapWideningCurve = ({ district }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const result = await getGapWidening(district);
        setData(result);
      } catch (error) {
        console.error('Failed to fetch gap widening data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    if (district) {
      fetchData();
    }
  }, [district]);
  
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 h-96 flex items-center justify-center">
        <div className="animate-pulse text-gray-400">Loading chart...</div>
      </div>
    );
  }
  
  if (!data) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 h-96 flex items-center justify-center">
        <p className="text-gray-500">Select a district to view the gap analysis</p>
      </div>
    );
  }
  
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-bold text-gray-800 mb-2">
        The Widening Gap: {data.district}, {data.state}
      </h3>
      <p className="text-sm text-gray-500 mb-4">
        Cumulative Enrollments vs. Biometric Updates (Age 5-17)
      </p>
      
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart data={data.data_points}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12 }}
            tickFormatter={(val) => new Date(val).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}
          />
          <YAxis
            tick={{ fontSize: 12 }}
            tickFormatter={(val) => val.toLocaleString()}
          />
          <Tooltip
            formatter={(value, name) => [value.toLocaleString(), name]}
            labelFormatter={(label) => new Date(label).toLocaleDateString('en-IN', { 
              year: 'numeric', month: 'long', day: 'numeric' 
            })}
          />
          <Legend />
          
          {/* Enrollment Area */}
          <Area
            type="monotone"
            dataKey="cumulative_enrollments"
            name="Cumulative Enrollments"
            stroke="#1e40af"
            fill="#1e40af"
            fillOpacity={0.3}
          />
          
          {/* Update Area */}
          <Area
            type="monotone"
            dataKey="cumulative_updates"
            name="Biometric Updates"
            stroke="#22c55e"
            fill="#22c55e"
            fillOpacity={0.3}
          />
          
          {/* Gap Area (visual only - the space between) */}
        </AreaChart>
      </ResponsiveContainer>
      
      <div className="mt-4 p-4 bg-red-50 rounded-lg">
        <p className="text-sm text-red-700">
          <strong>Interpretation:</strong> The shaded area between the blue (Enrollments) and green (Updates) lines 
          represents children who have enrolled but not yet updated their biometrics. 
          A widening gap indicates growing risk of service disruption.
        </p>
      </div>
    </div>
  );
};

export default GapWideningCurve;
