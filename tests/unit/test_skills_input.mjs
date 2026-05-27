import assert from "node:assert/strict";
import test from "node:test";

import {
  commitSkillDraft,
  dedupeSkills,
  parseSkillsInput,
  skillsToPayload,
  splitSkillTokens,
} from "../../frontend/src/utils/skills.js";

test("parseSkillsInput trims and splits comma-separated values", () => {
  assert.deepEqual(parseSkillsInput(" Python, FastAPI ,  "), ["Python", "FastAPI"]);
});

test("dedupeSkills is case-insensitive", () => {
  assert.deepEqual(dedupeSkills(["Python", "python", "PYTHON", "Java"]), ["Python", "Java"]);
});

test("preserves complex skill names", () => {
  const raw = "C/C++, REST APIs, CI/CD, TensorFlow/Keras";
  assert.deepEqual(parseSkillsInput(raw), ["C/C++", "REST APIs", "CI/CD", "TensorFlow/Keras"]);
});

test("splitSkillTokens handles paste separators", () => {
  assert.deepEqual(splitSkillTokens("Go; Rust\nJava|C++"), ["Go", "Rust", "Java", "C++"]);
});

test("commitSkillDraft merges without duplicates", () => {
  const next = commitSkillDraft(["Python"], "java, Python, C/C++");
  assert.deepEqual(next, ["Python", "java", "C/C++"]);
});

test("skillsToPayload returns clean array", () => {
  assert.deepEqual(skillsToPayload(" Python, python, Go "), ["Python", "Go"]);
});
