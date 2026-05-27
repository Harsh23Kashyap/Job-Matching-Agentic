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

export async function fetchSystemConfig() {
  const { data } = await api.get("/system/config");
  return data;
}

export async function setVectorStore(vectorStore) {
  const { data } = await api.post("/system/vector-store", { vector_store: vectorStore });
  return data;
}

export async function fetchAgentStatus() {
  const { data } = await api.get("/agents/status");
  return data;
}

export async function fetchAgentEvents() {
  const { data } = await api.get("/agents/events/recent");
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

export async function updateCandidateProfile(profile) {
  const { data } = await api.put("/candidates/me", profile);
  return data;
}

/** Create or update the logged-in candidate profile. */
export async function upsertCandidateProfile(profile) {
  try {
    const existing = await fetchMyProfile();
    if (existing?.id) {
      return updateCandidateProfile({ ...profile, id: existing.id });
    }
  } catch (err) {
    if (err.response?.status !== 404) throw err;
  }
  return saveCandidateProfile(profile);
}

export async function uploadJobDescription(file) {
  const form = new FormData();
  form.append("file", file);
  const { data } = await api.post("/jobs/upload-description", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export async function saveJobPosting(job) {
  const { data } = await api.post("/jobs", job);
  return data;
}

/** Default ML pipeline for candidate job search. */
export const DEFAULT_CANDIDATE_MATCH = {
  mode: "candidate_to_jobs",
  topK: 10,
  strategy: "multimodal",
  metric: "cosine",
  skillsMode: "jaccard",
  semanticWeight: 0.7,
  ensemble: false,
  fusionMode: "learned",
  applyConstraints: true,
  autoStrategy: true,
  useCalibration: true,
  useFeedbackBoost: true,
  explainMode: "llm",
};

export const DEFAULT_EMPLOYER_MATCH = {
  mode: "job_to_candidates",
  topK: 10,
  strategy: "multimodal",
  metric: "cosine",
  skillsMode: "jaccard",
  semanticWeight: 0.7,
  ensemble: false,
  fusionMode: "learned",
  applyConstraints: true,
  autoStrategy: false,
  useCalibration: true,
  useFeedbackBoost: false,
  explainMode: "rules",
};

export async function fetchSavedJobs() {
  const { data } = await api.get("/candidates/me/saved-jobs");
  return data.saved_jobs || [];
}

export async function updateSavedJob(jobId, jobTitle, saved) {
  const { data } = await api.put("/candidates/me/saved-jobs", {
    job_id: jobId,
    job_title: jobTitle,
    saved,
  });
  return data;
}

export async function fetchMyApplications() {
  const { data } = await api.get("/candidates/me/applications");
  return data.applications || [];
}

export async function createApplication(jobId, jobTitle, matchScore) {
  const { data } = await api.post("/candidates/me/applications", {
    job_id: jobId,
    job_title: jobTitle,
    match_score: matchScore,
  });
  return data;
}

export async function fetchEmployerApplications() {
  const { data } = await api.get("/jobs/mine/applications");
  return data.applications || [];
}

export async function fetchFairnessReport() {
  const { data } = await api.get("/system/fairness");
  return data;
}

export async function runMatch(config) {
  const path =
    config.mode === "candidate_to_jobs"
      ? config.ensemble
        ? "/match/ensemble"
        : "/match/candidate-to-jobs"
      : "/match/job-to-candidates";

  const mlFlags = {
    fusion_mode: config.fusionMode || "fixed",
    apply_constraints: Boolean(config.applyConstraints),
    auto_strategy: Boolean(config.autoStrategy),
    use_calibration: Boolean(config.useCalibration),
    use_feedback_boost: Boolean(config.useFeedbackBoost),
    explain_mode: config.explainMode || "rules",
    use_cross_encoder: Boolean(config.useCrossEncoder),
  };

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
        ...mlFlags,
      };

  const { data } = await api.post(path, body);
  return data;
}

export async function recordFeedback(candidateId, jobId, action) {
  const { data } = await api.post("/feedback", {
    candidate_id: candidateId,
    job_id: jobId,
    action,
  });
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
