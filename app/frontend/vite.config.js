import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue2'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000 // Change if needed
  },
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
