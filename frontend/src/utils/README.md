# Utils

Pure helpers · no React, easy to unit test with Node `node --test`.

## Files

| File | Purpose |
|------|---------|
| `profileFields.js` | API ↔ form mapping; `profileToPayload`, `isCandidateProfileReady` |
| `jobFields.js` | Job form ↔ API mapping |
| `format.js` | Match %, score bands, humanized strategy labels |
| `feedbackState.js` | Merge server feedback with local UI state |
| `resumeClean.js` | Frontend mirror of backend CID cleanup |
| `skills.js` | Skill string ↔ array for payloads |
| `validation.js` | Form validation helpers |
| `profileEvents.js` | `PROFILE_UPDATED_EVENT` for cross-page refresh |
| `portalBackground.js` | `resolveBackgroundVariant()` for ornaments |

## Tests

```bash
node --test tests/unit/frontend/test_profile_fields.mjs
node --test tests/unit/frontend/test_match_format.mjs
node --test tests/unit/frontend/test_feedback_state.mjs
node --test tests/unit/frontend/test_*.mjs
```
