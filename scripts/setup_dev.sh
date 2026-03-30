#!/bin/bash
# Setup development environment for Enterprise AI Platform
# Usage: ./scripts/setup_dev.sh

set -e  # Exit on error

echo "================================================"
echo "Enterprise AI Platform - Development Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]]; then
    echo "❌ Error: Python $required_version or higher required (found $python_version)"
    exit 1
fi
echo "✓ Python $python_version detected"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo "✓ Main dependencies installed"
fi

if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt --quiet
    echo "✓ Development dependencies installed"
else
    # Install common dev dependencies if file doesn't exist
    echo "Installing common development dependencies..."
    pip install --quiet \
        pytest \
        pytest-cov \
        pytest-mock \
        black \
        isort \
        flake8 \
        mypy \
        pre-commit
    echo "✓ Development dependencies installed"
fi
echo ""

# Setup pre-commit hooks
echo "Setting up pre-commit hooks..."
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo "✓ Pre-commit hooks installed"
else
    echo "⚠ pre-commit not available, skipping hook installation"
fi
echo ""

# Create necessary directories
echo "Creating project directories..."
mkdir -p data/sample_data
mkdir -p logs
mkdir -p outputs
mkdir -p models
echo "✓ Directories created"
echo ""

# Setup environment variables
echo "Setting up environment variables..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ .env file created from .env.example"
        echo "⚠ Please edit .env and fill in your credentials"
    else
        cat > .env << 'EOF'
# Environment Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO

# Data Sources
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
S3_BUCKET=your-bucket-name

# API Keys (DO NOT commit actual values)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Monitoring
ENABLE_MONITORING=true
EOF
        echo "✓ .env file created with defaults"
        echo "⚠ Please edit .env and fill in your credentials"
    fi
else
    echo "✓ .env file already exists"
fi
echo ""

# Run initial tests
echo "Running initial tests..."
if pytest tests/ -q --tb=no 2>/dev/null; then
    echo "✓ Tests passed"
else
    echo "⚠ Some tests failed or no tests found (this is OK for initial setup)"
fi
echo ""

# Summary
echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Edit .env file with your credentials"
echo "3. Run tests: pytest tests/"
echo "4. Run pipeline: python run_pipeline.py"
echo ""
echo "Development commands:"
echo "  - Run tests: ./scripts/run_tests.sh"
echo "  - Format code: black . && isort ."
echo "  - Lint code: flake8 ."
echo "  - Type check: mypy pipeline/"
echo ""
echo "Happy coding! 🚀"
