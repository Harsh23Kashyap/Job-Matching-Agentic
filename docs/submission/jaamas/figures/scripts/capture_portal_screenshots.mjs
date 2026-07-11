#!/usr/bin/env node
/**
 * Capture Section 4 portal screenshots (Figure 10) from the running dev stack.
 * Prereqs: backend :8001, frontend :5173, demo accounts seeded.
 */
import { chromium } from "playwright";
import { existsSync } from "node:fs";
import { mkdir } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(__dirname, "../screenshots");
const BASE = "http://localhost:5173";
const API = BASE;

async function apiLogin(context, email, password) {
  const res = await context.request.post(`${API}/auth/login`, {
    data: { email, password },
  });
  if (!res.ok()) {
    throw new Error(`Login failed for ${email}: ${res.status()} ${await res.text()}`);
  }
}

async function captureCandidate(page) {
  await page.goto(`${BASE}/candidate/onboarding`, { waitUntil: "networkidle" });
  await page.getByRole("heading", { name: /^Upload resume$/i }).waitFor({ timeout: 15000 });
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(OUT, "ui-candidate-onboarding.png") });

  await page.goto(`${BASE}/candidate/profile`, { waitUntil: "networkidle" });
  await page.getByRole("heading", { name: /Edit profile|Your profile|Finish your profile/i }).first().waitFor({
    timeout: 15000,
  });
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(OUT, "ui-candidate-profile.png") });

  await page.goto(`${BASE}/candidate/matches`, { waitUntil: "networkidle" });
  const findBtn = page.getByRole("button", { name: /^Find matching jobs$/i });
  if (await findBtn.isVisible({ timeout: 3000 }).catch(() => false)) {
    await findBtn.click();
  }
  await page.getByRole("heading", { name: /Machine Learning Engineer/i }).waitFor({
    timeout: 45000,
  });
  await page.getByRole("button", { name: /^View details$/i }).first().click();
  await page.waitForSelector(".match-drawer", { timeout: 15000 });
  await page.waitForTimeout(500);
  await page.screenshot({
    path: path.join(OUT, "ui-candidate-matches.png"),
  });
  await page.locator(".match-drawer").screenshot({
    path: path.join(OUT, "ui-score-breakdown.png"),
  });
}

async function captureEmployer(page) {
  await page.goto(`${BASE}/employer/jobs`, { waitUntil: "networkidle" });
  await page.getByRole("heading", { name: /My jobs/i }).first().waitFor({
    timeout: 15000,
  });
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(OUT, "ui-employer-jobs.png") });

  await page.goto(`${BASE}/employer/matches`, { waitUntil: "networkidle" });
  const refreshBtn = page.getByRole("button", { name: /^Refresh matches$|^Find candidates$/i });
  if (await refreshBtn.first().isVisible({ timeout: 3000 }).catch(() => false)) {
    await refreshBtn.first().click();
  }
  await page.getByRole("button", { name: /^View profile$/i }).first().waitFor({
    timeout: 45000,
  });
  await page.getByRole("button", { name: /^View profile$/i }).first().click();
  await page.waitForSelector(".match-drawer", { timeout: 15000 });
  await page.waitForTimeout(500);
  await page.screenshot({
    path: path.join(OUT, "ui-employer-matches.png"),
  });
}

async function captureAdmin(page) {
  await page.goto(`${BASE}/admin/console`, { waitUntil: "networkidle" });
  await page.getByRole("heading", { name: /Operations console/i }).waitFor({ timeout: 15000 });
  await page.waitForSelector(".agent-status-panel, .admin-summary-row", { timeout: 15000 });
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT, "ui-admin-console.png") });

  const querySelect = page.locator("#query-select");
  if (await querySelect.isVisible({ timeout: 5000 }).catch(() => false)) {
    await querySelect.selectOption({ label: /Rahul Sharma/i }).catch(async () => {
      const options = await querySelect.locator("option").allTextContents();
      const match = options.find((o) => /Rahul/i.test(o));
      if (match) await querySelect.selectOption({ label: match });
    });
  }

  const runBtn = page.getByRole("button", { name: /^Run match$/i });
  if (await runBtn.isVisible({ timeout: 5000 }).catch(() => false)) {
    await runBtn.click();
    await page.getByText(/Machine Learning Engineer|Results|Rank/i).first().waitFor({ timeout: 45000 });
    await page.waitForTimeout(500);
  }

  const matchSection = page.locator("#admin-section-matching");
  if (await matchSection.isVisible({ timeout: 3000 }).catch(() => false)) {
    await matchSection.scrollIntoViewIfNeeded();
    await page.waitForTimeout(400);
    await matchSection.screenshot({ path: path.join(OUT, "ui-admin-match-run.png") });
  } else {
    await page.screenshot({ path: path.join(OUT, "ui-admin-match-run.png") });
  }
}

async function main() {
  await mkdir(OUT, { recursive: true });
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,
  });

  try {
    await apiLogin(context, "demo.candidate@test.com", "demo1234");
    const candPage = await context.newPage();
    await captureCandidate(candPage);
    await candPage.close();

    await context.clearCookies();
    await apiLogin(context, "demo.employer@test.com", "demo1234");
    const empPage = await context.newPage();
    await captureEmployer(empPage);
    await empPage.close();

    await context.clearCookies();
    await apiLogin(context, "demo.admin@test.com", "demo1234");
    const adminPage = await context.newPage();
    await captureAdmin(adminPage);
    await adminPage.close();

    console.log("Saved screenshots to", OUT);

    const figuresDir = path.resolve(__dirname, "..");
    const venvPy = path.resolve(figuresDir, "../../../../backend/.venv/bin/python");
    const py = process.env.PYTHON ?? (existsSync(venvPy) ? venvPy : "python3");
    const border = spawnSync(
      py,
      [
        path.join(figuresDir, "crop_figures.py"),
        figuresDir,
        "--borders-only",
        "--border-screenshots-only",
        "--border-px",
        "3",
      ],
      { stdio: "inherit" },
    );
    if (border.status !== 0) {
      throw new Error("Screenshot border pass failed");
    }
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
