import test from "node:test";
import assert from "node:assert/strict";
import { buildFeedbackMaps } from "../../../frontend/src/utils/feedbackState.js";

test("buildFeedbackMaps tracks candidate actions", () => {
  const maps = buildFeedbackMaps([
    { target_id: "job_01", action: "save", context_id: null },
    { target_id: "job_02", action: "not_interested", context_id: null },
    { target_id: "job_03", action: "apply", context_id: null },
  ]);
  assert.equal(maps.saved.has("job_01"), true);
  assert.equal(maps.notInterested.has("job_02"), true);
  assert.equal(maps.applied.has("job_03"), true);
});

test("buildFeedbackMaps filters employer context", () => {
  const maps = buildFeedbackMaps(
    [
      { target_id: "cv_01", action: "save", context_id: "job_01" },
      { target_id: "cv_02", action: "reject", context_id: "job_02" },
    ],
    { contextId: "job_01" },
  );
  assert.equal(maps.saved.has("cv_01"), true);
  assert.equal(maps.rejected.has("cv_02"), false);
});

test("buildFeedbackMaps unsave clears saved state", () => {
  const maps = buildFeedbackMaps([
    { target_id: "job_01", action: "save", context_id: null },
    { target_id: "job_01", action: "unsave", context_id: null },
  ]);
  assert.equal(maps.saved.has("job_01"), false);
});
