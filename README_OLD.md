.# Knowledge & AI Strategy Demonstration

![Build](https://github.com/najsefoster1/knowledge-ai-strategy-python-project/actions/workflows/ci.yml/badge.svg)

## Overview
This project demonstrates a comprehensive knowledge management (KM) and AI readiness framework aligned with the requirements of a Knowledge & AI Strategy Lead role. It transforms knowledge assets into AI-ready data that powers intelligent agents, automation, and customer experiences.

## Governance & Taxonomy
- **Playbook**: See [km_strategy_playbook.md](km_strategy_playbook.md) for the full KM strategy and governance framework, including lifecycle, roles, SLAs, and RACI.
- **Taxonomy**: The [taxonomy.yaml](taxonomy.yaml) file defines domains, subdomains, audiences, formats, statuses, and metadata fields to ensure consistency and AI readiness.
- **Governance Addendum**: The [docs/governance_playbook_addendum.md](docs/governance_playbook_addendum.md) outlines lifecycle states, SLAs, required metadata, PII handling, and quality gates.

## Ingestion & Validation
- **Ingestion Script**: [scripts/knowledge_ingestion.py](scripts/knowledge_ingestion.py) reads Markdown articles from `data/sample_knowledge`, extracts YAML front matter, validates against the taxonomy, and writes a structured JSON file.
- **Quality Checks**: [script
- s/knowledge_quality_checks.py](scripts/knowledge_quality_checks.py) validates required fields and freshness. Run `make ingest` then `make validate` to generate `build/knowledge.json` and check quality.
- **Sample Data**: Place sample articles in [`data/sample_knowledge`](data/sample_knowledge) and run `make ingest` to process them.
- **Automated Tests**: See [`tests/test_ingestion.py`](tests/test_ingestion.py) for smoke tests verifying ingestion.

## KPIs & Measurement
Key AI-linked KPIs and measurement approaches are defined in [`docs/kpi_metrics.md`](docs/kpi_metrics.md). Metrics include ticket deflection rate, AI agent resolution rate, search success rate, onboarding time-to-value, and article freshness.


## Cross-Functional Adoption
- **Roles & Community**: KM Authors create content; subject-matter experts verify accuracy; the KM team governs standards; functional owners approve. A KM Council convenes regularly to review metrics and drive alignment across CX, Product, Engineering, and Marketing.
- **Processes**: Knowledge capture is embedded into daily workflows via intake templates and checklists. Contributors follow the taxonomy and lifecycle from draft to published and retired.
- **Change Leadership**: Adoption is driven through coaching, recognition of contributions, and integration into onboarding. SLAs ensure timely publishing and review.

## Getting Started
1. Clone this repository and install dependencies via `python -m pip install -r requirements.txt`.
2. Review the [km_strategy_playbook.md](km_strategy_playbook.md) and [taxonomy.yaml](taxonomy.yaml) to understand the framework.
3. Customize the taxonomy to your domain and add articles under `data/sample_knowledge`.
4. Run `make ingest` to generate `build/knowledge.json` and `make validate` to check quality.
5. Use the resulting JSON as a knowledge source for retrieval-augmented generation, chatbots, search indexes, or analytics pipelines.

## Repository Structure
- `km_strategy_playbook.md` – Strategy, governance, taxonomy, adoption.
- `taxonomy.yaml` – Knowledge taxonomy and metadata definitions.
- `scripts/knowledge_ingestion.py` – Python script for ingestion.
- `scripts/knowledge_quality_checks.py` – Validation script for metadata and freshness.
- `data/sample_knowledge/sample_article.md` – Example knowledge article.
- `docs/kpi_metrics.md` – KPI definitions and measurement.
- `.github/` – CI workflow and contribution templates.
- `tests/` – Unit tests for ingestion.
 
![Build](https://github.com/najsefoster1/knowledge-ai-strategy-python-project/actions/workflows/ci.yml/badge.svg)

# Knowledge & AI Strategy - Najse’s working demo

I wanted something you can skim in minutes and still see how I work. This repo shows how I design a knowledge backbone that is AI ready from day one - clear taxonomy, disciplined governance, and content that is written for both people and retrieval systems.

## Strategy & Governance

The `km_strategy_playbook.md` outlines the vision, roles, taxonomy standards, metadata requirements, and lifecycle phases from create to retire. The `taxonomy.yaml` defines domains, subdomains, audience types, formats, status values, and optional fields for energy and agriculture. Together they demonstrate how I embed governance into daily work and cascade ownership across teams.

## AI Readiness & Ingestion

The `scripts/knowledge_ingestion.py` and `scripts/knowledge_quality_checks.py` show how to parse Markdown articles with YAML front matter, validate metadata against the taxonomy, export it for retrieval, and enforce freshness and PII risk rules. The `docs/ai/embedding_schema.md` and `docs/ai/retrieval_policy.md` outline how to map metadata into vector embeddings and how to decide what content is public or private.

## Cross Domain Packs

I created domain packs for transportation, energy, and agriculture. Each pack contains a playbook, decision guides, articles with YAML front matter, and a screenshots folder. These packs turn raw domain knowledge into decision ready assets with service level agreements and review cadences. They show how to make knowledge useful for customer support, product, engineering, and marketing.

## Change Leadership

This README includes rollout steps, user stories, and adoption practices. It explains why knowledge capture matters, how to author AI ready articles, and how to build a community of practice. I wrote it in my own voice to make it approachable and human.

## Measurement & KPIs

The `docs/measurement/telemetry_spec.md`, synthetic events script, and KPI queries define and instrument AI linked metrics: ticket deflection percentage, AI agent resolution percentage, search success rate, onboarding time to value, and article freshness. These metrics help track the impact of knowledge management and AI across the customer lifecycle.

## Governance Trail & Housekeeping

A separate `github-housekeeping` repository will log renames, actions, errors, and rollback notes. It supports disciplined change control and makes it easy to see who did what and why.

## Getting Started

To run the ingestion and validation pipelines locally:

```
make setup
make ingest
make validate
make validate_ai
```

To explore the domain packs, navigate into `docs/packs/transportation`, `docs/packs/energy`, or `docs/packs/agriculture` and read the playbooks and articles. For more details about governance, taxonomy, AI readiness, or measurement, open the documents in the `docs` folder. I look forward to discussing how this approach can help your organization build an AI ready knowledge foundation.
