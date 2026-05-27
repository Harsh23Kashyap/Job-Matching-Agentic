import assert from "node:assert/strict";
import test from "node:test";

import { resolveMatchExplanation } from "../../../frontend/src/utils/matchExplainability.js";

test("resolveMatchExplanation uses API explanation when present", () => {
  const row = {
    similarity: 0.8,
    explanation: {
      matched_skills: ["Python"],
      missing_skills: ["Go"],
      semantic: { score: 0.8, label: "Good fit", reason: "Strong alignment" },
      experience: { score: 1, label: "Strong fit", reason: "Meets requirement" },
      compensation: { score: 0.9, label: "Strong fit", reason: "Within budget" },
      remote: { score: 1, label: "Strong fit", reason: "Remote match" },
      score_breakdown: [
        { key: "semantic", label: "Semantic fit", weight: 0.28, score: 0.8, contribution: 0.224 },
      ],
      final_score: 0.8,
    },
  };

  const explanation = resolveMatchExplanation(row);
  assert.deepEqual(explanation.matched_skills, ["Python"]);
  assert.equal(explanation.semantic.reason, "Strong alignment");
  assert.equal(explanation.score_breakdown.length, 1);
});

test("resolveMatchExplanation falls back to legacy score fields", () => {
  const row = {
    similarity: 0.72,
    semantic_score: 0.75,
    skills_score: 0.6,
    title_score: 0.5,
    experience_score: 0.9,
    compensation_score: 0.85,
    remote_score: 1,
    matched_skills: ["React"],
    missing_skills: ["GraphQL"],
  };

  const explanation = resolveMatchExplanation(row);
  assert.deepEqual(explanation.matched_skills, ["React"]);
  assert.deepEqual(explanation.missing_skills, ["GraphQL"]);
  assert.equal(explanation.semantic.label, "Good");
  assert.equal(explanation.experience.label, "Strong");
  assert.ok(explanation.score_breakdown.length >= 5);
});
