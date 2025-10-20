# Knowledge & AI Strategy Demonstration

![Build](https://github.com/najsefoster1/knowledge-ai-strategy-python-project/actions/workflows/ci.yml/badge.svg)

## Overview
This project demonstrates a comprehensive knowledge management (KM) and AI readiness framework aligned with the requirements of a Knowledge & AI Strategy Lead role. It transforms knowledge assets into AI-ready data that powers intelligent agents, automation, and customer experiences.

## Governance & Taxonomy
- **Playbook**: See [km_strategy_playbook.md](km_strategy_playbook.md) for the full KM strategy and governance framework, including lifecycle, roles, SLAs, and RACI.
- **Taxonomy**: The [taxonomy.yaml](taxonomy.yaml) file defines domains, subdomains, audiences, formats, statuses, and metadata fields to ensure consistency and AI readiness.
- **Governance Addendum**: The [docs/governance_playbook_addendum.md](docs/governance_playbook_addendum.md) outlines lifecycle states, SLAs, required metadata, PII handling, and quality gates.

## Ingestion & Validation
- **Ingestion Script**: [scripts/knowledge_ingestion.py](scripts/knowledge_ingestion.py) reads Markdown articles from `data/sample_knowledge`, extracts YAML front matter, validates against the taxonomy, and writes a structured JSON file.
- **Quality Checks**: [scripts/knowledge_quality_checks.py](scripts/knowledge_quality_checks.py) validates required fields and freshness. Run `make ingest` then `make validate` to generate `build/knowledge.json` and check quality.
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

## License
MIT License. See [LICENSE](LICENSE) for details.
