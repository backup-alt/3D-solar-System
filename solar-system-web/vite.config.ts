import { defineConfig } from 'vite'

export default defineConfig({
  base: '/3D-solar-System/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: true,
  }
})
