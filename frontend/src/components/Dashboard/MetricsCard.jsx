import React from 'react';

const MetricsCard = ({ title, value, subtitle, icon: Icon, color }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">{title}</p>
          <p className={`text-3xl font-bold ${color || 'text-gray-800'}`}>
            {value}
          </p>
          {subtitle && <p className="text-sm text-gray-400 mt-1">{subtitle}</p>}
        </div>
        {Icon && (
          <div className={`p-4 rounded-full bg-gray-100`}>
            <Icon size={24} className="text-gray-600" />
          </div>
        )}
      </div>
    </div>
  );
};

export default MetricsCard;
