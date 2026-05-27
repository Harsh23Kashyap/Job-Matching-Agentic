import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/agents": "http://localhost:8001",
      "/candidates": "http://localhost:8001",
      "/jobs": "http://localhost:8001",
      "/match": "http://localhost:8001",
      "/match-resume": "http://localhost:8001",
      "/match-job": "http://localhost:8001",
      "/match-resume-ensemble": "http://localhost:8001",
      "/agent": "http://localhost:8001",
      "/system": "http://localhost:8001",
    },
  },
});
