import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "";

export const api = axios.create({
  baseURL,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

/** Parse FastAPI/axios errors for auth forms. */
export function apiErrorMessage(err, fallback) {
  const status = err.response?.status;
  const detail = err.response?.data?.detail;
  if (status === 404) {
    return "Auth API not found — restart the backend on port 8001 (v1.1+).";
  }
  if (typeof detail === "object" && detail?.error) return detail.error;
  if (typeof detail === "string") return detail;
  if (err.message === "Network Error") {
    return "Cannot reach the API — is the backend running on port 8001?";
  }
  return fallback;
}

export async function fetchMe() {
  const { data } = await api.get("/auth/me");
  return data;
}

export async function login(email, password) {
  const { data } = await api.post("/auth/login", { email, password });
  return data;
}

export async function register(email, password, role) {
  const { data } = await api.post("/auth/register", { email, password, role });
  return data;
}

export async function logout() {
  await api.post("/auth/logout");
}

export async function fetchAgentStatus() {
  const { data } = await api.get("/agents/status");
  return data;
}

export async function fetchCandidates() {
  const { data } = await api.get("/candidates");
  return data.names;
}

export async function fetchJobs() {
  const { data } = await api.get("/jobs");
  return data.titles;
}

export async function fetchMyProfile() {
  const { data } = await api.get("/candidates/me");
  return data;
}

export async function fetchMyJobs() {
  const { data } = await api.get("/jobs/mine");
  return data;
}

export async function uploadResume(file) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/candidates/upload-resume", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function saveCandidateProfile(profile) {
  const { data } = await api.post("/candidates", profile);
  return data;
}

export async function saveJobPosting(job) {
  const { data } = await api.post("/jobs", job);
  return data;
}

export async function runMatch(config) {
  const path =
    config.mode === "candidate_to_jobs"
      ? config.ensemble
        ? "/match/ensemble"
        : "/match/candidate-to-jobs"
      : "/match/job-to-candidates";

  const body = config.ensemble
    ? {
        query_key: config.queryKey,
        top_k: config.topK,
        searches: config.searches,
        retrieval: "exhaustive",
      }
    : {
        query_key: config.queryKey,
        top_k: config.topK,
        strategy: config.strategy,
        metric: config.metric,
        skills_mode: config.skillsMode,
        semantic_weight: config.semanticWeight,
        retrieval: "exhaustive",
      };

  const { data } = await api.post(path, body);
  return data;
}

export async function runDailyBatch(config) {
  const { data } = await api.post("/match/daily-batch", {
    top_k: config.topK,
    strategy: config.strategy,
    metric: config.metric,
    skills_mode: config.skillsMode,
    semantic_weight: config.semanticWeight,
    candidate_pool: 120,
  });
  return data;
}
