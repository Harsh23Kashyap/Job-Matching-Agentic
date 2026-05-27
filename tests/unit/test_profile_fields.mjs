import assert from "node:assert/strict";
import test from "node:test";

import {
  EMPTY_PROFILE_FIELDS,
  isCandidateProfileReady,
  profileToPayload,
} from "../../frontend/src/utils/profileFields.js";

test("profileToPayload omits empty id on first save", () => {
  const payload = profileToPayload({ ...EMPTY_PROFILE_FIELDS, name: "Harsh Kashyap", skills: "Python" });
  assert.equal("id" in payload, false);
  assert.equal(payload.name, "Harsh Kashyap");
  assert.deepEqual(payload.skills, ["Python"]);
});

test("profileToPayload keeps id when updating", () => {
  const payload = profileToPayload({
    ...EMPTY_PROFILE_FIELDS,
    id: "candidate-abc123",
    name: "Harsh Kashyap",
    skills: "Python",
  });
  assert.equal(payload.id, "candidate-abc123");
});

test("isCandidateProfileReady requires id and name", () => {
  assert.equal(isCandidateProfileReady(null), false);
  assert.equal(isCandidateProfileReady({}), false);
  assert.equal(isCandidateProfileReady({ id: "x", name: "" }), false);
  assert.equal(isCandidateProfileReady({ id: "", name: "Harsh Kashyap" }), false);
  assert.equal(isCandidateProfileReady({ id: "cv_01", name: "Harsh Kashyap" }), true);
});
