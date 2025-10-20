from pathlib import Path
import json, subprocess, sys

def test_ingest_runs():
    Path("build").mkdir(exist_ok=True)
    subprocess.check_call([sys.executable, "scripts/knowledge_ingestion.py",
                           "--input-dir", "data/sample_knowledge",
                           "--taxonomy", "taxonomy.yaml",
                           "--output", "build/knowledge.json"])
    assert Path("build/knowledge.json").exists()
    data = json.loads(Path("build/knowledge.json").read_text())
    assert isinstance(data, list) and len(data) >= 1
