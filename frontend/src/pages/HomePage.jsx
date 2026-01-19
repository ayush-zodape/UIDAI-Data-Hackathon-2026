import React from 'react';
import { Link } from 'react-router-dom';
import { Upload, BarChart3, MessageCircle, ArrowRight, AlertTriangle, Users, TrendingUp } from 'lucide-react';

const HomePage = () => {
  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-uidai-blue to-blue-800 rounded-2xl p-8 text-white mb-8">
        <h1 className="text-4xl font-bold mb-4">
          Digital Continuity Platform
        </h1>
        <p className="text-xl opacity-90 mb-6">
          Identifying At-Risk Cohorts through Biometric Lag Index Analysis
        </p>
        <p className="text-lg opacity-80 mb-8">
          Analyze the gap between Aadhaar enrollments and biometric updates for children aged 5-17 
          to identify districts where mandatory biometric updates are lagging behind.
        </p>
        <Link
          to="/upload"
          className="inline-flex items-center bg-white text-uidai-blue px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
        >
          Get Started
          <ArrowRight className="ml-2" size={20} />
        </Link>
      </div>
      
      {/* Problem Statement */}
      <div className="bg-red-50 border-l-4 border-red-500 rounded-lg p-6 mb-8">
        <div className="flex items-start">
          <AlertTriangle className="text-red-500 mr-4 flex-shrink-0" size={28} />
          <div>
            <h2 className="text-xl font-bold text-red-800 mb-2">The Silent Gap Problem</h2>
            <p className="text-red-700">
              Biometrics must be updated at ages 5 and 15. However, enrollment data often outpaces 
              biometric updates, creating a "Silent Gap" where children have valid Aadhaar numbers 
              but invalid biometrics - risking service disruption.
            </p>
          </div>
        </div>
      </div>
      
      {/* Features */}
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Platform Features</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <Upload className="text-uidai-blue" size={24} />
          </div>
          <h3 className="text-lg font-bold text-gray-800 mb-2">CSV Upload</h3>
          <p className="text-gray-600">
            Upload enrollment and biometric data files with drag-and-drop support.
          </p>
        </div>
        
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <BarChart3 className="text-green-600" size={24} />
          </div>
          <h3 className="text-lg font-bold text-gray-800 mb-2">BLI Analysis</h3>
          <p className="text-gray-600">
            Automatic calculation of Biometric Lag Index per district with risk categorization.
          </p>
        </div>
        
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <MessageCircle className="text-purple-600" size={24} />
          </div>
          <h3 className="text-lg font-bold text-gray-800 mb-2">AI Assistant</h3>
          <p className="text-gray-600">
            Ask natural language questions about your data and get instant insights.
          </p>
        </div>
      </div>
      
      {/* BLI Explanation */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Understanding the Biometric Lag Index (BLI)</h2>
        
        <div className="bg-gray-50 rounded-lg p-4 mb-4 font-mono text-center">
          BLI = (Total Enrollments₅₋₁₇ - Total Biometric Updates₅₋₁₇) / Total Enrollments₅₋₁₇
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-4 rounded-lg bg-green-50 border border-green-200">
            <div className="text-2xl font-bold text-green-600">&lt; 0.1</div>
            <div className="text-sm text-green-800">Low Risk</div>
            <div className="text-xs text-green-600 mt-1">Monitor</div>
          </div>
          <div className="p-4 rounded-lg bg-yellow-50 border border-yellow-200">
            <div className="text-2xl font-bold text-yellow-600">0.1 - 0.3</div>
            <div className="text-sm text-yellow-800">Medium Risk</div>
            <div className="text-xs text-yellow-600 mt-1">Review</div>
          </div>
          <div className="p-4 rounded-lg bg-orange-50 border border-orange-200">
            <div className="text-2xl font-bold text-orange-600">0.3 - 0.5</div>
            <div className="text-sm text-orange-800">High Risk</div>
            <div className="text-xs text-orange-600 mt-1">Plan Intervention</div>
          </div>
          <div className="p-4 rounded-lg bg-red-50 border border-red-200">
            <div className="text-2xl font-bold text-red-600">&gt; 0.5</div>
            <div className="text-sm text-red-800">Critical Risk</div>
            <div className="text-xs text-red-600 mt-1">Immediate Camp</div>
          </div>
        </div>
      </div>
      
      {/* Quick Start */}
      <div className="bg-blue-50 rounded-xl p-6">
        <h2 className="text-xl font-bold text-blue-800 mb-4">Quick Start Guide</h2>
        <ol className="list-decimal list-inside space-y-2 text-blue-700">
          <li>Navigate to <strong>Upload Data</strong> and upload your CSV files</li>
          <li>Wait for processing to complete (usually under 3 seconds)</li>
          <li>View the <strong>Dashboard</strong> to see Top 10 Problem Districts</li>
          <li>Click on any district to see the "Gap Widening Curve"</li>
          <li>Use the <strong>AI Assistant</strong> for natural language queries</li>
        </ol>
      </div>
    </div>
  );
};

export default HomePage;
