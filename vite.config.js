import path from 'path';

import { defineConfig } from 'vite'
import preact from '@preact/preset-vite'


// https://vite.dev/config/
export default defineConfig({
  plugins: [preact()],
  resolve: {
    alias: {
      // '@': path.resolve(__dirname, 'src'),
      'src': path.resolve(__dirname, 'src'),
    },
  },
})
