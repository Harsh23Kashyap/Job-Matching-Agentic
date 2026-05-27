import Button from "./Button.jsx";
import {
  activeMatchFilterCount,
  hasActiveMatchFilters,
} from "../utils/matchFilters.js";

const MATCH_SCORE_OPTIONS = [
  { value: 0, label: "Any" },
  { value: 50, label: "50%+" },
  { value: 60, label: "60%+" },
  { value: 70, label: "70%+" },
  { value: 80, label: "80%+" },
  { value: 90, label: "90%+" },
  { value: 100, label: "100%" },
];

function RangeField({ label, minValue, maxValue, onMinChange, onMaxChange, minPlaceholder, maxPlaceholder }) {
  return (
    <div className="match-filter-range">
      <span className="match-filter-range__label">{label}</span>
      <div className="match-filter-range__inputs">
        <input
          type="number"
          className="filter-input"
          placeholder={minPlaceholder}
          aria-label={`${label} minimum`}
          value={minValue}
          min="0"
          onChange={(e) => onMinChange(e.target.value)}
        />
        <span className="match-filter-range__sep">to</span>
        <input
          type="number"
          className="filter-input"
          placeholder={maxPlaceholder}
          aria-label={`${label} maximum`}
          value={maxValue}
          min="0"
          onChange={(e) => onMaxChange(e.target.value)}
        />
      </div>
    </div>
  );
}

export default function MatchResultsFilters({
  variant = "candidate-jobs",
  filters,
  onChange,
  onClear,
  skillOptions = [],
  onRefresh,
  loading = false,
  refreshLabel = "Refresh",
}) {
  const isCandidateJobs = variant === "candidate-jobs";
  const activeCount = activeMatchFilterCount(filters);
  const showClear = hasActiveMatchFilters(filters);

  const patch = (partial) => onChange({ ...filters, ...partial });

  const toggleSkill = (skill) => {
    const selected = new Set(filters.skills || []);
    if (selected.has(skill)) selected.delete(skill);
    else selected.add(skill);
    patch({ skills: [...selected] });
  };

  return (
    <div className="match-filters">
      <div className="match-filters__primary results-filters">
        <input
          type="search"
          className="filter-search"
          placeholder={isCandidateJobs ? "Search roles…" : "Search candidates…"}
          aria-label={isCandidateJobs ? "Search roles" : "Search candidates"}
          value={filters.search}
          onChange={(e) => patch({ search: e.target.value })}
        />

        <label className={`filter-pill${filters.remoteOnly ? " filter-pill--active" : ""}`}>
          <input
            type="checkbox"
            className="visually-hidden"
            checked={filters.remoteOnly}
            onChange={(e) => patch({ remoteOnly: e.target.checked })}
          />
          Remote only
        </label>

        <select
          className="filter-select"
          value={filters.sort}
          onChange={(e) => patch({ sort: e.target.value })}
          aria-label="Sort results"
        >
          <option value="best">Best match</option>
          <option value="newest">Newest</option>
          <option value="compensation">
            {isCandidateJobs ? "Highest budget" : "Highest expected pay"}
          </option>
          <option value="title">{isCandidateJobs ? "Role title A–Z" : "Name A–Z"}</option>
        </select>

        {showClear && (
          <button type="button" className="btn-ghost btn-ghost--sm match-filters__clear" onClick={onClear}>
            Clear all{activeCount > 0 ? ` (${activeCount})` : ""}
          </button>
        )}

        {onRefresh && (
          <Button className="btn-secondary filter-refresh" loading={loading} loadingLabel="Refreshing…" onClick={onRefresh}>
            {refreshLabel}
          </Button>
        )}
      </div>

      <details className="match-filters__advanced">
        <summary>
          More filters{activeCount > 0 ? ` · ${activeCount} active` : ""}
        </summary>
        <div className="match-filters__advanced-body">
          {skillOptions.length > 0 && (
            <div className="match-filter-skills">
              <span className="match-filter-skills__label">Skills</span>
              <div className="match-filter-skills__chips" role="group" aria-label="Filter by skill">
                {skillOptions.map((skill) => {
                  const active = (filters.skills || []).includes(skill);
                  return (
                    <button
                      key={skill}
                      type="button"
                      className={`filter-pill filter-pill--btn${active ? " filter-pill--active" : ""}`}
                      onClick={() => toggleSkill(skill)}
                      aria-pressed={active}
                    >
                      {skill}
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          <div className="match-filters__ranges">
            <div className="match-filter-score-range">
              <span className="match-filter-range__label">Match score</span>
              <div className="match-filter-score-range__inputs">
                <select
                  className="filter-select"
                  value={String(filters.minMatch)}
                  onChange={(e) => patch({ minMatch: Number(e.target.value) })}
                  aria-label="Minimum match score"
                >
                  {MATCH_SCORE_OPTIONS.filter((opt) => opt.value < 100).map((opt) => (
                    <option key={`min-${opt.value}`} value={opt.value}>
                      Min {opt.label}
                    </option>
                  ))}
                </select>
                <select
                  className="filter-select"
                  value={String(filters.maxMatch)}
                  onChange={(e) => patch({ maxMatch: Number(e.target.value) })}
                  aria-label="Maximum match score"
                >
                  {MATCH_SCORE_OPTIONS.filter((opt) => opt.value > 0).map((opt) => (
                    <option key={`max-${opt.value}`} value={opt.value}>
                      Max {opt.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <RangeField
              label={isCandidateJobs ? "Required experience (years)" : "Candidate experience (years)"}
              minValue={filters.expMin}
              maxValue={filters.expMax}
              minPlaceholder="Min yrs"
              maxPlaceholder="Max yrs"
              onMinChange={(value) => patch({ expMin: value })}
              onMaxChange={(value) => patch({ expMax: value })}
            />

            <RangeField
              label={isCandidateJobs ? "Budget (INR/year)" : "Expected pay (INR/year)"}
              minValue={filters.salaryMin}
              maxValue={filters.salaryMax}
              minPlaceholder="Min"
              maxPlaceholder="Max"
              onMinChange={(value) => patch({ salaryMin: value })}
              onMaxChange={(value) => patch({ salaryMax: value })}
            />
          </div>
        </div>
      </details>
    </div>
  );
}
