# AI-Assisted Resilient Data Pipeline

A production-ready, agentic AI–driven data system that automatically detects, diagnoses, and heals data quality issues during NLP-based sentiment analysis using Apache Airflow and local LLMs via Ollama.

This project demonstrates how Agentic AI + LLMs can be embedded into data engineering workflows to create resilient, self-correcting pipelines instead of brittle, failure-prone systems.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-3.0+-017CEE?logo=apache-airflow)
![Ollama](https://img.shields.io/badge/Ollama-LLaMA%203.2-orange)
![License](https://img.shields.io/badge/License-MIT-green)


## Overview

Traditional data pipelines fail when they encounter malformed or unexpected data. This project demonstrates an **agentic, self-healing approach** where the pipeline:

1. **Diagnoses** data quality issues in real-time
2. **Heals** problematic records automatically
3. **Processes** sentiment analysis using local LLM (Ollama)
4. **Reports** detailed health metrics and healing statistics

## Architecture
![ResilientSentimentPipeline.jpeg](assets/ResilientSentimentPipeline.jpeg)


## Features

| Feature | Description |
|---------|-------------|
| **Agentic Self-Healing** | Automatically fixes missing, malformed, or invalid data |
| **Config-Driven Healing Rules** | Healing logic defined via configuration, not hard-coded |
| **Healing History per Record** | Tracks every healing action applied to each review |
| **Confidence-Aware Sentiment Output** | Classifies predictions into HIGH / MEDIUM / LOW confidence |
| **LLM Abstraction Layer** | Decouples sentiment analysis logic from the underlying LLM |
| **Local LLM** | Uses Ollama with LLaMA 3.2 - no external API calls |
| **Batch Processing** | Configurable batch sizes with offset support |
| **Parallel Execution** | Scale with multiple concurrent DAG runs |
| **Health Monitoring** | Real-time pipeline health status reporting |
| **Graceful Degradation** | Falls back to neutral predictions on failures |
| **Detailed Metrics** | Sentiment distribution, confidence scores, healing stats |

## Self-Healing Capabilities

The pipeline automatically detects and heals the following data quality issues:

| Error Type | Detection | Healing Action |
|------------|-----------|----------------|
| `missing_text` | Text field is `None` | Fill with placeholder |
| `empty_text` | Text is empty or whitespace | Fill with placeholder |
| `wrong_type` | Text is not a string | Type conversion |
| `special_characters_only` | No alphanumeric characters | Replace with marker |
| `too_long` | Exceeds max length (2000 chars) | Truncate with ellipsis |

## Advanced Agentic Capabilities

## 1. Config-Driven Healing Rules
Healing logic is fully configuration-driven, allowing new data quality rules to be added or modified without changing DAG code. This makes the pipeline adaptable to evolving data contracts.

## 2. Healing History per Record
Each processed record maintains a detailed healing trace, including:
- Detected error type
- Healing action applied
- Timestamp of correction  
This improves auditability, debugging, and observability.

## 3. Confidence-Aware Sentiment Output
In addition to sentiment labels, the pipeline assigns confidence bands:
- **HIGH** (≥ 0.85)
- **MEDIUM** (0.65–0.84)
- **LOW** (< 0.65)

This enables downstream systems to make risk-aware decisions.

## 4. LLM Abstraction Layer
Sentiment analysis is implemented via an abstraction layer, allowing the underlying LLM backend to be swapped (e.g., Ollama today, other providers in the future) without impacting pipeline logic.

## Prerequisites

- Python 3.12+
- [Ollama](https://ollama.ai/) installed and running
- Apache Airflow 3.0+
- 8GB+ RAM recommended for LLM inference

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PavanMahindrakar/AI-assisted-resilient-data-pipeline.git
   cd ResilientSentimentPipeline
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Ollama**
   ```bash
   # Download and install Ollama (Ubuntu)
   curl -fsSL https://ollama.com/install.sh | sh

   # Start Ollama service
   ollama serve

   # Pull the model (in a new terminal)
   ollama pull llama3.2
   ```

5. **Initialize Airflow**
   ```bash
   export AIRFLOW_HOME=$(pwd)
   airflow db migrate
   ```

6. **Start Airflow services**
   ```bash
   airflow standalone
   ```

   Or run components separately:
   ```bash
   # Terminal 1: Start webserver
   airflow webserver --port 8080

   # Terminal 2: Start scheduler
   airflow scheduler
   ```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PIPELINE_BASE_DIR` | Project root | Base directory for the pipeline |
| `PIPELINE_INPUT_FILE` | `input/yelp_academic_dataset_review.json` | Input data file |
| `PIPELINE_OUTPUT_DIR` | `output/` | Output directory |
| `PIPELINE_MAX_TEXT_LENGTH` | `2000` | Max characters per review |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.2` | Model for sentiment analysis |
| `OLLAMA_TIMEOUT` | `120` | Request timeout (seconds) |
| `OLLAMA_RETRIES` | `3` | Retry attempts on failure |

### DAG Parameters

Configure via Airflow UI or CLI:

```json
{
  "input_file": "/path/to/reviews.json",
  "batch_size": 100,
  "offset": 0,
  "ollama_model": "llama3.2"
}
```

## Usage

### Single Run (Airflow UI)

1. Open Airflow UI at `http://localhost:8080`
2. Navigate to `self_healing_pipeline`
3. Click "Trigger DAG" and configure parameters
4. Monitor execution in the Graph view

### Single Run (CLI)

```bash
airflow dags trigger ResilientSentimentPipeline\
    --conf '{"batch_size": 100, "offset": 0}'
```

### Batch Processing (Large Datasets)

Use the batch runner for processing millions of records:

```bash
# Process 5M records with batch size 1000 (sequential)
python scripts/batch_runner.py --total 5000000 --batch-size 1000

# Process with 5 parallel DAG runs
python scripts/batch_runner.py --total 5000000 --batch-size 5000 --parallel 5

# Resume from offset 100000
python scripts/batch_runner.py --total 5000000 --batch-size 1000 --start 100000

# Dry run to preview triggers
python scripts/batch_runner.py --total 5000000 --batch-size 10000 --dry-run
```

## Pipeline Tasks

| Task | Description | Output |
|------|-------------|--------|
| `load_model` | Initialize Ollama model, pull if needed | Model config |
| `load_reviews` | Read reviews from JSON file with offset | List of reviews |
| `diagnose_and_heal_batch` | Detect and fix data quality issues | Healed reviews |
| `batch_analyze_sentiment` | LLM sentiment classification | Analyzed reviews |
| `aggregate_results` | Compute statistics, write output | Summary JSON |
| `generate_health_report` | Assess pipeline health status | Health report |

## Health Monitoring

The pipeline generates health status based on processing outcomes:

| Status | Condition |
|--------|-----------|
| `HEALTHY` | <50% reviews needed healing, no degradation |
| `WARNING` | >50% reviews needed healing |
| `DEGRADED` | Some inference failures occurred |
| `CRITICAL` | >10% records in degraded state |

### Sample Health Report

```json
{
  "pipeline": "ResilientSentimentPipeline",
  "health_status": "HEALTHY",
  "metrics": {
    "total_processed": 100,
    "success_rate": 0.85,
    "healing_rate": 0.15,
    "degradation_rate": 0.0
  },
  "sentiment_distribution": {
    "POSITIVE": 45,
    "NEGATIVE": 30,
    "NEUTRAL": 25
  }
}
```

## Output

Results are saved to `output/` with timestamped filenames:

```
output/
└── sentiment_analysis_summary_2025-12-08_14-30-00_Offset0.json
```

### Output Schema

```json
{
  "run_info": {
    "timestamp": "2025-12-08T14:30:00",
    "batch_size": 100,
    "offset": 0
  },
  "totals": {
    "processed": 100,
    "success": 85,
    "healed": 15,
    "degraded": 0
  },
  "rates": {
    "success_rate": 0.85,
    "healing_rate": 0.15,
    "degradation_rate": 0.0
  },
  "sentiment_distribution": {...},
  "healing_statistics": {...},
  "results": [...]
}
```

### Record-Level Output (inside `results`)
Each entry in the `results` array represents a processed review with enhanced observability:

```json
{
  "review_id": "abc123",
  "text": "Great service and food!",
  "original_text": "Great service and food!!!!!!!!",
  "predicted_sentiment": "POSITIVE",
  "confidence": 0.91,
  "confidence_level": "HIGH",
  "status": "healed",
  "healing_applied": true,
  "healing_action": "truncated_text",
  "error_type": "too_long",
  "healing_history": [
    {
      "error_type": "too_long",
      "action": "truncated_text",
      "timestamp": "2025-12-08T14:30:00"
    }
  ],
  "metadata": {
    "user_id": "u123",
    "date": "2015-03-05",
    "useful": 2,
    "funny": 0,
    "cool": 1
  }
}
```

## Project Structure

```
ResilientSentimentPipeline/
├── dags/
│     ├── agentic_pipeline_dag.py    # Main DAG definition
      └── init.py
├── core/
      ├── healing_engine.py          # Config-driven healing logic
      ├── sentiment_engine.py        # LLM abstraction layer
      ├── response_parser.py         # Robust LLM response parsing
      ├── confidence_utils.py        # Confidence band computation
      └── init.py
├── scripts/
│     └── batch_runner.py            # Batch processing script
├── input/                           # Input data directory
├── output/                          # Generated results
├── logs/                            # Airflow logs
├── requirements.txt                 # Python dependencies
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Author

**Pavan Mahindrakar** - [@PavanMahindrakar](https://github.com/PavanMahindrakar)

---

If you found this project helpful, please consider giving it a star!
# cache refresh
