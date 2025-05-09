import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import istanbul from 'vite-plugin-istanbul';

export default defineConfig({
  plugins: [
    react(),
    istanbul({
      include: 'src/*', // Instrumenta solo el código en src/
      exclude: ['node_modules', 'test/', 'cypress/'],
      extension: ['.js', '.jsx', '.ts', '.tsx'],
      requireEnv: false, // Habilita instrumentación sin variable de entorno
    }),
  ],
});