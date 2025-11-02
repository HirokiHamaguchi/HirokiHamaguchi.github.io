import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
    plugins: [react()],
    build: {
        outDir: '../_program/dist',
        rollupOptions: {
            input: {
                'hit-and-blow': resolve(__dirname, 'hit-and-blow/index.html'),
                'text-tools': resolve(__dirname, 'text-tools/index.html'),
            },
            output: {
                entryFileNames: 'assets/[name].js',
                chunkFileNames: 'assets/[name].js',
                assetFileNames: 'assets/[name].[ext]'
            }
        }
    }
})