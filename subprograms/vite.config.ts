import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
    plugins: [react()],
    build: {
        outDir: 'dist',
        rollupOptions: {
            input: {
                'hit-and-blow': resolve(__dirname, 'hit-and-blow/index.html'),
                'hello-world': resolve(__dirname, 'hello-world/index.html'),
            },
            output: {
                entryFileNames: 'assets/[name].js',
                chunkFileNames: 'assets/[name].js',
                assetFileNames: 'assets/[name].[ext]'
            }
        }
    }
})