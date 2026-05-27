import assert from "node:assert/strict";
import test from "node:test";

import {
  deriveWhyMatch,
  formatCandidateMatchScore,
  formatSkillExperienceLine,
  isApplyAvailable,
  matchPercent,
  matchTier,
} from "../../frontend/src/utils/format.js";

test("matchPercent rounds to whole percent", () => {
  assert.equal(matchPercent(0.5898), "59%");
  assert.equal(formatCandidateMatchScore(0.5898), "59%");
});

test("matchTier labels are candidate friendly", () => {
  assert.equal(matchTier(0.62).label, "Good fit");
  assert.equal(matchTier(0.45).label, "Moderate fit");
  assert.equal(matchTier(0.2).label, "Low fit");
});

test("formatSkillExperienceLine", () => {
  assert.equal(formatSkillExperienceLine(["Python"]), "Matches your Python experience.");
  assert.equal(
    formatSkillExperienceLine(["Java", "Spring Boot"]),
    "Matches your Java and Spring Boot experience.",
  );
});

test("deriveWhyMatch uses skill-based copy", () => {
  const row = {
    similarity: 0.58,
    matched_skills: ["Docker"],
    missing_skills: [],
    why_ranked: [],
  };
  assert.equal(deriveWhyMatch(row), "Matches your Docker experience.");
});

test("deriveWhyMatch fallback when no overlap", () => {
  const row = {
    similarity: 0.5,
    matched_skills: [],
    missing_skills: ["Go"],
    why_ranked: [],
  };
  assert.equal(deriveWhyMatch(row), "Limited direct skill overlap, but role context is close.");
});

test("isApplyAvailable defaults to true", () => {
  assert.equal(isApplyAvailable({}), true);
  assert.equal(isApplyAvailable({ apply_available: false }), false);
});
