import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
      manifest: {
        name: 'MBAS - Modern Business Automation System',
        short_name: 'MBAS',
        description: 'Offline-first business management for inventory, billing, and reports - A Product of Z&T Technologies',
        theme_color: '#ffffff',
        background_color: '#ffffff',
        display: 'standalone',
        orientation: 'portrait-primary',
        scope: '/',
        start_url: '/',
        icons: [
          {
            src: 'pwa-64x64.png',
            sizes: '64x64',
            type: 'image/png'
          },
          {
            src: 'pwa-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any'
          },
          {
            src: 'maskable-icon-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'
          }
        ]
      },
      workbox: {
        // Precache the app shell (JS/CSS/HTML/icons) for instant loads and
        // offline shell availability. API responses are NEVER cached: business
        // data (stock, sales, settings) must always come from the local
        // backend. The previous runtimeCaching rules cached every backend GET
        // for 30 days (the NetworkFirst "/api/*" rule matched no real route),
        // which served stale data and doubled request traffic on every
        // navigation — a primary cause of the tab-switch hangs.
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff,woff2}'],
        // Don't let the SPA navigation fallback hijack direct requests to
        // backend routes (CSV downloads, API docs, health checks).
        navigateFallbackDenylist: [
          /^\/(auth|settings|inventory|billing|dashboard|suppliers|purchases|reports|system|ai|users|health|version|docs|redoc|openapi\.json)/
        ]
      },
      devOptions: {
        enabled: false // No SW in dev: avoids cache confusion while debugging
      }
    })
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    // Dev-only proxy: the app uses relative API URLs (same-origin in
    // production where FastAPI serves the built frontend). In dev, forward
    // backend routes from the Vite server to uvicorn on 127.0.0.1:8000.
    //
    // Several of these path prefixes (/dashboard, /billing, /settings,
    // /reports, /users, /inventory, /suppliers, /purchases) are ALSO
    // frontend SPA route names. Without `bypass`, a hard navigation or
    // refresh on one of those pages matches the proxy rule and gets
    // forwarded to the backend instead of Vite's own index.html — the
    // backend then serves its production `dist/index.html` static-file
    // fallback (hashed asset paths that don't exist under `vite dev`),
    // producing a blank page. `bypass` lets navigation requests
    // (Accept: text/html) fall through to Vite's SPA handling, while
    // actual API/XHR calls still proxy to the backend.
    proxy: Object.fromEntries(
      [
        '/auth', '/settings', '/inventory', '/billing', '/dashboard',
        '/suppliers', '/purchases', '/reports', '/system', '/ai',
        '/users', '/version', '/health'
      ].map((route) => [
        route,
        {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          bypass: (req: import('http').IncomingMessage) => {
            if (req.headers.accept?.includes('text/html')) {
              return req.url;
            }
          },
        },
      ])
    ),
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          'vendor-ui': [
            '@radix-ui/react-dialog',
            '@radix-ui/react-dropdown-menu',
            '@radix-ui/react-select',
            '@radix-ui/react-avatar',
            '@radix-ui/react-label',
            '@radix-ui/react-scroll-area',
            '@radix-ui/react-separator',
            '@radix-ui/react-slot',
            '@radix-ui/react-tabs'
          ],
          'vendor-table': ['@tanstack/react-table'],
          'vendor-utils': ['axios', 'framer-motion', 'sonner', 'clsx', 'tailwind-merge']
        }
      }
    },
    chunkSizeWarningLimit: 300,
    sourcemap: false, // Disable sourcemaps in production for smaller bundle
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.log in production
      }
    }
  },
  optimizeDeps: {
    include: ['react', 'react-dom', 'axios', 'react-router-dom'],
  },
})
