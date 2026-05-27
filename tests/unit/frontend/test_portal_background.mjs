import assert from "node:assert/strict";
import test from "node:test";

import {
  BACKGROUND_VARIANTS,
  resolveBackgroundVariant,
} from "../../../frontend/src/utils/portalBackground.js";

test("resolveBackgroundVariant maps candidate and employer routes", () => {
  assert.equal(resolveBackgroundVariant("/candidate/onboarding"), "onboarding");
  assert.equal(resolveBackgroundVariant("/candidate/profile"), "profile");
  assert.equal(resolveBackgroundVariant("/candidate/matches"), "jobs");
  assert.equal(resolveBackgroundVariant("/candidate/saved"), "jobs");
  assert.equal(resolveBackgroundVariant("/employer/jobs"), "employer-jobs");
  assert.equal(resolveBackgroundVariant("/employer/matches"), "employer-candidates");
  assert.equal(resolveBackgroundVariant("/employer/applications"), "employer-candidates");
  assert.equal(resolveBackgroundVariant("/admin/console"), "admin");
  assert.equal(resolveBackgroundVariant("/login"), "base");
});

test("background variants include admin and jobs", () => {
  assert.ok(BACKGROUND_VARIANTS.includes("admin"));
  assert.ok(BACKGROUND_VARIANTS.includes("jobs"));
  assert.ok(BACKGROUND_VARIANTS.includes("employer-jobs"));
});
