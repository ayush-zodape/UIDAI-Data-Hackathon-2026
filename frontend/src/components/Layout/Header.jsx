import React from 'react';
import { Link } from 'react-router-dom';
import useDataStore from '../../store/useDataStore';

const Header = () => {
  const { isDataLoaded, overallBLI } = useDataStore();
  
  return (
    <header className="bg-gradient-to-r from-uidai-blue to-uidai-orange text-white shadow-lg">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center">
              <span className="text-uidai-blue font-bold text-xl">BLI</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold">Digital Continuity</h1>
              <p className="text-sm opacity-90">Biometric Lag Index Analyzer</p>
            </div>
          </div>
          
          {isDataLoaded && (
            <div className="bg-white/20 rounded-lg px-4 py-2">
              <span className="text-sm">Overall BLI:</span>
              <span className="ml-2 text-xl font-bold">{overallBLI.toFixed(4)}</span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
