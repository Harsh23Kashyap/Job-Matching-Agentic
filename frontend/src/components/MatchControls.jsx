import { useEffect, useState } from "react";
import { fetchCandidates, fetchJobs } from "../api/client.js";
import { IconMatch } from "./icons.jsx";

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
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ mode, queryKey, strategy, metric, skillsMode, semanticWeight, topK, ensemble, ensembleChecks })
    );
  }, [mode, queryKey, strategy, metric, skillsMode, semanticWeight, topK, ensemble, ensembleChecks]);

  const handleModeChange = (next) => {
    setMode(next);
    setQueryKey(next === "candidate_to_jobs" ? names[0] || "" : titles[0] || "");
  };

  const buildConfig = () => ({
    mode,
    queryKey,
    strategy,
    metric,
    skillsMode,
    semanticWeight,
    topK,
    ensemble: ensemble && mode === "candidate_to_jobs",
    searches: DEFAULT_ENSEMBLE.filter((_, i) => ensembleChecks[i]),
  });

  return (
    <section className="panel span-5">
      <div className="panel-header">
        <IconMatch size={18} />
        <h2>Match Controls</h2>
      </div>

      <div className="control-section">
        <p className="control-section-title">Direction</p>
        <div className="pill-group">
          <button
            type="button"
            className={`pill-option ${mode === "candidate_to_jobs" ? "active" : ""}`}
            onClick={() => handleModeChange("candidate_to_jobs")}
          >
            Resume → Jobs
          </button>
          <button
            type="button"
            className={`pill-option ${mode === "job_to_candidates" ? "active" : ""}`}
            onClick={() => handleModeChange("job_to_candidates")}
          >
            Job → Candidates
          </button>
        </div>
      </div>

      <div className="control-section">
        <p className="control-section-title">Query</p>
        <div className="field">
          <label htmlFor="query-select">{mode === "candidate_to_jobs" ? "Candidate" : "Job title"}</label>
          <select id="query-select" value={queryKey} onChange={(e) => setQueryKey(e.target.value)}>
            {(mode === "candidate_to_jobs" ? names : titles).map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="control-section">
        <p className="control-section-title">Strategy</p>
        <div className="controls-grid">
          <div className="field">
            <label htmlFor="strategy">Algorithm</label>
            <select id="strategy" value={strategy} onChange={(e) => setStrategy(e.target.value)} disabled={ensemble}>
              <option value="semantic">Semantic</option>
              <option value="multimodal">Multimodal</option>
            </select>
          </div>
          <div className="field">
            <label htmlFor="metric">Metric</label>
            <select id="metric" value={metric} onChange={(e) => setMetric(e.target.value)} disabled={ensemble}>
              <option value="cosine">Cosine</option>
              <option value="euclidean">Euclidean</option>
            </select>
          </div>
          <div className="field">
            <label htmlFor="skills">Skills mode</label>
            <select id="skills" value={skillsMode} onChange={(e) => setSkillsMode(e.target.value)} disabled={ensemble}>
              <option value="jaccard">Jaccard</option>
              <option value="embedding">Soft embedding</option>
            </select>
          </div>
          <div className="field">
            <label htmlFor="weight">Semantic weight</label>
            <input
              id="weight"
              type="number"
              min="0"
              max="1"
              step="0.05"
              value={semanticWeight}
              onChange={(e) => setSemanticWeight(Number(e.target.value))}
              disabled={ensemble || strategy === "semantic"}
            />
          </div>
          <div className="field">
            <label htmlFor="topk">Top K</label>
            <input id="topk" type="number" min="1" max="15" value={topK} onChange={(e) => setTopK(Number(e.target.value))} />
          </div>
          {mode === "candidate_to_jobs" && (
            <label className="checkbox-row" style={{ alignSelf: "end", paddingBottom: 8 }}>
              <input type="checkbox" checked={ensemble} onChange={(e) => setEnsemble(e.target.checked)} />
              Ensemble (RRF)
            </label>
          )}
        </div>
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
        <button type="button" className="btn-primary" disabled={loading || !queryKey} onClick={() => onRun(buildConfig())}>
          {loading ? "Running…" : "Run match"}
        </button>
        <button type="button" className="btn-secondary" disabled={loading} onClick={() => onDailyBatch(buildConfig())}>
          Daily batch
        </button>
      </div>
    </section>
  );
}
