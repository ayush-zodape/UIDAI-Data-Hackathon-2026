import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

export const uploadFiles = async (enrollmentFile, biometricFile, demographicFile = null) => {
  const formData = new FormData();
  formData.append('enrollment', enrollmentFile);
  formData.append('biometric', biometricFile);
  if (demographicFile) {
    formData.append('demographic', demographicFile);
  }
  
  const response = await api.post('/upload/files', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const getUploadStatus = async () => {
  const response = await api.get('/upload/status');
  return response.data;
};

export const computeBLI = async () => {
  const response = await api.get('/analysis/compute-bli');
  return response.data;
};

export const getGapWidening = async (district) => {
  const response = await api.get(`/analysis/gap-widening/${encodeURIComponent(district)}`);
  return response.data;
};

export const getSeasonality = async () => {
  const response = await api.get('/analysis/seasonality');
  return response.data;
};

export const getStateSummary = async () => {
  const response = await api.get('/analysis/state-summary');
  return response.data;
};

export const askQuestion = async (message) => {
  const response = await api.post('/chat/ask', { message });
  return response.data;
};

export default api;
