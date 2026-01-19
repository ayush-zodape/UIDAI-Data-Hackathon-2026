import React from 'react';
import { AlertTriangle } from 'lucide-react';

const ProblemDistrictsTable = ({ districts, onSelectDistrict }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
        <AlertTriangle className="mr-2 text-red-500" size={20} />
        Top 10 Problem Districts (Highest BLI)
      </h3>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b-2 border-gray-200">
              <th className="text-left py-3 px-4">Rank</th>
              <th className="text-left py-3 px-4">District</th>
              <th className="text-left py-3 px-4">State</th>
              <th className="text-right py-3 px-4">BLI Score</th>
              <th className="text-right py-3 px-4">Gap</th>
              <th className="text-center py-3 px-4">Risk</th>
              <th className="text-center py-3 px-4">Action</th>
            </tr>
          </thead>
          <tbody>
            {districts.map((district, index) => (
              <tr
                key={`${district.state}-${district.district}`}
                className="border-b border-gray-100 hover:bg-gray-50"
              >
                <td className="py-3 px-4 font-bold text-gray-500">#{index + 1}</td>
                <td className="py-3 px-4 font-semibold">{district.district}</td>
                <td className="py-3 px-4 text-gray-600">{district.state}</td>
                <td className="py-3 px-4 text-right font-mono">
                  {district.bli_score.toFixed(4)}
                </td>
                <td className="py-3 px-4 text-right font-mono text-red-600">
                  {district.child_update_gap.toLocaleString()}
                </td>
                <td className="py-3 px-4 text-center">
                  <span
                    className="px-3 py-1 rounded-full text-sm font-semibold"
                    style={{
                      backgroundColor: `${district.color_code}20`,
                      color: district.color_code
                    }}
                  >
                    {district.risk_level}
                  </span>
                </td>
                <td className="py-3 px-4 text-center">
                  <button
                    onClick={() => onSelectDistrict(district.district)}
                    className="text-uidai-blue hover:underline text-sm"
                  >
                    View Trend
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ProblemDistrictsTable;
