import assert from "node:assert/strict";
import test from "node:test";

import {
  EMPTY_PROFILE_FIELDS,
  hasCandidateProfile,
  isCandidateProfileReady,
  isProfileStale,
  profileFromApi,
  profileToPayload,
} from "../../../frontend/src/utils/profileFields.js";
const PROFILE_STALE_MARKER = { __profileStale: true };

test("profileToPayload omits empty id on first save", () => {
  const payload = profileToPayload({ ...EMPTY_PROFILE_FIELDS, name: "Jordan Rivera", skills: "Python" });
  assert.equal("id" in payload, false);
  assert.equal(payload.name, "Jordan Rivera");
  assert.deepEqual(payload.skills, ["Python"]);
});

test("profileToPayload keeps id when updating", () => {
  const payload = profileToPayload({
    ...EMPTY_PROFILE_FIELDS,
    id: "candidate-abc123",
    name: "Jordan Rivera",
    skills: "Python",
  });
  assert.equal(payload.id, "candidate-abc123");
});

test("isCandidateProfileReady requires id and name", () => {
  assert.equal(isCandidateProfileReady(null), false);
  assert.equal(isCandidateProfileReady({}), false);
  assert.equal(isCandidateProfileReady({ id: "x", name: "" }), false);
  assert.equal(isCandidateProfileReady({ id: "", name: "Jordan Rivera" }), false);
  assert.equal(isCandidateProfileReady({ id: "cv_01", name: "Jordan Rivera" }), true);
});

test("hasCandidateProfile is true when id or name is set", () => {
  assert.equal(hasCandidateProfile(null), false);
  assert.equal(hasCandidateProfile({}), false);
  assert.equal(hasCandidateProfile({ id: "cv_01" }), true);
  assert.equal(hasCandidateProfile({ name: "Jordan Rivera" }), true);
  assert.equal(hasCandidateProfile({ id: "cv_01", name: "Jordan Rivera" }), true);
});

test("stale profile marker is detected and maps to empty form fields", () => {
  assert.equal(isProfileStale(PROFILE_STALE_MARKER), true);
  assert.equal(hasCandidateProfile(PROFILE_STALE_MARKER), true);
  assert.equal(isCandidateProfileReady(PROFILE_STALE_MARKER), false);
  const fields = profileFromApi(PROFILE_STALE_MARKER);
  assert.equal(fields.name, "");
  assert.equal(fields.id, "");
});
