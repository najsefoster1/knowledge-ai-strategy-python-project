---
title: "Knowledge & AI Strategy Validator"
colorFrom: yellow
colorTo: blue
sdk: gradio
sdk_version: "3.33.0"
app_file: app.py
pinned: false
---

# Knowledge & AI Strategy Validator

This project delivers a **zero‑friction validator** for turning messy knowledge articles into structured, AI‑ready assets.  
It supports multiple file formats—Markdown, text, HTML, PDF and DOCX—and automatically enriches each document with metadata, taxonomy validation, staleness checks and PII detection.  
The goal is to make your content ingestion pipeline **model‑agnostic**, so you can feed any downstream system—from GPT to Claude, Cohere, Llama 2/Mistral, SharePoint AI or Bedrock—without worrying about bad inputs.

## ⚙️ Features

- **Multi‑file, multi‑format uploads**: Drag and drop as many `.md`, `.txt`, `.html`, `.pdf` or `.docx` files as you like. The app parses each document and extracts or infers metadata automatically.
- **Default taxonomy loaded**: A built‑in `taxonomy_schema.json` defines domains, subdomains, audiences, formats and statuses. You can optionally upload a custom taxonomy, but it’s not required.
- **Metadata inference & editing**: The app extracts YAML front matter when present and infers missing values (e.g. file name becomes the title). Required fields (`title`, `domain`, `subdomain`, `audience`, `format`, `status`, `last_updated`) are highlighted and exposed as editable dropdowns and a calendar input.  
  Missing values are flagged and you can update them directly in the interface.
- **Staleness & PII detection**: Articles older than 365 days are marked as stale. The body text is scanned for SSNs, phone numbers and email addresses. Detected issues are summarized in a bar chart.
- **Clean output**: After validation you can download a single `.json` for each file, a combined `.zip` of all JSON objects, or an aggregated `.csv` ready for spreadsheets or dashboards.
- **Intuitive UI**: Built with Gradio Blocks and a dark theme with gold accents. Tooltips explain each field, and a collapsible panel illustrates how this validator fits into the Knowledge‑to‑AI pipeline.
- **Model‑agnostic pipeline**: Designed to prepare documents for GPT, Claude, Cohere, Llama 2/Mistral, SharePoint AI, Bedrock/SageMaker and any future model.

## 📂 How to Use

1. **Upload documents** – Drag and drop multiple files into the “Knowledge Documents” box or click to select them. Supported formats are `.md`, `.txt`, `.html`, `.pdf` and `.docx`.
2. **(Optional) Upload a custom taxonomy** – If you have a company‑specific taxonomy, drop a JSON file in the second box. Otherwise, the default taxonomy is loaded automatically.
3. **Run analysis** – Click **Run Analysis**. The app cleans the content, infers metadata, and validates each document against the taxonomy.
4. **Review & edit** – The validation table highlights missing or invalid fields. Use the dropdowns and date picker to correct metadata. Click **Apply Edits** to re‑validate.
5. **Download AI‑ready assets** – Choose JSON or CSV export. You can download individual files or a ZIP containing all JSON outputs.

Annotated screenshots below illustrate the workflow:

| Step | Description | Screenshot |
|-----|-------------|-----------|
| Upload | The upload section allows you to drag multiple files in at once and optionally provide a custom taxonomy. | *(screenshot of upload section)* |
| Validate & Edit | After clicking **Run Analysis**, the app displays a table of metadata and issues. Use the dropdowns to select valid values and the calendar to adjust dates. | *(screenshot showing validation results and editable metadata)* |
| Export | Once everything looks good, export your dataset as JSON or CSV. | *(screenshot of export options)* |

> **Friendly messages guide you through the process** — if a document is missing an audience tag you’ll see “Audience tag missing—select one (Internal, Customer, Partner)” and if it contains an email address you’ll be prompted to verify.

## 🧐 Why It Matters

Modern AI applications depend on clean, well‑structured knowledge. Feeding unvalidated data into a large language model can lead to hallucinations, compliance issues and frustrated users. This validator serves as the first step in the **Knowledge‑to‑AI pipeline**, ensuring:

* **Consistency** – Metadata fields follow a controlled vocabulary and conform to your taxonomy.
* **Freshness** – Stale content is flagged so you can prioritize updates.
* **Safety** – Sensitive information like SSNs and emails are caught early.
* **Interoperability** – The output format works with GPT, Claude, Cohere, Llama 2/Mistral, SharePoint AI and Bedrock/SageMaker.

By establishing trust in your knowledge base up front, your downstream AI (chatbots, search, summarization engines) delivers more accurate and reliable answers.

## 💪 Local Development

Clone the repository and install dependencies in a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run the app locally:

```bash
python app.py
```

Open `http://localhost:7860` in your browser. You can customize the default taxonomy in `taxonomy_schema.json`.

## 🚀 Live Demo

Try the live Hugging Face Space here: [najsefoster/Knowledge‑ai‑strategy](https://huggingface.co/spaces/najsefoster/Knowledge-ai-strategy)  
This version is continuously deployed from the `main` branch and reflects the latest features.

## 💾 Repository Contents

```text
knowledge_ai_strategy_space/
├── app.py                  # Gradio app source code
├── requirements.txt        # Python dependencies
├── taxonomy_schema.json    # Default taxonomy definition
├── README.md               # Project overview and instructions
└── sample_data/            # Sample documents for demonstration
    ├── article_demo.md
    ├── article_example.pdf
    └── article_example.docx
```

## 📚 Coursework & Background

This project is part of my ongoing exploration of **knowledge management**, **AI strategy**, and **customer engagement**. I recently completed a **Master of Science in Information Systems & Business Analytics** at Park University (2025), with coursework in **Business Intelligence**, **Data Visualization**, **Machine Learning**, **SQL**, **Advanced Excel**, **Python Programming**, **IT Governance** and **Decision Science**.  
This builds on my experience designing knowledge backbones for the U.S. Air Force and driving AI initiatives in the private sector. I thrive in fast‑paced environments and love turning ambiguous challenges into scalable solutions.

---

*©2025 Najse Foster — Knowledge & AI Strategy Ingestion Validator*
