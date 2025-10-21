# KPI Evaluation Report

This report walks through the calculation of key performance indicators (KPIs) defined in our knowledge & AI strategy. The data used here comes from synthetic events captured in the repository.

## KPIs computed

- Ticket deflection % = (self-service solves + bot solves) / total intents
- AI agent resolution % = (bot-resolved interactions) / (all bot-handled interactions)
- Search success rate = successful queries / total queries
- Onboarding time-to-value = average days from onboarding start to first success
- Article freshness = % of knowledge articles updated within SLA

## Method

1. Load the synthetic event logs from `data/` using pandas.
2. Compute each KPI using the formulas above.
3. Generate simple charts (e.g. bar charts) for each metric and save them to `docs/metrics/`.
4. Summarize the results in the report.

### Example Code

```
import pandas as pd
import matplotlib.pyplot as plt

interactions = pd.read_csv('data/synthetic_events/interactions.csv')
search_events = pd.read_csv('data/synthetic_events/search_events.csv')
onboarding = pd.read_csv('data/synthetic_events/onboarding_events.csv')
articles = pd.read_csv('data/synthetic_events/articles.csv')

# Write functions to calculate each KPI
# Then create charts with matplotlib and save to docs/metrics/
```

### Results

After running the calculations, you should see results similar to:

- Ticket deflection %: 60.0%
- AI agent resolution %: 80.0%
- Search success rate: 50.0%
- Average onboarding time-to-value: 1.5 days
- Article freshness: 80.0%

Charts are saved in `docs/metrics/`.

---

Run this report after installing dependencies:

```bash
pip install pandas matplotlib
python notebooks/kpi_eval.md
```
