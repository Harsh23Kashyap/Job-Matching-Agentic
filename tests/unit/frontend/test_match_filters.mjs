import assert from "node:assert/strict";
import test from "node:test";

import {
  collectSkillOptions,
  createMatchFilters,
  filterAndSortMatchRows,
  hasActiveMatchFilters,
} from "../../../frontend/src/utils/matchFilters.js";

const sampleRows = [
  {
    target_id: "job_a",
    target_label: "Backend Engineer",
    similarity: 0.82,
    matched_skills: ["Python", "Docker"],
    missing_skills: ["Kubernetes"],
    job_required_experience: 5,
    job_budget_min: 2_000_000,
    job_budget_max: 3_000_000,
    job_remote_policy: true,
    job_created_at: "2026-05-20T10:00:00Z",
    remote_score: 1,
  },
  {
    target_id: "job_b",
    target_label: "Frontend Developer",
    similarity: 0.61,
    matched_skills: ["React"],
    missing_skills: ["TypeScript"],
    job_required_experience: 2,
    job_budget_min: 1_200_000,
    job_budget_max: 1_800_000,
    job_remote_policy: false,
    job_created_at: "2026-05-25T10:00:00Z",
    remote_score: 0.4,
  },
];

test("collectSkillOptions returns sorted unique skills", () => {
  const options = collectSkillOptions(sampleRows);
  assert.ok(options.includes("Python"));
  assert.ok(options.includes("Kubernetes"));
});

test("filterAndSortMatchRows applies search, skills, remote, and score range", () => {
  const filters = createMatchFilters({
    search: "backend",
    skills: ["Python"],
    remoteOnly: true,
    minMatch: 70,
    maxMatch: 100,
  });
  const rows = filterAndSortMatchRows(sampleRows, filters, "candidate-jobs");
  assert.equal(rows.length, 1);
  assert.equal(rows[0].target_id, "job_a");
});

test("filterAndSortMatchRows filters experience and budget ranges", () => {
  const filters = createMatchFilters({
    expMin: "4",
    expMax: "6",
    salaryMin: "2500000",
    salaryMax: "3500000",
  });
  const rows = filterAndSortMatchRows(sampleRows, filters, "candidate-jobs");
  assert.equal(rows.length, 1);
  assert.equal(rows[0].target_id, "job_a");
});

test("filterAndSortMatchRows sorts by compensation and newest", () => {
  const byPay = filterAndSortMatchRows(
    sampleRows,
    createMatchFilters({ sort: "compensation" }),
    "candidate-jobs",
  );
  assert.equal(byPay[0].target_id, "job_a");

  const byNewest = filterAndSortMatchRows(
    sampleRows,
    createMatchFilters({ sort: "newest" }),
    "candidate-jobs",
  );
  assert.equal(byNewest[0].target_id, "job_b");
});

test("hasActiveMatchFilters detects non-default state", () => {
  assert.equal(hasActiveMatchFilters(createMatchFilters()), false);
  assert.equal(
    hasActiveMatchFilters(createMatchFilters({ search: "ml", minMatch: 60 })),
    true,
  );
});

test("employer candidate filters use candidate salary and experience", () => {
  const candidates = [
    {
      target_id: "cv_1",
      target_label: "Alex",
      similarity: 0.75,
      matched_skills: ["Python"],
      missing_skills: [],
      candidate_experience_years: 6,
      candidate_preferred_salary: 2_500_000,
      candidate_remote_preference: true,
      remote_score: 1,
    },
    {
      target_id: "cv_2",
      target_label: "Sam",
      similarity: 0.55,
      matched_skills: ["Java"],
      missing_skills: ["Python"],
      candidate_experience_years: 2,
      candidate_preferred_salary: 900_000,
      candidate_remote_preference: false,
      remote_score: 0.4,
    },
  ];

  const rows = filterAndSortMatchRows(
    candidates,
    createMatchFilters({ expMin: "5", salaryMin: "2000000" }),
    "employer-candidates",
  );
  assert.equal(rows.length, 1);
  assert.equal(rows[0].target_id, "cv_1");
});
