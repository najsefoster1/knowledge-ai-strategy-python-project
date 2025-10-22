![Build](https://github.com/najsefoster1/knowledge-ai-strategy-python-project/actions/workflows/ci.yml/badge.svg)

# Knowledge & AI Strategy - working demo

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
