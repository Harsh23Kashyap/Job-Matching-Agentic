import { useEffect, useState } from "react";
import { fetchCandidates, fetchJobs, fetchSystemConfig } from "../api/client.js";
import { IconMatch } from "./icons.jsx";

const DEFAULT_ENSEMBLE = [
  { strategy: "semantic", metric: "cosine", weight: 1.0, skills_mode: "jaccard", semantic_weight: 0.7 },
  { strategy: "multimodal", metric: "cosine", weight: 1.0, skills_mode: "jaccard", semantic_weight: 0.7 },
  { strategy: "semantic", metric: "euclidean", weight: 1.0, skills_mode: "jaccard", semantic_weight: 0.7 },
  { strategy: "multimodal", metric: "cosine", weight: 1.0, skills_mode: "embedding", semantic_weight: 0.7 },
];

const DEFAULTS = {
  mode: "candidate_to_jobs",
  queryKey: "",
  strategy: "semantic",
  metric: "cosine",
  skillsMode: "jaccard",
  semanticWeight: 0.7,
  topK: 5,
  ensemble: false,
  ensembleChecks: [true, true, true, true],
  ensembleWeights: [1, 1, 1, 1],
  fusionMode: "fixed",
  applyConstraints: false,
  autoStrategy: false,
  useCalibration: false,
  useFeedbackBoost: false,
  explainMode: "rules",
  useCrossEncoder: false,
  rerankPool: 20,
};

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

export default function MatchControls({ onRun, onDailyBatch, loading, lastRun }) {
  const saved = loadSavedConfig();
  const [mode, setMode] = useState(saved?.mode || DEFAULTS.mode);
  const [queryKey, setQueryKey] = useState(saved?.queryKey || DEFAULTS.queryKey);
  const [strategy, setStrategy] = useState(saved?.strategy || DEFAULTS.strategy);
  const [metric, setMetric] = useState(saved?.metric || DEFAULTS.metric);
  const [skillsMode, setSkillsMode] = useState(saved?.skillsMode || DEFAULTS.skillsMode);
  const [semanticWeight, setSemanticWeight] = useState(saved?.semanticWeight ?? DEFAULTS.semanticWeight);
  const [topK, setTopK] = useState(saved?.topK ?? DEFAULTS.topK);
  const [ensemble, setEnsemble] = useState(saved?.ensemble ?? DEFAULTS.ensemble);
  const [ensembleChecks, setEnsembleChecks] = useState(saved?.ensembleChecks ?? DEFAULTS.ensembleChecks);
  const [ensembleWeights, setEnsembleWeights] = useState(saved?.ensembleWeights ?? defaultEnsembleWeights());
  const [fusionMode, setFusionMode] = useState(saved?.fusionMode || DEFAULTS.fusionMode);
  const [applyConstraints, setApplyConstraints] = useState(saved?.applyConstraints ?? DEFAULTS.applyConstraints);
  const [autoStrategy, setAutoStrategy] = useState(saved?.autoStrategy ?? DEFAULTS.autoStrategy);
  const [useCalibration, setUseCalibration] = useState(saved?.useCalibration ?? DEFAULTS.useCalibration);
  const [useFeedbackBoost, setUseFeedbackBoost] = useState(saved?.useFeedbackBoost ?? DEFAULTS.useFeedbackBoost);
  const [explainMode, setExplainMode] = useState(saved?.explainMode || DEFAULTS.explainMode);
  const [useCrossEncoder, setUseCrossEncoder] = useState(saved?.useCrossEncoder ?? DEFAULTS.useCrossEncoder);
  const [crossEncoderEnabled, setCrossEncoderEnabled] = useState(false);
  const [rerankPool, setRerankPool] = useState(saved?.rerankPool ?? DEFAULTS.rerankPool);
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
      }),
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

  const resetDefaults = () => {
    localStorage.removeItem(STORAGE_KEY);
    setMode(DEFAULTS.mode);
    setQueryKey(names[0] || "");
    setStrategy(DEFAULTS.strategy);
    setMetric(DEFAULTS.metric);
    setSkillsMode(DEFAULTS.skillsMode);
    setSemanticWeight(DEFAULTS.semanticWeight);
    setTopK(DEFAULTS.topK);
    setEnsemble(DEFAULTS.ensemble);
    setEnsembleChecks([...DEFAULTS.ensembleChecks]);
    setEnsembleWeights(defaultEnsembleWeights());
    setFusionMode(DEFAULTS.fusionMode);
    setApplyConstraints(DEFAULTS.applyConstraints);
    setAutoStrategy(DEFAULTS.autoStrategy);
    setUseCalibration(DEFAULTS.useCalibration);
    setUseFeedbackBoost(DEFAULTS.useFeedbackBoost);
    setExplainMode(DEFAULTS.explainMode);
    setUseCrossEncoder(DEFAULTS.useCrossEncoder);
    setRerankPool(DEFAULTS.rerankPool);
  };

  const semanticDisabled = ensemble || strategy === "semantic";
  const semanticPct = Math.round(semanticWeight * 100);

  return (
    <section className="panel admin-match-controls">
      <div className="panel-header">
        <IconMatch size={18} />
        <h2>Match controls</h2>
      </div>

      <div className="control-section">
        <p className="control-section-title">Direction</p>
        <p className="control-section-help">Choose whether to rank jobs for a candidate or candidates for a job.</p>
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
          <div className="field field--full">
            <label htmlFor="weight">Semantic weight · {semanticPct}%</label>
            <input
              id="weight"
              type="range"
              min="0"
              max="100"
              step="5"
              value={semanticPct}
              onChange={(e) => setSemanticWeight(Number(e.target.value) / 100)}
              disabled={semanticDisabled}
              className="admin-range"
            />
            <p className="control-section-help">Higher values prioritize resume meaning over skill overlap.</p>
          </div>
          <div className="field">
            <label htmlFor="topk">Top K</label>
            <input id="topk" type="number" min="1" max="15" value={topK} onChange={(e) => setTopK(Number(e.target.value))} />
            <p className="control-section-help">Number of results to return.</p>
          </div>
          {mode === "candidate_to_jobs" && (
            <label className="admin-toggle-row">
              <input type="checkbox" className="admin-toggle" checked={ensemble} onChange={(e) => setEnsemble(e.target.checked)} />
              <span>Ensemble (RRF)</span>
            </label>
          )}
        </div>
      </div>

      {ensemble && mode === "candidate_to_jobs" && (
        <div className="ensemble-box control-section">
          <p className="control-section-title">Ensemble searches</p>
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
          <p className="control-section-title">Advanced settings</p>
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
        </div>
      )}

      {!ensemble && (
        <div className="control-section">
          <p className="control-section-title">Constraints</p>
          <label className="admin-toggle-row admin-toggle-row--block">
            <input
              type="checkbox"
              className="admin-toggle"
              checked={applyConstraints}
              onChange={(e) => setApplyConstraints(e.target.checked)}
            />
            <span>Apply experience, remote, and salary constraints</span>
          </label>
          <div className="admin-constraint-chips">
            <span className={`admin-constraint-chip${applyConstraints ? " admin-constraint-chip--on" : ""}`}>Experience</span>
            <span className={`admin-constraint-chip${applyConstraints ? " admin-constraint-chip--on" : ""}`}>Remote</span>
            <span className={`admin-constraint-chip${applyConstraints ? " admin-constraint-chip--on" : ""}`}>Salary</span>
          </div>
          <div className="admin-advanced-toggles">
            <label className="admin-toggle-row">
              <input type="checkbox" className="admin-toggle" checked={autoStrategy} onChange={(e) => setAutoStrategy(e.target.checked)} />
              <span>Auto strategy routing</span>
            </label>
            <label className="admin-toggle-row">
              <input type="checkbox" className="admin-toggle" checked={useCalibration} onChange={(e) => setUseCalibration(e.target.checked)} />
              <span>Platt calibration</span>
            </label>
            <label className="admin-toggle-row">
              <input type="checkbox" className="admin-toggle" checked={useFeedbackBoost} onChange={(e) => setUseFeedbackBoost(e.target.checked)} />
              <span>Feedback boost</span>
            </label>
            {crossEncoderEnabled && (
              <label className="admin-toggle-row">
                <input type="checkbox" className="admin-toggle" checked={useCrossEncoder} onChange={(e) => setUseCrossEncoder(e.target.checked)} />
                <span>Cross-encoder rerank (top {rerankPool})</span>
              </label>
            )}
          </div>
        </div>
      )}

      {lastRun && (
        <p className="admin-last-run admin-last-run--inline">
          Last run: {lastRun.resultCount} results · {lastRun.ms}ms · {lastRun.label}
        </p>
      )}

      <div className="actions admin-match-actions">
        <button type="button" className="btn-primary" disabled={loading || !queryKey} onClick={() => onRun(buildConfig())}>
          {loading ? "Running…" : "Run match"}
        </button>
        <button type="button" className="btn-secondary" disabled={loading} onClick={resetDefaults}>
          Reset
        </button>
        <button type="button" className="btn-secondary btn-ghost" disabled={loading} onClick={() => onDailyBatch(buildConfig())}>
          Daily batch
        </button>
      </div>
    </section>
  );
}
