// Same-origin by default: in production the FastAPI backend serves the built
// frontend, so relative URLs hit the same host/port the page was loaded from.
// This works on localhost, 127.0.0.1 AND LAN access (http://192.168.x.x:8000)
// without CORS preflights. During `npm run dev`, Vite proxies the backend
// routes to 127.0.0.1:8000 (see vite.config.ts), so relative URLs work too.
// Set VITE_API_BASE_URL only if the API is intentionally hosted elsewhere.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";
