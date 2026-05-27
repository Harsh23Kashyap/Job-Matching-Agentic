import { useEffect, useState } from "react";
import { fetchCandidates, fetchJobs } from "../api/client.js";

const DEFAULT_ENSEMBLE = [
  { strategy: "semantic", metric: "cosine", weight: 1.0, skills_mode: "jaccard", semantic_weight: 0.7 },
  { strategy: "multimodal", metric: "cosine", weight: 1.0, skills_mode: "jaccard", semantic_weight: 0.7 },
  { strategy: "semantic", metric: "euclidean", weight: 1.0, skills_mode: "jaccard", semantic_weight: 0.7 },
  { strategy: "multimodal", metric: "cosine", weight: 1.0, skills_mode: "embedding", semantic_weight: 0.7 },
];

const STORAGE_KEY = "jm_match_config";

function loadSavedConfig() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export default function MatchControls({ onRun, onDailyBatch, loading }) {
  const saved = loadSavedConfig();
  const [mode, setMode] = useState(saved?.mode || "candidate_to_jobs");
  const [queryKey, setQueryKey] = useState(saved?.queryKey || "");
  const [strategy, setStrategy] = useState(saved?.strategy || "semantic");
  const [metric, setMetric] = useState(saved?.metric || "cosine");
  const [skillsMode, setSkillsMode] = useState(saved?.skillsMode || "jaccard");
  const [semanticWeight, setSemanticWeight] = useState(saved?.semanticWeight ?? 0.7);
  const [topK, setTopK] = useState(saved?.topK ?? 5);
  const [ensemble, setEnsemble] = useState(saved?.ensemble ?? false);
  const [ensembleChecks, setEnsembleChecks] = useState(saved?.ensembleChecks ?? [true, true, true, true]);
  const [names, setNames] = useState([]);
  const [titles, setTitles] = useState([]);

  useEffect(() => {
    Promise.all([fetchCandidates(), fetchJobs()]).then(([n, t]) => {
      setNames(n);
      setTitles(t);
      if (!queryKey) {
        setQueryKey(mode === "candidate_to_jobs" ? n[0] || "" : t[0] || "");
      }
    });
  }, []);

  useEffect(() => {
    const config = {
      mode,
      queryKey,
      strategy,
      metric,
      skillsMode,
      semanticWeight,
      topK,
      ensemble,
      ensembleChecks,
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(config));
  }, [mode, queryKey, strategy, metric, skillsMode, semanticWeight, topK, ensemble, ensembleChecks]);

  const handleModeChange = (next) => {
    setMode(next);
    setQueryKey(next === "candidate_to_jobs" ? names[0] || "" : titles[0] || "");
  };

  const buildConfig = () => {
    const searches = DEFAULT_ENSEMBLE.filter((_, i) => ensembleChecks[i]);
    return {
      mode,
      queryKey,
      strategy,
      metric,
      skillsMode,
      semanticWeight,
      topK,
      ensemble: ensemble && mode === "candidate_to_jobs",
      searches,
    };
  };

  return (
    <section className="panel controls-panel">
      <h2>Match Controls</h2>
      <div className="controls-grid">
        <label>
          Direction
          <select value={mode} onChange={(e) => handleModeChange(e.target.value)}>
            <option value="candidate_to_jobs">Resume → Jobs</option>
            <option value="job_to_candidates">Job → Candidates</option>
          </select>
        </label>

        <label>
          {mode === "candidate_to_jobs" ? "Candidate" : "Job title"}
          <select value={queryKey} onChange={(e) => setQueryKey(e.target.value)}>
            {(mode === "candidate_to_jobs" ? names : titles).map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>

        <label>
          Strategy
          <select value={strategy} onChange={(e) => setStrategy(e.target.value)} disabled={ensemble}>
            <option value="semantic">Semantic</option>
            <option value="multimodal">Multimodal</option>
          </select>
        </label>

        <label>
          Metric
          <select value={metric} onChange={(e) => setMetric(e.target.value)} disabled={ensemble}>
            <option value="cosine">Cosine</option>
            <option value="euclidean">Euclidean</option>
          </select>
        </label>

        <label>
          Skills mode
          <select value={skillsMode} onChange={(e) => setSkillsMode(e.target.value)} disabled={ensemble}>
            <option value="jaccard">Jaccard</option>
            <option value="embedding">Soft embedding</option>
          </select>
        </label>

        <label>
          Semantic weight
          <input
            type="number"
            min="0"
            max="1"
            step="0.05"
            value={semanticWeight}
            onChange={(e) => setSemanticWeight(Number(e.target.value))}
            disabled={ensemble || strategy === "semantic"}
          />
        </label>

        <label>
          Top K
          <input type="number" min="1" max="15" value={topK} onChange={(e) => setTopK(Number(e.target.value))} />
        </label>

        {mode === "candidate_to_jobs" && (
          <label className="checkbox-row">
            <input type="checkbox" checked={ensemble} onChange={(e) => setEnsemble(e.target.checked)} />
            Ensemble (RRF)
          </label>
        )}
      </div>

      {ensemble && mode === "candidate_to_jobs" && (
        <div className="ensemble-box">
          <p>Ensemble searches</p>
          {DEFAULT_ENSEMBLE.map((s, i) => (
            <label key={i} className="checkbox-row">
              <input
                type="checkbox"
                checked={ensembleChecks[i]}
                onChange={(e) => {
                  const next = [...ensembleChecks];
                  next[i] = e.target.checked;
                  setEnsembleChecks(next);
                }}
              />
              {s.strategy} / {s.metric}
              {s.skills_mode !== "jaccard" ? ` / ${s.skills_mode}` : ""}
            </label>
          ))}
        </div>
      )}

      <div className="actions">
        <button type="button" disabled={loading || !queryKey} onClick={() => onRun(buildConfig())}>
          {loading ? "Running…" : "Run match"}
        </button>
        <button type="button" disabled={loading} onClick={() => onDailyBatch(buildConfig())}>
          Daily batch
        </button>
      </div>
    </section>
  );
}
