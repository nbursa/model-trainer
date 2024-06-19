import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import * as dotenv from 'dotenv';

dotenv.config();

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL,
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
