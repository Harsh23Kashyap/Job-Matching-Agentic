import assert from "node:assert/strict";
import { describe, it } from "node:test";

import {
  COMPOSITE_WEIGHTS,
  describeMatchDrivers,
  resolveScoreComponents,
} from "../../frontend/src/utils/matchScoring.js";

describe("matchScoring", () => {
  it("weights sum to 1", () => {
    const total = Object.values(COMPOSITE_WEIGHTS).reduce((sum, value) => sum + value, 0);
    assert.ok(Math.abs(total - 1) < 1e-9);
  });

  it("builds fallback components from row fields", () => {
    const components = resolveScoreComponents({
      semantic_score: 0.8,
      skills_score: 0.7,
      title_score: 0.6,
      experience_score: 0.9,
      compensation_score: 1,
      remote_score: 0.4,
    });
    assert.equal(components.length, 6);
    assert.ok(components.every((item) => item.contribution === item.weight * item.score));
  });

  it("describes strongest and weakest drivers", () => {
    const line = describeMatchDrivers({
      score_components: [
        { key: "semantic", label: "Semantic fit", weight: 0.28, score: 0.82, contribution: 0.23 },
        { key: "remote", label: "Remote preference", weight: 0.1, score: 0.35, contribution: 0.035 },
      ],
    });
    assert.match(line, /semantic fit/i);
    assert.match(line, /remote preference/i);
  });
});
