import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/agents": "http://localhost:8000",
      "/candidates": "http://localhost:8000",
      "/jobs": "http://localhost:8000",
      "/match": "http://localhost:8000",
      "/match-resume": "http://localhost:8000",
      "/match-job": "http://localhost:8000",
      "/match-resume-ensemble": "http://localhost:8000",
      "/agent": "http://localhost:8000",
      "/system": "http://localhost:8000",
    },
  },
});
