import React from 'react';
import FileUploader from '../components/Upload/FileUploader';

const UploadPage = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-2">Upload Data Files</h1>
      <p className="text-gray-600 mb-6">
        Upload your enrollment and biometric data files to begin the analysis.
      </p>
      
      <FileUploader />
      
      {/* Data Format Guide */}
      <div className="mt-8 bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-lg font-bold text-gray-800 mb-4">Data Format Guide</h2>
        
        <div className="space-y-4">
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">Enrollment Data CSV</h3>
            <div className="bg-gray-50 rounded-lg p-3 font-mono text-sm overflow-x-auto">
              date, state, district, pincode, age_0_5, age_5_17, age_18_greater
            </div>
          </div>
          
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">Biometric Updates CSV</h3>
            <div className="bg-gray-50 rounded-lg p-3 font-mono text-sm overflow-x-auto">
              date, state, district, pincode, bio_age_5_17, bio_age_17_
            </div>
          </div>
          
          <div>
            <h3 className="font-semibold text-gray-700 mb-2">Demographic Updates CSV (Optional)</h3>
            <div className="bg-gray-50 rounded-lg p-3 font-mono text-sm overflow-x-auto">
              date, state, district, pincode, demo_age_5_17, demo_age_17_
            </div>
          </div>
        </div>
        
        <div className="mt-4 p-4 bg-yellow-50 rounded-lg">
          <p className="text-sm text-yellow-800">
            <strong>Note:</strong> Dates should be in DD-MM-YYYY format (Indian standard). 
            Pincode should be treated as text to preserve leading zeros.
          </p>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
