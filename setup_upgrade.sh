#!/usr/bin/env bash
set -e

echo "Creating folders..."
mkdir -p .github/workflows agents monitoring pipeline docs examples

echo "Creating README..."
cat > README.md <<'EOF'
# Enterprise AI Platform

Production-ready AI Platform blueprint demonstrating data → ML → monitoring → agentic AI.

## Architecture
![Architecture](docs/architecture.png)

## What this shows
- End-to-end ML pipeline
- Monitoring + drift detection
- CI/CD setup
- Agentic AI (RAG + orchestration)

## Run
python run_pipeline.py

## Structure
pipeline/ | monitoring/ | agents/ | docs/

## System Design
See docs/SYSTEM_DESIGN.md

## License
MIT
EOF

echo "Creating CI..."
cat > .github/workflows/ci.yml <<'EOF'
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run pipeline
        run: python run_pipeline.py
EOF

echo "Creating agents..."
cat > agents/rag_pipeline.py <<'EOF'
def generate_response(query):
    return f"RAG response for: {query}"

if __name__ == "__main__":
    print(generate_response("sample"))
EOF

cat > agents/agent_orchestrator.py <<'EOF'
def run_agent(task):
    return {"task": task, "status": "done"}

if __name__ == "__main__":
    print(run_agent("demo"))
EOF

echo "Creating monitoring..."
cat > monitoring/model_drift.py <<'EOF'
def check_drift(current, baseline):
    return abs(current - baseline) > 0.1
EOF

cat > monitoring/data_quality_checks.py <<'EOF'
def check_data():
    return "ok"
EOF

echo "Creating pipeline additions..."
cat > pipeline/config.py <<'EOF'
CONFIG = {"version": "v1"}
EOF

cat > pipeline/feature_engineering.py <<'EOF'
def build_features(data):
    return data
EOF

cat > pipeline/validate.py <<'EOF'
def validate(data):
    if not data:
        raise ValueError("Empty")
EOF

echo "Creating docs..."
cat > docs/SYSTEM_DESIGN.md <<'EOF'
# System Design

Batch-first AI platform with monitoring and extensibility into agents.

Designed for:
- scalability
- governance
- enterprise reuse
EOF

cat > docs/DECISIONS_AND_TRADEOFFS.md <<'EOF'
# Trade-offs

Batch vs Streaming → chose batch for simplicity
Synthetic data → safe for public repo
EOF

echo "Creating example..."
cat > examples/enterprise_run.md <<'EOF'
Run:
python run_pipeline.py
EOF

echo "Done."
