import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useDataStore from '../store/useDataStore';
import { computeBLI } from '../services/api';
import SummaryStats from '../components/Dashboard/SummaryStats';
import ProblemDistrictsTable from '../components/Dashboard/ProblemDistrictsTable';
import GapWideningCurve from '../components/Charts/GapWideningCurve';
import BLIDistribution from '../components/Charts/BLIDistribution';
import SeasonalityChart from '../components/Charts/SeasonalityChart';
import DistrictHeatmap from '../components/Charts/DistrictHeatmap';
import { Loader } from 'lucide-react';

const DashboardPage = () => {
  const navigate = useNavigate();
  const { isDataLoaded, analysisResults, setAnalysisResults, selectedDistrict, setSelectedDistrict } = useDataStore();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    if (!isDataLoaded) {
      navigate('/upload');
      return;
    }
    
    const fetchAnalysis = async () => {
      setLoading(true);
      try {
        const results = await computeBLI();
        setAnalysisResults(results);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to compute analysis');
      } finally {
        setLoading(false);
      }
    };
    
    if (!analysisResults) {
      fetchAnalysis();
    } else {
      setLoading(false);
    }
  }, [isDataLoaded, analysisResults, navigate, setAnalysisResults]);
  
  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <Loader className="animate-spin mx-auto mb-4 text-uidai-blue" size={48} />
          <p className="text-gray-600">Computing Biometric Lag Index...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p className="text-red-600">{error}</p>
        <button
          onClick={() => navigate('/upload')}
          className="mt-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700"
        >
          Re-upload Data
        </button>
      </div>
    );
  }
  
  if (!analysisResults) return null;
  
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">BLI Analysis Dashboard</h1>
        <span className="text-sm text-gray-500">
          Data: {analysisResults.date_range.start} to {analysisResults.date_range.end}
        </span>
      </div>
      
      {/* Summary Statistics */}
      <SummaryStats analysisResults={analysisResults} />
      
      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Problem Districts Table */}
        <div className="lg:col-span-2">
          <ProblemDistrictsTable
            districts={analysisResults.top_problem_districts}
            onSelectDistrict={setSelectedDistrict}
          />
        </div>
        
        {/* BLI Distribution */}
        <BLIDistribution districts={analysisResults.top_problem_districts} />
        
        {/* Seasonality Chart */}
        <SeasonalityChart />
        
        {/* Gap Widening Curve */}
        <div className="lg:col-span-2">
          <GapWideningCurve district={selectedDistrict || analysisResults.top_problem_districts[0]?.district} />
        </div>
        
        {/* State Summary Heatmap */}
        <div className="lg:col-span-2">
          <DistrictHeatmap stateSummary={analysisResults.state_summary} />
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
