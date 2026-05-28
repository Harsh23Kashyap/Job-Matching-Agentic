# Admin portal

Research and benchmarking console · not shown to product users.

## Pages

| File | Route | Purpose |
|------|-------|---------|
| `AdminConsole.jsx` | `/admin/console` | Agent status, manual match controls, system config |

## Features

- Three agent health cards (`AgentStatusPanel`)
- Manual match: pick entity, strategy, metric, skills mode, top-K (`MatchControls` + `ResultsPanel`)
- Agent event strip (`AgentEventStrip`) · last 50 bus events
- Vector store switch, ML toggles (`SystemConfigPanel`)

Demo: `demo.admin@test.com` / `demo1234`

For thesis narrative see [../../../docs/demo/DEMO-SCRIPT.md](../../../docs/demo/DEMO-SCRIPT.md) Part 1.

**Paper (Figure 10):** Admin console and manual match run in `ui-admin-console.png`, `ui-admin-match-run.png`.
