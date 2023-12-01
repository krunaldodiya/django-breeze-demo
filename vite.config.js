import vue from "@vitejs/plugin-vue";
import path from "path";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [
    vue({
      template: {
        transformAssetUrls: {
          base: null,
          includeAbsolute: false,
        },
      },
    }),
  ],
  resolve: {
    alias: {
      "@": path.resolve("resources/js"),
    },
  },
  base: "/static/",
  publicDir: false,
  build: {
    manifest: true,
    outDir: "static/build",
    rollupOptions: {
      input: {
        js: path.resolve(__dirname, "resources/js/app.js"),
        css: path.resolve(__dirname, "resources/css/app.css"),
      },
    },
    assetsInlineLimit: 0,
  },
});
