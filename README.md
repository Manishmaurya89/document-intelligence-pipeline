# document-intelligence-pipeline

An end-to-end pipeline that generates structured documents using a local LLM, parses them with Docling, and extracts named entities with GLiNER.

---

## Pipeline Overview

```
Topic + Pages
     │
     ▼
[1] generator.py       → Ollama (LLaMA 3) generates article text
     │
     ▼
[2] output.py          → ReportLab renders dataset.pdf
     │
     ▼
[3] docling_processor.py → Docling parses PDF into text + structured sections
     │
     ▼
[4] gliner_processor.py  → GLiNER extracts named entities (NER)
     │
     ▼
Output files: dataset.pdf, extracted_text.txt, docling_output.json,
              structured_output.json, entities.json
```

---

## Requirements

- Python 3.9+
- [Ollama](https://ollama.ai/) running locally with `llama3` pulled

```bash
ollama pull llama3
```

Install Python dependencies:

```bash
pip install requests reportlab docling gliner
```

---

## Usage

```bash
python main.py
```

You will be prompted for:
- **Topic** — e.g. `World War II`
- **Pages** — e.g. `3`

---

## Output Files

| File | Description |
|---|---|
| `dataset.pdf` | Generated document rendered as PDF |
| `extracted_text.txt` | Plain text extracted by Docling |
| `docling_output.json` | Full Docling JSON representation |
| `structured_output.json` | Section-by-section breakdown |
| `entities.json` | Deduplicated named entities with scores |

---

## Key Improvements

- **Lazy GLiNER loading** — model loads on first use, not at import time
- **Retry logic** — generator retries up to 3 times on Ollama timeout
- **Improved heading detection** — avoids misclassifying short sentences
- **Entity deduplication** — keeps highest-confidence score per (text, label) pair
- **Safe table rendering** — skips rows with mismatched column counts

---

## Entity Labels

GLiNER extracts the following entity types:

- `country`
- `person`
- `organization`
- `event`
- `date`

---

## Project Structure

```
├── main.py                  # Pipeline orchestrator
├── config.py                # Model and URL configuration
├── generator.py             # LLM document generation (Ollama)
├── output.py                # PDF rendering (ReportLab)
├── docling_processor.py     # PDF parsing and section extraction (Docling)
└── gliner_processor.py      # Named entity recognition (GLiNER)
```
