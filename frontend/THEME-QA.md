# Theme visual QA checklist

Run after any theme or CSS token change. Toggle theme with the moon/sun control in the top nav.

## Setup

1. Start the app: `cd frontend && npm run dev`
2. Log in as candidate and employer demo accounts (or register fresh users).
3. Toggle **light** and **dark** mode on each portal.

## Global checks (both themes)

- [ ] Body background uses `--background`; no stray cream/white page backgrounds in dark mode
- [ ] Primary text uses `--foreground`; helper/secondary text uses `--muted-foreground` (readable, not washed out)
- [ ] Cards/panels use `--card` + `--card-foreground` + `--border`
- [ ] Inputs/textareas use `--input` background and `--foreground` text
- [ ] Placeholders visible but muted (not invisible, not same as body text)
- [ ] Primary buttons: `--primary` bg, `--primary-foreground` text; readable when disabled
- [ ] Secondary/outline buttons: visible border and label in dark mode
- [ ] No helper text relying on `opacity` alone for contrast
- [ ] Match tier pills/badges readable in both modes

## Employer portal

| Route | What to verify |
|-------|----------------|
| `/employer/jobs` | Page subtitle, stat cards (Open roles, Remote-friendly), numbers |
| `/employer/jobs` | JD import panel: dashed border, helper text, paste hint, textarea placeholder |
| `/employer/jobs` | Post role form labels, compensation fields, sticky footer buttons |
| `/employer/jobs` | Empty job list state (if no roles) |
| `/employer/matches` | Toolbar select, candidate cards, filters, empty state |
| `/employer/applications` | Section headers, activity rows |

## Candidate portal

| Route | What to verify |
|-------|----------------|
| `/candidate/onboarding` | Stepper, dropzone upload, helper copy |
| `/candidate/profile` | Form sections, skills input placeholder, profile strength |
| `/candidate/matches` | Match cards, tier pills, filters, drawer |
| `/candidate/saved` | Saved list, empty state |

## Auth (no portal accent)

| Route | What to verify |
|-------|----------------|
| `/login`, `/register` | Labels, placeholders, role picker cards, primary CTA |

## Admin

| Route | What to verify |
|-------|----------------|
| `/admin` | KPI cards, config panel, results table row hover |

## Pass criteria

- WCAG-ish: no text below ~4.5:1 on its immediate background for body/helper copy
- No white/cream cards in dark mode unless intentionally highlighted
- Stat numbers and labels clearly visible
- Upload/JD dashed borders visible in dark mode
- Disabled controls legible (muted, not invisible)

## Token reference

Semantic tokens live in `frontend/src/theme/tokens.css`; dark component overrides in `frontend/src/theme/dark-mode.css`.

Core: `--background`, `--foreground`, `--muted`, `--muted-foreground`, `--card`, `--card-foreground`, `--border`, `--input`, `--primary`, `--primary-foreground`

Surfaces: `--bg-elevated`, `--upload-bg`, `--upload-border`, `--skeleton-base`, `--skeleton-shine`, `--nav-backdrop`, `--sticky-footer-bg`

Focus: `--focus-ring`, `--focus-ring-error`

Illustrations: `--illustration-stroke`, `--illustration-accent`, `--illustration-sand`

Utility classes: `.text-foreground`, `.text-muted-foreground`, `.text-card-foreground`, `.bg-card`, `.bg-input`, `.border-border`
