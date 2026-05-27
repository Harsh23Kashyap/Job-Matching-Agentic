import assert from "node:assert/strict";
import test from "node:test";

import {
  commitSkillDraft,
  dedupeSkills,
  parseSkillsInput,
  skillsToPayload,
  splitSkillTokens,
} from "../../../frontend/src/utils/skills.js";

test("parseSkillsInput trims and splits comma-separated values", () => {
  assert.deepEqual(parseSkillsInput(" Python, FastAPI ,  "), ["FastAPI", "Python"]);
});

test("dedupeSkills is case-insensitive", () => {
  assert.deepEqual(dedupeSkills(["Python", "python", "PYTHON", "Java"]), ["Java", "Python"]);
});

test("preserves complex skill names", () => {
  const raw = "C/C++, REST APIs, CI/CD, TensorFlow/Keras";
  assert.deepEqual(parseSkillsInput(raw), ["C/C++", "CI/CD", "REST API", "TensorFlow/Keras"]);
});

test("splitSkillTokens handles paste separators", () => {
  assert.deepEqual(splitSkillTokens("Go; Rust\nJava|C++"), ["Go", "Rust", "Java", "C++"]);
});

test("commitSkillDraft merges without duplicates", () => {
  const next = commitSkillDraft(["Python"], "java, Python, C/C++");
  assert.deepEqual(next, ["C/C++", "Java", "Python"]);
});

test("dedupeSkills merges synonym variants", () => {
  assert.deepEqual(dedupeSkills(["React.js", "React", "reactjs", "Python"]), ["Python", "React"]);
});

test("skillsToPayload canonicalizes variants", () => {
  assert.deepEqual(skillsToPayload(" React.js, ML, AWS EC2, Python "), ["AWS", "Machine Learning", "Python", "React"]);
});
