import React from 'react';

const DistrictHeatmap = ({ stateSummary }) => {
  if (!stateSummary || stateSummary.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 h-64 flex items-center justify-center">
        <p className="text-gray-500">No state data available</p>
      </div>
    );
  }
  
  const getColorClass = (bli) => {
    if (bli < 0.1) return 'bg-green-100 text-green-800 border-green-300';
    if (bli < 0.3) return 'bg-yellow-100 text-yellow-800 border-yellow-300';
    if (bli < 0.5) return 'bg-orange-100 text-orange-800 border-orange-300';
    return 'bg-red-100 text-red-800 border-red-300';
  };
  
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-lg font-bold text-gray-800 mb-4">
        State-wise BLI Summary
      </h3>
      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        {stateSummary.map((state, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg border ${getColorClass(state.bli_score)}`}
          >
            <p className="font-semibold text-sm truncate">{state.state}</p>
            <p className="text-lg font-bold">{state.bli_score.toFixed(4)}</p>
            <p className="text-xs opacity-75">
              Gap: {state.child_update_gap?.toLocaleString() || 'N/A'}
            </p>
          </div>
        ))}
      </div>
      
      <div className="mt-4 flex justify-center space-x-4 text-xs">
        <span className="flex items-center">
          <span className="w-3 h-3 rounded bg-green-200 mr-1"></span> Low
        </span>
        <span className="flex items-center">
          <span className="w-3 h-3 rounded bg-yellow-200 mr-1"></span> Medium
        </span>
        <span className="flex items-center">
          <span className="w-3 h-3 rounded bg-orange-200 mr-1"></span> High
        </span>
        <span className="flex items-center">
          <span className="w-3 h-3 rounded bg-red-200 mr-1"></span> Critical
        </span>
      </div>
    </div>
  );
};

export default DistrictHeatmap;
