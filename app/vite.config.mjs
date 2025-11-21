/* eslint-env node */
/* global process */
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(process.cwd(), './src'), // Replaced __dirname for ESM compatibility
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: ['frontend'],
    proxy: {
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
      '/static': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
      '/admin': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
});
