// API Configuration
const config = {
  // Backend API URL
  API_BASE_URL: window.REACT_APP_BACKEND_URL || 'https://hussain3241-ai-book-backend.hf.space',

  // Fallback to localhost for development
  get backendUrl() {
    if (window.location.hostname === 'localhost') {
      return 'http://localhost:8001';
    }
    return this.API_BASE_URL;
  }
};

export default config;
