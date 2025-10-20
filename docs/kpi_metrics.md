# AI-linked KM KPIs

- Ticket deflection % = (self-service solves + bot solves) / total intents
- AI agent resolution % = autonomous resolutions / AI-handled interactions
- Search success rate = successful queries / total queries
- Onboarding time-to-value = days from start to first successful task
- Article freshness = % articles updated within SLA (e.g., 90 days)

## Measurement approach
- Instrument bot and search events; export daily aggregates.
- Tie deflection to page_view -> case_open conversion.
- Track last_updated vs SLA; flag stale assets.
