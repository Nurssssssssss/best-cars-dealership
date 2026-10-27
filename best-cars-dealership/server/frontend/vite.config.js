import { defineConfig } from 'vite';
export default defineConfig(({command}) => ({
  base: command === 'build' ? '/static/' : '/',
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/admin': 'http://127.0.0.1:8000',
      '/static': 'http://127.0.0.1:8000'
    }
  },
  build: {outDir: 'dist'}
}));
