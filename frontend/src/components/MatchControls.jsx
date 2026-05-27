import { useEffect, useState } from "react";
import { fetchCandidates, fetchJobs, fetchSystemConfig } from "../api/client.js";
import { IconMatch } from "./icons.jsx";

const DEFAULT_ENSEMBLE = [
  { strategy: "semantic", metric: "cosine", weight: 1.0, skills_mode: "jaccard", semantic_weight: 0.7 },
  { strategy: "multimodal", metric: "cosine", weight: 1.0, skills_mode: "jaccard", semantic_weight: 0.7 },
  { strategy: "semantic", metric: "euclidean", weight: 1.0, skills_mode: "jaccard", semantic_weight: 0.7 },
  { strategy: "multimodal", metric: "cosine", weight: 1.0, skills_mode: "embedding", semantic_weight: 0.7 },
];

function defaultEnsembleWeights() {
  return DEFAULT_ENSEMBLE.map((s) => s.weight);
}

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
  const [ensembleWeights, setEnsembleWeights] = useState(saved?.ensembleWeights ?? defaultEnsembleWeights());
  const [fusionMode, setFusionMode] = useState(saved?.fusionMode || "fixed");
  const [applyConstraints, setApplyConstraints] = useState(saved?.applyConstraints ?? false);
  const [autoStrategy, setAutoStrategy] = useState(saved?.autoStrategy ?? false);
  const [useCalibration, setUseCalibration] = useState(saved?.useCalibration ?? false);
  const [useFeedbackBoost, setUseFeedbackBoost] = useState(saved?.useFeedbackBoost ?? false);
  const [explainMode, setExplainMode] = useState(saved?.explainMode || "rules");
  const [useCrossEncoder, setUseCrossEncoder] = useState(saved?.useCrossEncoder ?? false);
  const [crossEncoderEnabled, setCrossEncoderEnabled] = useState(false);
  const [rerankPool, setRerankPool] = useState(saved?.rerankPool ?? 20);
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
    fetchSystemConfig().then((cfg) => {
      setCrossEncoderEnabled(Boolean(cfg.enable_cross_encoder_rerank));
      if (cfg.cross_encoder_rerank_pool) {
        setRerankPool(cfg.cross_encoder_rerank_pool);
      }
    });
  }, []);

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        mode,
        queryKey,
        strategy,
        metric,
        skillsMode,
        semanticWeight,
        topK,
        ensemble,
        ensembleChecks,
        ensembleWeights,
        fusionMode,
        applyConstraints,
        autoStrategy,
        useCalibration,
        useFeedbackBoost,
        explainMode,
        useCrossEncoder,
        rerankPool,
      })
    );
  }, [
    mode,
    queryKey,
    strategy,
    metric,
    skillsMode,
    semanticWeight,
    topK,
    ensemble,
    ensembleChecks,
    ensembleWeights,
    fusionMode,
    applyConstraints,
    autoStrategy,
    useCalibration,
    useFeedbackBoost,
    explainMode,
    useCrossEncoder,
    rerankPool,
  ]);

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
    searches: DEFAULT_ENSEMBLE.map((s, i) => ({ ...s, weight: ensembleWeights[i] ?? s.weight })).filter((_, i) => ensembleChecks[i]),
    fusionMode,
    applyConstraints,
    autoStrategy,
    useCalibration,
    useFeedbackBoost,
    explainMode,
    useCrossEncoder,
    rerankPool,
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
            <label key={i} className="checkbox-row ensemble-row">
              <input
                type="checkbox"
                checked={ensembleChecks[i]}
                onChange={(e) => {
                  const next = [...ensembleChecks];
                  next[i] = e.target.checked;
                  setEnsembleChecks(next);
                }}
              />
              <span>
                {s.strategy} / {s.metric}
                {s.skills_mode !== "jaccard" ? ` / ${s.skills_mode}` : ""}
              </span>
              <input
                type="number"
                min="0.1"
                max="5"
                step="0.1"
                className="ensemble-weight-input"
                value={ensembleWeights[i] ?? 1}
                disabled={!ensembleChecks[i]}
                onChange={(e) => {
                  const next = [...ensembleWeights];
                  next[i] = Number(e.target.value);
                  setEnsembleWeights(next);
                }}
                aria-label={`Weight for ${s.strategy} ${s.metric}`}
              />
            </label>
          ))}
        </div>
      )}

      {!ensemble && (
        <div className="control-section">
          <p className="control-section-title">Advanced ML</p>
          <div className="controls-grid">
            <div className="field">
              <label htmlFor="fusion">Fusion mode</label>
              <select id="fusion" value={fusionMode} onChange={(e) => setFusionMode(e.target.value)}>
                <option value="fixed">Fixed weights</option>
                <option value="learned">Learned LR fusion</option>
                <option value="hierarchical">Hierarchical skills</option>
              </select>
            </div>
            <div className="field">
              <label htmlFor="explain">Explain mode</label>
              <select id="explain" value={explainMode} onChange={(e) => setExplainMode(e.target.value)}>
                <option value="rules">Rule-based</option>
                <option value="llm">Grounded LLM</option>
              </select>
            </div>
          </div>
          <div className="ensemble-box" style={{ marginTop: 12 }}>
            <label className="checkbox-row">
              <input type="checkbox" checked={applyConstraints} onChange={(e) => setApplyConstraints(e.target.checked)} />
              Apply constraints (exp / remote / salary)
            </label>
            <label className="checkbox-row">
              <input type="checkbox" checked={autoStrategy} onChange={(e) => setAutoStrategy(e.target.checked)} />
              Auto strategy routing
            </label>
            <label className="checkbox-row">
              <input type="checkbox" checked={useCalibration} onChange={(e) => setUseCalibration(e.target.checked)} />
              Platt calibration
            </label>
            <label className="checkbox-row">
              <input type="checkbox" checked={useFeedbackBoost} onChange={(e) => setUseFeedbackBoost(e.target.checked)} />
              Feedback boost
            </label>
            {crossEncoderEnabled && mode === "candidate_to_jobs" && (
              <label className="checkbox-row">
                <input type="checkbox" checked={useCrossEncoder} onChange={(e) => setUseCrossEncoder(e.target.checked)} />
                Cross-encoder rerank (top {rerankPool} → top K)
              </label>
            )}
            {crossEncoderEnabled && mode === "job_to_candidates" && (
              <label className="checkbox-row">
                <input type="checkbox" checked={useCrossEncoder} onChange={(e) => setUseCrossEncoder(e.target.checked)} />
                Cross-encoder rerank candidates (top {rerankPool})
              </label>
            )}
          </div>
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
