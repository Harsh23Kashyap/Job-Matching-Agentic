# Components

Reusable UI shared across portals.

## Match & results

| Component | Purpose |
|-----------|---------|
| `MatchDetailsDrawer.jsx` | Score bars, skill gaps, resume coach, similar recs |
| `CandidateJobResults.jsx` | Candidate match list + drawer trigger |
| `EmployerCandidateResults.jsx` | Employer match list + drawer trigger |
| `ResultsPanel.jsx` | Admin ranked results table |
| `SimilarRecommendations.jsx` | 3 similar job/candidate cards |
| `ResumeImprovementPanel.jsx` | Read-only resume coach UI |

## Forms & inputs

| Component | Purpose |
|-----------|---------|
| `ProfileForm.jsx` | Candidate profile fields |
| `JobPostingForm.jsx` | Employer job form |
| `FormSection.jsx`, `FormField.jsx` | Layout primitives |
| `SkillsChipsInput.jsx`, `SkillChip.jsx` | Skill tag entry |
| `CompensationInput.jsx` | Salary single + range |
| `ExperienceInput.jsx`, `LinksChipsInput.jsx` | Structured fields |

## Portal chrome

| Component | Purpose |
|-----------|---------|
| `PortalBackground.jsx`, `BackgroundOrnaments.jsx` | Subtle animated SVG backgrounds |
| `EmptyState.jsx`, `EmptyStatePanel.jsx` | Zero-state illustrations |
| `PageHeader.jsx`, `Stepper.jsx`, `Toast.jsx` | Common patterns |
| `AgentStatusPanel.jsx`, `AgentEventStrip.jsx` | Admin observability |
| `ProtectedRoute.jsx` | Role guard wrapper |

## Styling

Global tokens and portal styles: [../App.css](../App.css)
