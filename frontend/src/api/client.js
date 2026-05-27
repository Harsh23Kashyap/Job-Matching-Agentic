import axios from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL || "";

export const api = axios.create({ baseURL, headers: { "Content-Type": "application/json" } });

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
