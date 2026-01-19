/**
 * Utility functions for formatting data
 */

/**
 * Format a number with thousand separators
 */
export const formatNumber = (num) => {
  if (num === null || num === undefined) return 'N/A';
  return num.toLocaleString();
};

/**
 * Format a BLI score to 4 decimal places
 */
export const formatBLI = (score) => {
  if (score === null || score === undefined) return 'N/A';
  return score.toFixed(4);
};

/**
 * Format a date string to Indian locale
 */
export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

/**
 * Format file size in human readable format
 */
export const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
};

/**
 * Get risk level color class based on BLI score
 */
export const getRiskColorClass = (bli) => {
  if (bli < 0.1) return 'text-green-600 bg-green-50';
  if (bli < 0.3) return 'text-yellow-600 bg-yellow-50';
  if (bli < 0.5) return 'text-orange-600 bg-orange-50';
  return 'text-red-600 bg-red-50';
};

/**
 * Get risk level label based on BLI score
 */
export const getRiskLevel = (bli) => {
  if (bli < 0.1) return 'Low';
  if (bli < 0.3) return 'Medium';
  if (bli < 0.5) return 'High';
  return 'Critical';
};

/**
 * Truncate text with ellipsis
 */
export const truncateText = (text, maxLength = 20) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};
