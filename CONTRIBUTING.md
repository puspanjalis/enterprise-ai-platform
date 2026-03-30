# Contributing to Enterprise AI Platform

Thank you for your interest in contributing to the Enterprise AI Platform. This document provides guidelines for contributing code, documentation, and other improvements.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows professional engineering standards:

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Assume good intentions
- Collaborate transparently

## How to Contribute

### Types of Contributions

**Bug Reports**
- Search existing issues first
- Provide minimal reproducible example
- Include environment details (OS, Python version, etc.)
- Use issue template

**Feature Requests**
- Describe the use case and business value
- Explain current workarounds if any
- Consider if it fits platform scope
- Discuss in issues before implementing

**Code Contributions**
- Start with issues labeled "good first issue"
- Discuss approach before large changes
- Follow code standards
- Include tests and documentation
- Submit focused pull requests

**Documentation**
- Fix typos and clarify unclear sections
- Add examples and tutorials
- Improve troubleshooting guides
- Update outdated information

## Development Setup

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Git
- PostgreSQL (for local development)

### Local Environment

```bash
# Clone repository
git clone https://github.com/puspanjalis/enterprise-ai-platform.git
cd enterprise-ai-platform

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit install

# Run tests to verify setup
pytest tests/
```

### Docker Development

```bash
# Build image
docker-compose build

# Run platform locally
docker-compose up

# Run tests in Docker
docker-compose run --rm platform pytest tests/
```

## Code Standards

### Python Style

Follow PEP 8 with these specifics:

- Line length: 100 characters
- Use Black for formatting
- Use isort for imports
- Use type hints
- Docstrings in Google style

```python
# Example
from typing import List, Dict, Optional
import pandas as pd

def process_data(
    df: pd.DataFrame,
    columns: List[str],
    config: Optional[Dict] = None
) -> pd.DataFrame:
    """
    Process dataframe according to configuration.
    
    Args:
        df: Input dataframe to process
        columns: Columns to include in processing
        config: Optional configuration dictionary
    
    Returns:
        Processed dataframe
    
    Raises:
        ValueError: If required columns missing
    """
    if config is None:
        config = {}
    
    # Processing logic
    result = df[columns].copy()
    return result
```

### Code Organization

```
module/
├── __init__.py          # Module exports
├── core.py              # Core functionality
├── utils.py             # Helper functions
├── config.py            # Configuration
└── tests/
    ├── test_core.py     # Core tests
    └── test_utils.py    # Utility tests
```

### Naming Conventions

- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`
- Files: `snake_case.py`

## Testing Guidelines

### Test Structure

```python
import pytest
from pipeline.feature_engineering import FeatureTransformer

class TestFeatureTransformer:
    """Tests for FeatureTransformer class."""
    
    def test_transform_basic(self):
        """Test basic transformation."""
        transformer = FeatureTransformer()
        result = transformer.transform(data)
        assert result is not None
    
    def test_transform_missing_columns(self):
        """Test handling of missing columns."""
        transformer = FeatureTransformer()
        with pytest.raises(ValueError):
            transformer.transform(invalid_data)
```

### Coverage Requirements

- New code: 80% minimum coverage
- Critical paths: 100% coverage
- Run: `pytest --cov=pipeline tests/`

### Test Types

**Unit Tests**
- Test individual functions/classes
- Mock external dependencies
- Fast execution (< 1 second each)

**Integration Tests**
- Test component interactions
- Use real dependencies where practical
- Slower but more realistic

**End-to-End Tests**
- Test full pipeline execution
- Run on sample data
- Validate outputs

## Documentation

### Code Documentation

Every module, class, and public function must have docstrings:

```python
def calculate_psi(expected: np.ndarray, actual: np.ndarray, bins: int = 10) -> float:
    """
    Calculate Population Stability Index (PSI).
    
    PSI measures drift in feature distributions:
    - PSI < 0.1: No significant change
    - PSI 0.1-0.2: Moderate change, investigate
    - PSI > 0.2: Significant change, action needed
    
    Args:
        expected: Reference distribution (training data)
        actual: Current distribution (production data)
        bins: Number of bins for bucketing (default: 10)
    
    Returns:
        PSI score as float
        
    Example:
        >>> expected = np.random.normal(0, 1, 1000)
        >>> actual = np.random.normal(0.2, 1.1, 1000)
        >>> psi = calculate_psi(expected, actual)
        >>> print(f"PSI: {psi:.3f}")
        PSI: 0.156
    """
```

### README Updates

When adding features:
- Update README with usage example
- Add to feature list
- Update architecture diagram if applicable

### CHANGELOG

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
## [Unreleased]

### Added
- New feature X for use case Y

### Changed
- Improved performance of Z by 40%

### Fixed
- Bug in validation logic causing false positives
```

## Pull Request Process

### Before Submitting

```bash
# 1. Update from main
git fetch origin
git rebase origin/main

# 2. Run tests
pytest tests/

# 3. Check code style
black .
isort .
flake8 .

# 4. Update documentation
# Edit relevant docs in docs/

# 5. Update CHANGELOG
# Add entry under [Unreleased]
```

### PR Template

```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Changes
- Change 1
- Change 2

## Testing
How was this tested?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Code style checks pass
```

### Review Process

1. Automated checks must pass (CI/CD)
2. At least one approval required
3. No unresolved comments
4. Up to date with main branch

### After Merge

- Delete feature branch
- Monitor deployment to staging
- Verify in production after release

## Release Process

Maintained by platform team:

1. Create release branch: `release/vX.Y.Z`
2. Update version in `__init__.py`
3. Finalize CHANGELOG
4. Create GitHub release with notes
5. Tag: `vX.Y.Z`
6. Deploy to production

## Getting Help

- Documentation: `docs/`
- Issues: GitHub Issues
- Questions: #ml-platform Slack
- Email: platform-team@example.com

## Recognition

Contributors are listed in:
- README Contributors section
- Release notes
- Annual contributor spotlight

Thank you for making the Enterprise AI Platform better!
