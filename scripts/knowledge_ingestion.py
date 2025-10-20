"""
knowledge_ingestion.py

This script ingests Markdown-based knowledge articles, extracts YAML front matter
metadata, validates fields against a taxonomy, and outputs a structured JSON
file ready for AI training and retrieval. It demonstrates core ETL skills
relevant for knowledge management.
"""

import os
import json
import yaml
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class ArticleMetadata:
    """Represents metadata extracted from a knowledge article."""
    title: str
    domain: str
    subdomain: Optional[str]
    audience: str
    format: str
    status: str
    author: Optional[str] = None
    last_updated: Optional[str] = None
    path: Optional[str] = None


def load_taxonomy(taxonomy_path: str) -> Dict:
    """Load taxonomy definition from a YAML file."""
    with open(taxonomy_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_front_matter(content: str) -> Dict:
    """Extract YAML front matter from a Markdown file content."""
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            front_matter = content[3:end]
            try:
                return yaml.safe_load(front_matter)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML front matter: {e}")
    return {}


def ingest_article(path: str, taxonomy: Dict) -> ArticleMetadata:
    """Ingest a single Markdown article and return validated metadata."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    meta = parse_front_matter(content)
    if not meta:
        raise ValueError(f"No YAML front matter found in {path}")

    # Validate against taxonomy
    def validate(field: str, value: str) -> str:
        allowed = taxonomy['taxonomy'].get(field)
        if allowed and value not in allowed:
            raise ValueError(f"Value '{value}' for {field} not in taxonomy options: {allowed}")
        return value

    title = meta.get('title', os.path.basename(path))
    domain = validate('domain', meta.get('domain'))
    subdomain = meta.get('subdomain')
    if subdomain:
        # optionally validate subdomain if defined in taxonomy
        pass
    audience = validate('audience', meta.get('audience'))
    fmt = validate('format', meta.get('format'))
    status = validate('status', meta.get('status'))

    return ArticleMetadata(
        title=title,
        domain=domain,
        subdomain=subdomain,
        audience=audience,
        format=fmt,
        status=status,
        author=meta.get('author'),
        last_updated=meta.get('last_updated'),
        path=path,
    )


def ingest_directory(input_dir: str, taxonomy_path: str) -> List[ArticleMetadata]:
    """Walk a directory recursively and ingest all Markdown files."""
    taxonomy = load_taxonomy(taxonomy_path)
    articles: List[ArticleMetadata] = []
    for root, _, files in os.walk(input_dir):
        for name in files:
            if name.lower().endswith('.md'):
                file_path = os.path.join(root, name)
                try:
                    article = ingest_article(file_path, taxonomy)
                    articles.append(article)
                except Exception as exc:
                    print(f"Skipping {file_path}: {exc}")
    return articles


def export_to_json(articles: List[ArticleMetadata], output_path: str) -> None:
    """Export ingested articles metadata to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump([asdict(a) for a in articles], f, indent=2)


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Ingest Markdown knowledge articles and export metadata to JSON.")
    parser.add_argument('--input-dir', required=True, help='Directory containing Markdown knowledge articles')
    parser.add_argument('--taxonomy', required=True, help='Path to taxonomy YAML file')
    parser.add_argument('--output', default='knowledge_metadata.json', help='Output JSON file path')
    args = parser.parse_args()

    articles = ingest_directory(args.input_dir, args.taxonomy)
    export_to_json(articles, args.output)
    print(f"Ingested {len(articles)} articles and wrote metadata to {args.output}")


if __name__ == '__main__':
    main()
