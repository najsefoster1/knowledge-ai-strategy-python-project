.PHONY: setup format lint test ingest validate validate_ai

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

format:
	black .
	isort .

lint:
	flake8flake8 --max-line-length=120 .
	yamllint .
	mdformat --check .

test:
	pytest -q

ingest:
	python scripts/knowledge_ingestion.py --input-dir data/sample_knowledge --taxonomy taxonomy.yaml --output build/knowledge.json

validate:
	python scripts/knowledge_quality_checks.py --input build/knowledge.json --min-freshness-days 90

validate_ai:
	# Placeholder for AI validation
	python -c "print('validate_ai ok')"		
