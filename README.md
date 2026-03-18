# Enterprise AI Platform Demo
**Repo title:** Enterprise AI Platform (Snowflake + MLOps Example)

**Overview:** End-to-end platform for scalable AI, from data ingestion to curated features, model training, deployment, and monitoring.

**Tags:** MLOps, data-engineering, snowflake, databricks

## What this repo shows
- Cloud-neutral reference architecture for enterprise AI delivery
- Runnable Python demo pipeline on synthetic customer-usage data
- CI/CD starter templates and infrastructure-as-code stubs
- Slide deck and one-page summary for stakeholder walkthroughs

## Usage
### Local run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_pipeline.py
```

### Docker run
```bash
docker build -t enterprise-ai-platform .
docker run --rm enterprise-ai-platform
```

**Requirements:** Python 3.9+, Docker (optional)

## Architecture
![Enterprise AI Platform architecture](docs/architecture.png)

The flow is:
`Data sources -> ingestion -> raw zone -> curated zone -> feature store -> model training -> registry -> scoring -> monitoring`

## Repository structure
```text
enterprise-ai-platform/
├── run_pipeline.py
├── pipeline/
│   ├── etl.py
│   ├── train.py
│   └── monitor.py
├── models/
│   ├── training_placeholder.ipynb
│   └── monitoring_placeholder.ipynb
├── infra/
│   ├── github-actions-ci.yml
│   ├── databricks_job_stub.yml
│   ├── snowflake_objects.sql
│   └── terraform/main.tf
├── data/sample_data/
│   └── synthetic_customer_usage.csv
└── docs/
    ├── architecture.png
    ├── architecture.pdf
    ├── one_page_summary.pdf
    └── platform_deck.pdf
```

## Results
Simulated workflow output:
- 120k records processed
- Model accuracy = 92%
- Drift status = green

A runnable local sample is included; presentation metrics are fixed demo KPIs for consistency.

See `docs/pipeline_results.json` after executing the pipeline.

## Links
- [Newsletter #X](https://www.linkedin.com/newsletters/scaling-ai-without-hype) for details

## IP checklist
- Public cloud or open frameworks only
- Synthetic data only; no customer data
- Abstract company names and environments
- Architecture patterns only; no proprietary code

## License
MIT
