"""
Gradio app for the Knowledge & AI Strategy ingestion and validation system.

This app allows users to upload Markdown knowledge articles with YAML front
matter, optionally provide a taxonomy schema in JSON format, validate the
metadata and content, detect stale or invalid articles, and export AI‑ready
JSON for downstream use (e.g. embeddings and RAG).
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt

import gradio as gr
import yaml

# Additional imports for new features
import os
import re
try:
    import pdfplumber  # type: ignore
except ImportError:
    pdfplumber = None  # pdfplumber may not be installed in all environments
try:
    import docx  # type: ignore
except ImportError:
    docx = None  # python-docx may not be installed



# Default taxonomy schema used if none is provided by the user
DEFAULT_TAXONOMY = {
    "domain": [
        "product",
        "customer-support",
        "marketing",
        "engineering",
        "operations",
    ],
    "subdomain": {
        "product": ["features", "pricing", "release-notes"],
        "customer-support": ["troubleshooting", "faq", "how-to"],
        "marketing": ["positioning", "competitive-analysis"],
        "engineering": ["architecture", "runbooks", "postmortems"],
        "operations": ["policies", "procedures"],
    },
    "audience": ["customer", "internal", "partner"],
    "format": ["article", "faq", "how-to", "runbook", "policy"],
    "status": ["draft", "reviewed", "published", "deprecated"],
}

# Required fields for front matter
REQUIRED_FIELDS = [
    "title",
    "domain",
    "subdomain",
    "audience",
    "format",
    "status",
    "last_updated",
]


def parse_front_matter(content: str) -> Tuple[dict, str]:
    """Parse YAML front matter and return metadata and body."""
    meta: dict = {}
    body: str = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            _, front_matter, remainder = parts[0], parts[1], parts[2]
            try:
                meta = yaml.safe_load(front_matter) or {}
            except yaml.YAMLError:
                meta = {}
            body = remainder.strip()
    return meta, body


def extract_pdf(file_obj) -> str:
    """Extract text from a PDF file-like object.

    This function uses the pdfplumber library when available. If pdfplumber
    isn't installed or an error occurs during extraction, it returns an
    empty string. The caller should handle missing content gracefully.
    """
    if pdfplumber is None:
        return ""
    text = ""
    try:
        with pdfplumber.open(file_obj) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        return ""
    return text


def extract_docx(file_obj) -> str:
    """Extract text from a DOCX file-like object.

    Uses python-docx to read paragraphs. If the library isn't installed
    or an exception occurs, returns an empty string. The caller should
    handle missing content gracefully.
    """
    if docx is None:
        return ""
    try:
        document = docx.Document(file_obj)
        return "\n".join(paragraph.text for paragraph in document.paragraphs)
    except Exception:
        return ""


def strip_html_tags(text: str) -> str:
    """Remove basic HTML tags from text using a simple regex.

    This is a naive implementation and may not handle nested tags perfectly,
    but it's sufficient for stripping tags when HTML files are uploaded.
    """
    # Remove script/style tags and their content
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    # Remove all remaining tags
    text = re.sub(r"<[^>]+>", "", text)
    return text


def clean_text(text: str) -> str:
    """Remove emojis and non-ASCII characters from text.

    This uses a regex to strip characters outside of the basic multilingual
    plane. The resulting text should retain standard punctuation and
    printable ASCII characters.
    """
    # Remove characters that are not basic printable ASCII or common punctuation
    return re.sub(r"[^\x00-\x7F]+", "", text)


def validate_article(meta: dict, body: str, taxonomy: dict, stale_days: int = 365) -> List[str]:
    """Validate a single article's metadata and body.

    Returns a list of issue strings. An empty list means the article passed validation.
    """
    issues: List[str] = []
    # Check required fields
    for field in REQUIRED_FIELDS:
        if not meta.get(field):
            issues.append(f"Missing required field: {field}")
    # Validate taxonomy values
    domain = meta.get("domain")
    if domain and domain not in taxonomy.get("domain", []):
        issues.append(f"Invalid domain: {domain}")
    subdomain = meta.get("subdomain")
    if domain and subdomain:
        allowed_subs = taxonomy.get("subdomain", {}).get(domain)
        if allowed_subs and subdomain not in allowed_subs:
            issues.append(f"Invalid subdomain '{subdomain}' for domain '{domain}'")
    audience = meta.get("audience")
    if audience and audience not in taxonomy.get("audience", []):
        issues.append(f"Invalid audience: {audience}")
    fmt = meta.get("format")
    if fmt and fmt not in taxonomy.get("format", []):
        issues.append(f"Invalid format: {fmt}")
    status = meta.get("status")
    if status and status not in taxonomy.get("status", []):
        issues.append(f"Invalid status: {status}")
    # Staleness check
    last_updated = meta.get("last_updated")
    if last_updated:
        try:
            date_val = datetime.fromisoformat(str(last_updated))
            if datetime.utcnow() - date_val > timedelta(days=stale_days):
                issues.append(
                    f"Article is stale (> {stale_days} days since last_updated)"
                )
        except ValueError:
            issues.append("Invalid last_updated date format (use YYYY-MM-DD)")
  


 # PII heuristics in body
    import re
    # SSN detection
    if re.search(r"\b\d{3}-\d{2}-\d{4}\b", body):
                issues.append("Possible SSN-likelike pattern detected in body")
    # Email detection
    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", body):
        issues.append("Email addresses detected in body (verify necessity)")
    # Phone number detection (US formats)
    if re.search(r"(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b", body):
        issues.append("Possible phone number detected in body")

    return issues

  
    
def process_files(files: List[bytes], taxonomy_file: bytes | None) -> Tuple[str, List[dict]]:
    """Process uploaded files and return JSON string and table data.

    This function now supports multiple file types including Markdown, text,
    HTML, PDF and DOCX. It removes emojis/non-ASCII characters from the
    extracted text, infers missing metadata when possible, and uses the
    default taxonomy unless a custom taxonomy file is provided. Missing
    required metadata fields are marked as "Unknown" and a corresponding
    issue is recorded for transparency.
    """
    # Load taxonomy from user or use default
    taxonomy = DEFAULT_TAXONOMY
    if taxonomy_file is not None:
        try:
            loaded = json.loads(taxonomy_file.decode("utf-8"))
            if isinstance(loaded, dict) and "taxonomy" in loaded:
                taxonomy = loaded["taxonomy"]
            else:
                taxonomy = loaded
        except Exception:
            # If JSON parsing fails, ignore and keep default
            pass
    records: List[dict] = []
    bundle: List[dict] = []
    for uploaded_file in files:
        # Determine file name and extension if possible
        name = getattr(uploaded_file, "name", "uploaded")
        ext = os.path.splitext(name)[1].lower()
        # Read raw bytes
        try:
            content_bytes = uploaded_file.read()  # type: ignore[attr-defined]
        except Exception:
            content_bytes = uploaded_file  # assume it's bytes
        text = ""
        # Extract text based on extension
        if ext in [".pdf"]:
            text = extract_pdf(uploaded_file)
        elif ext in [".docx"]:
            text = extract_docx(uploaded_file)
        else:
            # For .md, .txt, .html and unknown types, decode as text
            try:
                text = content_bytes.decode("utf-8", errors="ignore")
            except Exception:
                text = ""
            # Strip basic HTML tags if file is HTML
            if ext in [".html", ".htm"]:
                text = strip_html_tags(text)
        # Clean emojis and non-ASCII characters
        text = clean_text(text)
        # Parse YAML front matter for metadata if present
        meta, body = parse_front_matter(text)
        # Infer missing title from file name if not provided
        base_name = os.path.splitext(os.path.basename(name))[0]
        if not meta.get("title") and base_name:
            meta["title"] = base_name.replace("_", " ")
        # Infer missing last_updated as today's date if not provided
        if not meta.get("last_updated"):
            meta["last_updated"] = datetime.utcnow().date().isoformat()
        # Fill missing required fields with 'Unknown' and record issue
        issues = validate_article(meta, body, taxonomy)
        for field in REQUIRED_FIELDS:
            if not meta.get(field):
                meta[field] = "Unknown"
                if f"Missing required field: {field}" not in issues:
                    issues.append(f"Missing required field: {field}")
        # Build row for DataFrame
        row = {
            "title": meta.get("title"),
            "domain": meta.get("domain"),
            "subdomain": meta.get("subdomain"),
            "audience": meta.get("audience"),
            "format": meta.get("format"),
            "status": meta.get("status"),
            "last_updated": meta.get("last_updated"),
            "issues": "; ".join(issues) if issues else "None",
        }
        records.append(row)
        # Append to bundle for JSON export
        bundle.append({
            "metadata": meta,
            "content": body,
            "issues": issues,
        })
    json_output = json.dumps(bundle, indent=2, default=str)
    return json_output, records


def build_interface() -> gr.Blocks:
    """Construct the Gradio interface with a custom dark theme and enhanced visuals.

    The returned interface allows users to upload Markdown knowledge articles with
    YAML front matter, optionally supply a taxonomy JSON file, validate the
    metadata and content, view the results in a table and JSON format, and
    visualize a summary chart of validation issues. Additional context such as
    a problem statement, user story, and required metadata fields is displayed
    to set the stage for executives and technical stakeholders.
    """
    # Define a custom dark theme with amber accent using the Soft theme base.  
    # Note: 'gold' is not a valid shortcut for gradio themes, so 'amber' is used to achieve a similar warm tone.
    theme = gr.themes.Soft(primary_hue="amber").set(
        body_background_fill="#0c0c0c",
        body_text_color="#e8e8e8",
        button_primary_background_fill="#d4a20c",
        button_primary_text_color="#0c0c0c",
        button_secondary_background_fill="#1c1c1c",
        block_shadow="0 4px 20px rgba(0,0,0,0.4)",
        block_border_width="1px",
    )

    with gr.Blocks(theme=theme) as demo:
        # High‑level context for the dashboard
        gr.Markdown(
            """
            # Knowledge & AI Strategy Ingestion and Validation

            **Problem Statement**
            
            Today's enterprises hold a wealth of knowledge in many shapes — FAQs, SOPs, PDFs, DOCX manuals, HTML pages and Markdown notes. Without structure and governance these assets cannot be harnessed by modern AI systems. Manual curation is tedious and error‑prone. This dashboard automates ingestion, cleansing, metadata validation, taxonomy compliance, staleness checks and PII detection so you can confidently feed any AI engine with trusted content.

            **User Story**
            
            *As a Knowledge & AI Strategy Lead* I need to upload multiple knowledge documents of varying formats and quickly see if they're AI‑ready. I don't want to worry about YAML front matter or custom taxonomies – the app should infer or ask for missing details and use our default taxonomy automatically. By exporting clean JSON and CSV, I can feed models like GPT, Claude, RAG pipelines, search indexes or summarizers without any surprises.

            **Mission Statement**

            *Scaling knowledge, one file at a time.* We believe well‑governed data fuels the next generation of predictive analytics, personalization and cross‑functional innovation. This tool is the first step: turning unstructured tribal knowledge into AI‑ingestible assets for any platform.

            **Required metadata fields**
            
            `title`, `domain`, `subdomain`, `audience`, `format`, `status`, `last_updated` (YYYY‑MM‑DD). Missing fields are automatically set to "Unknown" and flagged in the validation report.
            
            **Supported file formats**
            
            `.md`, `.txt`, `.html`, `.pdf`, `.docx` — upload as many as you need.
            """,
            label=None,
        )

        gr.Markdown("## 📂 Upload Your Knowledge Assets")
        with gr.Row():
            # Allow multiple file types and multiple uploads. Using `binary` returns bytes.
            file_input = gr.File(
                label="Knowledge Documents (md, txt, html, pdf, docx)",
                file_types=[".md", ".txt", ".html", ".htm", ".pdf", ".docx"],
                file_count="multiple",
                type="binary",
            )
            # Taxonomy upload is optional; if not provided, a default taxonomy is used.
            taxonomy_input = gr.File(
                label="Custom Taxonomy (optional)",
                file_types=[".json"],
                type="binary",
            )

        run_btn = gr.Button("🔍 Run Analysis", variant="primary")

        gr.Markdown("## 🧪 Validation Report")
        # Store the bundle (list of article dicts) and taxonomy used in hidden state
        bundle_state = gr.State([])
        taxonomy_state = gr.State(DEFAULT_TAXONOMY)

        json_output = gr.Code(label="AI‑ready JSON", language="json")
        # Make the validation table interactive so users can edit missing fields directly
        table = gr.Dataframe(
            headers=[
                "title",
                "domain",
                "subdomain",
                "audience",
                "format",
                "status",
                "last_updated",
                "issues",
            ],
            wrap=True,
            label="Validation Results",
            interactive=True,
        )

        gr.Markdown("## 📊 Issue Summary Chart")
        plot_output = gr.Plot(label="Issue Summary")

        # Button to apply edits from the interactive table back into the metadata. When clicked,
        # it revalidates each record using the current taxonomy and updates the JSON, table,
        # issue summary chart and hidden bundle state. This allows users to fill in missing
        # metadata fields without editing the source files.
        apply_btn = gr.Button("💾 Apply Edits to Metadata", variant="secondary")

        def categorize_issue(issue: str) -> str:
            """Categorize an issue string into high‑level categories."""
            lower = issue.lower()
            if "missing required field" in lower:
                return "Missing Fields"
            if "invalid" in lower:
                return "Invalid Values"
            if "stale" in lower:
                return "Stale Content"
            if "ssn" in lower or "email" in lower:
                return "PII"
            return "Other"

        def on_click(files: list[bytes], taxonomy_file: bytes | None):
            """Handle Run Analysis and return JSON, table rows, and a bar chart.

            If no files are uploaded, returns an empty JSON string, empty list, and
            an empty matplotlib figure.
            """
            # No files uploaded: clear outputs
            if not files:
                # Create empty figure for plot
                fig = plt.figure()
                plt.title("No Data")
                plt.axis("off")
                # Reset bundle and taxonomy state
                return "[]", [], fig, [], DEFAULT_TAXONOMY
            # Process files and get JSON/bundle
            json_str, records = process_files(files, taxonomy_file)
            # Build rows for table
            rows = [
                [
                    rec.get("title"),
                    rec.get("domain"),
                    rec.get("subdomain"),
                    rec.get("audience"),
                    rec.get("format"),
                    rec.get("status"),
                    rec.get("last_updated"),
                    rec.get("issues"),
                ]
                for rec in records
            ]
            # Retrieve the taxonomy used (either default or provided)
            taxonomy_used = DEFAULT_TAXONOMY
            if taxonomy_file is not None:
                try:
                    loaded = json.loads(taxonomy_file.decode("utf-8"))
                    taxonomy_used = loaded.get("taxonomy", loaded)
                except Exception:
                    pass
            # Aggregate issue categories
            from collections import Counter
            counter = Counter()
            for rec in records:
                issues_str = rec.get("issues")
                if not issues_str or issues_str == "None":
                    counter["No Issues"] += 1
                else:
                    for issue in issues_str.split("; "):
                        counter[categorize_issue(issue)] += 1
            # Create bar chart
            fig, ax = plt.subplots()
            categories = list(counter.keys())
            counts = [counter[c] for c in categories]
            ax.bar(categories, counts)
            ax.set_xlabel("Issue Category")
            ax.set_ylabel("Count")
            ax.set_title("Validation Issue Summary")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            # Build bundle for state: reconstruct bundle objects from JSON
            bundle = json.loads(json_str)
            return json_str, rows, fig, bundle, taxonomy_used

        def on_apply(table_data, bundle: list[dict], taxonomy: dict):
            """Apply edits from the interactive table back into the metadata.

            Accepts the current table data (which may be a pandas DataFrame or list of lists),
            updates each article's metadata based on the edited values, re-runs
            validation using the provided taxonomy, and returns updated outputs and
            state. If there is no data to apply, returns empty outputs.
            """
            # Guard against missing state
            if not bundle or table_data is None:
                fig = plt.figure()
                plt.title("No Data")
                plt.axis("off")
                return "[]", [], fig, [], taxonomy
            # Normalize the table data to a list of lists. Gradio may provide a
            # pandas DataFrame or a list. Attempt conversion gracefully.
            try:
                # If it's a pandas DataFrame, use .values.tolist()
                import pandas as pd  # type: ignore
                if isinstance(table_data, pd.DataFrame):
                    rows_list = table_data.values.tolist()
                else:
                    # Convert each row to a list if not already
                    rows_list = [list(row) if not isinstance(row, list) else row for row in table_data]
            except Exception:
                # Fallback: assume table_data is already a list of lists
                rows_list = table_data
            new_bundle: list[dict] = []
            new_records: list[list] = []
            from collections import Counter
            counter = Counter()
            # Ensure the number of rows matches number of articles
            num = min(len(rows_list), len(bundle))
            for idx in range(num):
                row = rows_list[idx]
                art = bundle[idx]
                meta = art.get("metadata", {})
                # Update metadata fields from row (matching column order)
                try:
                    meta["title"] = row[0] or meta.get("title")
                    meta["domain"] = row[1] or meta.get("domain")
                    meta["subdomain"] = row[2] or meta.get("subdomain")
                    meta["audience"] = row[3] or meta.get("audience")
                    meta["format"] = row[4] or meta.get("format")
                    meta["status"] = row[5] or meta.get("status")
                    meta["last_updated"] = row[6] or meta.get("last_updated")
                except Exception:
                    pass
                # Re-validate article with updated metadata
                content = art.get("content", "")
                issues = validate_article(meta, content, taxonomy)
                art["metadata"] = meta
                art["issues"] = issues
                # Build record for table
                issues_str = "; ".join(issues) if issues else "None"
                new_records.append([
                    meta.get("title"),
                    meta.get("domain"),
                    meta.get("subdomain"),
                    meta.get("audience"),
                    meta.get("format"),
                    meta.get("status"),
                    meta.get("last_updated"),
                    issues_str,
                ])
                # Update issue category counts
                if not issues:
                    counter["No Issues"] += 1
                else:
                    for issue in issues:
                        counter[categorize_issue(issue)] += 1
                new_bundle.append(art)
            # Build new JSON string
            json_str = json.dumps(new_bundle, indent=2, default=str)
            # Create bar chart
            fig, ax = plt.subplots()
            categories = list(counter.keys())
            counts = [counter[c] for c in categories]
            if categories:
                ax.bar(categories, counts)
                ax.set_xlabel("Issue Category")
                ax.set_ylabel("Count")
                ax.set_title("Validation Issue Summary")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
            else:
                plt.title("No Data")
                plt.axis("off")
            return json_str, new_records, fig, new_bundle, taxonomy

        # When Run Analysis is clicked, execute on_click and update both visible outputs and hidden state
        run_btn.click(
            on_click,
            inputs=[file_input, taxonomy_input],
            outputs=[json_output, table, plot_output, bundle_state, taxonomy_state],
        )

        # When Apply Edits is clicked, use the interactive table data, bundle state and taxonomy state
        # to update metadata and re-run validation. Note: table.value will contain the edited rows.
        apply_btn.click(
            on_apply,
            inputs=[table, bundle_state, taxonomy_state],
            outputs=[json_output, table, plot_output, bundle_state, taxonomy_state],
        )
    return demo


if __name__ == "__main__":
    interface = build_interface()
    interface.launch()
