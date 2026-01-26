import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue2";
import path from "path";
import { NodeModulesPolyfillPlugin } from "@esbuild-plugins/node-modules-polyfill";
import { NodeGlobalsPolyfillPlugin } from "@esbuild-plugins/node-globals-polyfill";

export default defineConfig(({ mode }) => ({
  define:
    mode === "production"
      ? {
          // Caddy templates replaces these at serve-time (production only).
          // Use very-unique custom delimiters to avoid collisions with:
          // - Go templates default `{{ ... }}` sequences in minified bundles
          // - JS libs that embed `<% ... %>`-style templates (lodash/underscore, etc.)
          "import.meta.env.VITE_AXIOS_BASE_URL": JSON.stringify(
            '___CADDY_TEMPLATE_START___ env "VITE_AXIOS_BASE_URL" ___CADDY_TEMPLATE_END___'
          ),
          "import.meta.env.VITE_VECTOR_TILE_BASE_URL": JSON.stringify(
            '___CADDY_TEMPLATE_START___ env "VITE_VECTOR_TILE_BASE_URL" ___CADDY_TEMPLATE_END___'
          ),
        }
      : {},
  plugins: [
    vue(),
    NodeGlobalsPolyfillPlugin({
      process: true,
      buffer: true,
    }),
  ],
  server: {
    port: 8080,
    strictPort: true,
    host: true,
    allowedHosts: [
      "https://gwells-frontend-26e83e-prod.apps.silver.devops.gov.bc.ca",
      "https://gwells-backend-26e83e-prod.apps.silver.devops.gov.bc.ca",
      "localhost",
      "https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer/tile/*",
      "https://gwells.apps.silver.devops.gov.bc.ca/gwells/tiles/*",
    ],
    cors: {
      origin: [
        "https://gwells-frontend-26e83e-prod.apps.silver.devops.gov.bc.ca",
        "https://gwells-frontend-26e83e-dev.apps.silver.devops.gov.bc.ca",
        "https://gwells-backend-26e83e-prod.apps.silver.devops.gov.bc.ca",
        "https://gwells-staging.apps.silver.devops.gov.bc.ca",
        "https://gwells.apps.silver.devops.gov.bc.ca",
        "https://maps.gov.bc.ca",
      ],
      credentials: true,
    },
  },
  preview: {
    port: 8080,
    strictPort: true,
    host: true,
    allowedHosts: [
      "https://gwells-frontend-26e83e-prod.apps.silver.devops.gov.bc.ca",
      "https://gwells-backend-26e83e-prod.apps.silver.devops.gov.bc.ca",
      "localhost",
      "https://maps.gov.bc.ca/arcserver/rest/services/Province/roads_wm/MapServer/tile/*",
      "https://gwells.apps.silver.devops.gov.bc.ca/gwells/tiles/*",
    ],
    cors: {
      origin: [
        "https://gwells-frontend-26e83e-prod.apps.silver.devops.gov.bc.ca",
        "https://gwells-frontend-26e83e-dev.apps.silver.devops.gov.bc.ca",
        "https://gwells-backend-26e83e-prod.apps.silver.devops.gov.bc.ca",
        "https://gwells-staging.apps.silver.devops.gov.bc.ca",
        "https://gwells.apps.silver.devops.gov.bc.ca",
        "https://maps.gov.bc.ca",
      ],
      credentials: true,
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
      util: "rollup-plugin-node-polyfills/polyfills/util",
      buffer: "rollup-plugin-node-polyfills/polyfills/buffer-es6",
      events: "rollup-plugin-node-polyfills/polyfills/events",
      process: "rollup-plugin-node-polyfills/polyfills/process-es6",
      stream: "rollup-plugin-node-polyfills/polyfills/stream",
      string_decoder: "rollup-plugin-node-polyfills/polyfills/string-decoder",
    },
    extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
  },
  css: {
    preprocessorOptions: {
      scss: {
        // If you need any global SCSS variables or imports
        // additionalData: `@import "./src/common/variables.scss";`
      },
    },
  },
  optimizeDeps: {
    esbuildOptions: {
      plugins: [NodeModulesPolyfillPlugin()],
    },
  },
}));
