import { resolve } from 'path';
import { defineConfig } from 'vite';


export default defineConfig({
    base: 'tg/',
    build: {

        rollupOptions: {
            input: {
                auth: resolve(__dirname, 'auth.html')
            }
        },
    },
});
