import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { uploadFiles } from '../../services/api';
import useDataStore from '../../store/useDataStore';

const FileUploader = () => {
  const [files, setFiles] = useState({
    enrollment: null,
    biometric: null,
    demographic: null
  });
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  
  const { setUploadStatus } = useDataStore();
  
  const onDropEnrollment = useCallback((acceptedFiles) => {
    setFiles(prev => ({ ...prev, enrollment: acceptedFiles[0] }));
  }, []);
  
  const onDropBiometric = useCallback((acceptedFiles) => {
    setFiles(prev => ({ ...prev, biometric: acceptedFiles[0] }));
  }, []);
  
  const onDropDemographic = useCallback((acceptedFiles) => {
    setFiles(prev => ({ ...prev, demographic: acceptedFiles[0] }));
  }, []);
  
  const handleUpload = async () => {
    if (!files.enrollment || !files.biometric) {
      setError('Please upload both Enrollment and Biometric files');
      return;
    }
    
    setUploading(true);
    setError(null);
    
    try {
      const result = await uploadFiles(files.enrollment, files.biometric, files.demographic);
      setSuccess(true);
      setUploadStatus({
        enrollment: true,
        biometric: true,
        demographic: !!files.demographic
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please check your files.');
    } finally {
      setUploading(false);
    }
  };
  
  const DropZone = ({ onDrop, file, label, required }) => {
    const { getRootProps, getInputProps, isDragActive } = useDropzone({
      onDrop,
      accept: { 'text/csv': ['.csv'] },
      maxFiles: 1
    });
    
    return (
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
          isDragActive ? 'border-uidai-blue bg-blue-50' : 'border-gray-300 hover:border-gray-400'
        } ${file ? 'bg-green-50 border-green-500' : ''}`}
      >
        <input {...getInputProps()} />
        {file ? (
          <div className="flex items-center justify-center space-x-2 text-green-600">
            <CheckCircle size={24} />
            <span>{file.name}</span>
          </div>
        ) : (
          <>
            <Upload className="mx-auto text-gray-400 mb-2" size={32} />
            <p className="text-gray-600">{label}</p>
            {required && <span className="text-red-500 text-sm">*Required</span>}
          </>
        )}
      </div>
    );
  };
  
  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-6">Upload CSV Files</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <DropZone
          onDrop={onDropEnrollment}
          file={files.enrollment}
          label="Enrollment Data"
          required
        />
        <DropZone
          onDrop={onDropBiometric}
          file={files.biometric}
          label="Biometric Updates"
          required
        />
        <DropZone
          onDrop={onDropDemographic}
          file={files.demographic}
          label="Demographic Updates (Optional)"
        />
      </div>
      
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-4 flex items-center">
          <AlertCircle className="mr-2" size={20} />
          {error}
        </div>
      )}
      
      {success && (
        <div className="bg-green-50 text-green-600 p-4 rounded-lg mb-4 flex items-center">
          <CheckCircle className="mr-2" size={20} />
          Files uploaded successfully! Navigate to Dashboard to view analysis.
        </div>
      )}
      
      <button
        onClick={handleUpload}
        disabled={uploading || !files.enrollment || !files.biometric}
        className={`w-full py-3 rounded-lg font-semibold transition-colors ${
          uploading || !files.enrollment || !files.biometric
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : 'bg-uidai-blue text-white hover:bg-blue-700'
        }`}
      >
        {uploading ? 'Uploading...' : 'Upload and Analyze'}
      </button>
      
      <div className="mt-4 text-sm text-gray-500">
        <p><strong>Expected columns:</strong></p>
        <ul className="list-disc list-inside">
          <li>Enrollment: date, state, district, pincode, age_5_17</li>
          <li>Biometric: date, state, district, pincode, bio_age_5_17</li>
        </ul>
      </div>
    </div>
  );
};

export default FileUploader;
