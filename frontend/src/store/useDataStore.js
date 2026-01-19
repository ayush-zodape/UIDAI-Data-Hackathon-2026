import { create } from 'zustand';

const useDataStore = create((set, get) => ({
  // Upload state
  isDataLoaded: false,
  uploadStatus: {
    enrollment: false,
    biometric: false,
    demographic: false
  },
  
  // Analysis results
  analysisResults: null,
  topDistricts: [],
  overallBLI: 0,
  dateRange: { start: '', end: '' },
  
  // Selected district for detail view
  selectedDistrict: null,
  gapWideningData: null,
  
  // Chat history
  chatHistory: [],
  
  // Actions
  setUploadStatus: (status) => set({ uploadStatus: status, isDataLoaded: status.enrollment && status.biometric }),
  
  setAnalysisResults: (results) => set({
    analysisResults: results,
    topDistricts: results.top_problem_districts,
    overallBLI: results.overall_bli,
    dateRange: results.date_range
  }),
  
  setSelectedDistrict: (district) => set({ selectedDistrict: district }),
  
  setGapWideningData: (data) => set({ gapWideningData: data }),
  
  addChatMessage: (message) => set((state) => ({
    chatHistory: [...state.chatHistory, message]
  })),
  
  clearChatHistory: () => set({ chatHistory: [] }),
  
  reset: () => set({
    isDataLoaded: false,
    uploadStatus: { enrollment: false, biometric: false, demographic: false },
    analysisResults: null,
    topDistricts: [],
    overallBLI: 0,
    selectedDistrict: null,
    gapWideningData: null,
    chatHistory: []
  })
}));

export default useDataStore;
