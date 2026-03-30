#!/bin/bash
# Run test suite for Enterprise AI Platform
# Usage: ./scripts/run_tests.sh [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default options
COVERAGE=false
VERBOSE=false
MARKERS=""
PARALLEL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -m|--marker)
            MARKERS="$2"
            shift 2
            ;;
        -p|--parallel)
            PARALLEL=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./scripts/run_tests.sh [options]"
            echo ""
            echo "Options:"
            echo "  -c, --coverage    Generate coverage report"
            echo "  -v, --verbose     Verbose output"
            echo "  -m, --marker      Run specific test markers (e.g., 'unit', 'integration')"
            echo "  -p, --parallel    Run tests in parallel"
            echo "  -h, --help        Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./scripts/run_tests.sh                    # Run all tests"
            echo "  ./scripts/run_tests.sh -c                 # Run with coverage"
            echo "  ./scripts/run_tests.sh -m unit            # Run only unit tests"
            echo "  ./scripts/run_tests.sh -m integration -v  # Run integration tests verbosely"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Enterprise AI Platform - Test Suite${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# Check if virtual environment is activated
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${YELLOW}⚠ Virtual environment not activated${NC}"
    echo "Activating .venv..."
    source .venv/bin/activate
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest not found${NC}"
    echo "Installing pytest..."
    pip install pytest pytest-cov pytest-xdist
fi

# Build pytest command
PYTEST_CMD="pytest tests/"

if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
else
    PYTEST_CMD="$PYTEST_CMD -q"
fi

if [ -n "$MARKERS" ]; then
    PYTEST_CMD="$PYTEST_CMD -m $MARKERS"
    echo -e "Running tests with marker: ${YELLOW}$MARKERS${NC}"
fi

if [ "$PARALLEL" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -n auto"
    echo -e "Running tests in ${YELLOW}parallel mode${NC}"
fi

if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=pipeline --cov=monitoring --cov=agents --cov-report=html --cov-report=term"
    echo -e "Coverage report will be generated"
fi

echo ""
echo -e "${GREEN}Running tests...${NC}"
echo ""

# Run tests
if eval $PYTEST_CMD; then
    echo ""
    echo -e "${GREEN}✓ All tests passed!${NC}"
    
    if [ "$COVERAGE" = true ]; then
        echo ""
        echo -e "${GREEN}Coverage report generated:${NC}"
        echo "  - HTML: htmlcov/index.html"
        echo "  - Terminal: (shown above)"
        
        # Try to open coverage report in browser (Linux/Mac)
        if command -v xdg-open &> /dev/null; then
            xdg-open htmlcov/index.html &> /dev/null &
        elif command -v open &> /dev/null; then
            open htmlcov/index.html &> /dev/null &
        fi
    fi
    
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some tests failed${NC}"
    echo ""
    echo "To see more details, run with -v flag:"
    echo "  ./scripts/run_tests.sh -v"
    exit 1
fi
