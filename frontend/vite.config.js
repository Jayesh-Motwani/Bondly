import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Vite configuration for LoveGuru frontend
// Enables React JSX and sets up the development server
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // Proxy API requests to the Python backend
    proxy: {
      '/query': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
