import assert from "node:assert/strict";
import test from "node:test";

import { cleanFieldText } from "../../../frontend/src/utils/resumeClean.js";
import {
  mergeExtractedIntoFields,
  normalizeProfileFields,
  normalizeUrl,
} from "../../../frontend/src/utils/profileNormalize.js";
import { EMPTY_PROFILE_FIELDS } from "../../../frontend/src/utils/profileFields.js";

test("cleanFieldText removes CID artifacts from names", () => {
  assert.equal(cleanFieldText("Harsh Kashyap (cid:131), (cid:239)"), "Harsh Kashyap");
});

test("normalizeProfileFields cleans contact fields", () => {
  const normalized = normalizeProfileFields({
    ...EMPTY_PROFILE_FIELDS,
    name: "Jane Doe (cid:12)",
    email: " Jane@Example.COM ",
    phone: "+91 98765 43210",
    linkedin: "linkedin.com/in/jane-doe",
    skills: "Python, python, Go",
  });
  assert.equal(normalized.name, "Jane Doe");
  assert.equal(normalized.email, "jane@example.com");
  assert.equal(normalized.linkedin, "https://linkedin.com/in/jane-doe");
  assert.deepEqual(normalized.skills.split(", "), ["Go", "Python"]);
});

test("normalizeUrl adds https scheme", () => {
  assert.equal(normalizeUrl("github.com/jane"), "https://github.com/jane");
});

test("mergeExtractedIntoFields preserves existing id and merges skills", () => {
  const existing = {
    ...EMPTY_PROFILE_FIELDS,
    id: "candidate-abc",
    name: "Existing Name",
    skills: "Python",
    email: "keep@example.com",
  };
  const merged = mergeExtractedIntoFields(existing, {
    name: "Parsed Name",
    skills: ["Go", "Python"],
    email: "",
    phone: "+91 99999 88888",
  });
  assert.equal(merged.id, "candidate-abc");
  assert.equal(merged.name, "Parsed Name");
  assert.equal(merged.email, "keep@example.com");
  assert.equal(merged.phone, "+91 99999 88888");
  assert.deepEqual(merged.skills.split(", "), ["Go", "Python"]);
});

test("mergeExtractedIntoFields does not wipe salary when extraction empty", () => {
  const existing = {
    ...EMPTY_PROFILE_FIELDS,
    preferred_salary: 1200000,
    preferred_currency: "INR",
  };
  const merged = mergeExtractedIntoFields(existing, {
    name: "Alex",
    skills: ["Rust"],
    preferred_salary: null,
  });
  assert.equal(merged.preferred_salary, 1200000);
  assert.equal(merged.preferred_currency, "INR");
});
