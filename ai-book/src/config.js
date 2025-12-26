// API Configuration
const config = {
  // Backend API URL - safe for SSR
  API_BASE_URL: 'https://hussain3241-ai-book-backend.hf.space',

  // Fallback to localhost for development
  get backendUrl() {
    // Check if we're in browser environment
    if (typeof window === 'undefined') {
      return this.API_BASE_URL;
    }

    // Use environment variable if available
    if (window.REACT_APP_BACKEND_URL) {
      return window.REACT_APP_BACKEND_URL;
    }

    // Auto-detect localhost for development
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:8001';
    }

    return this.API_BASE_URL;
  }
};

export default config;
