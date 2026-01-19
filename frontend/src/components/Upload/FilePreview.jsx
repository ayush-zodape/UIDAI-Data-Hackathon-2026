import React from 'react';
import { FileText, X } from 'lucide-react';

const FilePreview = ({ file, onRemove }) => {
  if (!file) return null;
  
  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };
  
  return (
    <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
      <div className="flex items-center space-x-3">
        <FileText className="text-blue-500" size={24} />
        <div>
          <p className="font-medium text-gray-800">{file.name}</p>
          <p className="text-sm text-gray-500">{formatFileSize(file.size)}</p>
        </div>
      </div>
      {onRemove && (
        <button
          onClick={onRemove}
          className="text-gray-400 hover:text-red-500 transition-colors"
        >
          <X size={20} />
        </button>
      )}
    </div>
  );
};

export default FilePreview;
