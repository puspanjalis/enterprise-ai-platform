"""
Shared test configuration and fixtures.

This module provides common test utilities, fixtures, and configuration
used across the test suite.
"""

import pytest
import pandas as pd
import numpy as np
from typing import Dict, Any
from pathlib import Path


@pytest.fixture
def sample_dataframe():
    """
    Fixture providing a sample DataFrame for testing.
    
    Returns:
        pd.DataFrame: Sample data with typical enterprise features
    """
    np.random.seed(42)
    n_rows = 1000
    
    return pd.DataFrame({
        'customer_id': range(1, n_rows + 1),
        'age': np.random.randint(18, 80, n_rows),
        'income': np.random.uniform(20000, 200000, n_rows),
        'credit_score': np.random.randint(300, 850, n_rows),
        'account_balance': np.random.uniform(-1000, 50000, n_rows),
        'transaction_count': np.random.randint(0, 100, n_rows),
        'is_active': np.random.choice([True, False], n_rows),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_rows),
        'timestamp': pd.date_range('2024-01-01', periods=n_rows, freq='H')
    })


@pytest.fixture
def sample_config():
    """
    Fixture providing sample configuration for testing.
    
    Returns:
        dict: Sample configuration dictionary
    """
    return {
        'data_source': {
            'type': 'postgresql',
            'host': 'localhost',
            'port': 5432,
            'database': 'test_db'
        },
        'feature_engineering': {
            'numerical_features': ['age', 'income', 'credit_score'],
            'categorical_features': ['region', 'is_active'],
            'scaling_method': 'standard'
        },
        'model': {
            'type': 'random_forest',
            'n_estimators': 100,
            'max_depth': 10
        },
        'monitoring': {
            'drift_threshold': 0.2,
            'data_quality_threshold': 0.95
        }
    }


@pytest.fixture
def test_data_dir(tmp_path):
    """
    Fixture providing temporary directory for test data.
    
    Args:
        tmp_path: pytest tmp_path fixture
        
    Returns:
        Path: Temporary directory path
    """
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    return data_dir


class MockDatabaseConnection:
    """Mock database connection for testing."""
    
    def __init__(self):
        self.connected = False
        self.queries_executed = []
    
    def connect(self):
        """Simulate database connection."""
        self.connected = True
        return self
    
    def execute(self, query: str) -> pd.DataFrame:
        """
        Simulate query execution.
        
        Args:
            query: SQL query string
            
        Returns:
            pd.DataFrame: Mock query result
        """
        self.queries_executed.append(query)
        return pd.DataFrame({'result': [1, 2, 3]})
    
    def close(self):
        """Simulate closing connection."""
        self.connected = False


@pytest.fixture
def mock_db_connection():
    """
    Fixture providing mock database connection.
    
    Returns:
        MockDatabaseConnection: Mock connection object
    """
    return MockDatabaseConnection()


def assert_dataframe_equal(df1: pd.DataFrame, df2: pd.DataFrame, **kwargs):
    """
    Enhanced DataFrame equality assertion with better error messages.
    
    Args:
        df1: First DataFrame
        df2: Second DataFrame
        **kwargs: Additional arguments passed to pd.testing.assert_frame_equal
    """
    try:
        pd.testing.assert_frame_equal(df1, df2, **kwargs)
    except AssertionError as e:
        print(f"\nDataFrame comparison failed:")
        print(f"Shape df1: {df1.shape}, Shape df2: {df2.shape}")
        print(f"Columns df1: {list(df1.columns)}")
        print(f"Columns df2: {list(df2.columns)}")
        raise e


def create_test_csv(path: Path, df: pd.DataFrame):
    """
    Helper to create test CSV file.
    
    Args:
        path: File path
        df: DataFrame to save
    """
    df.to_csv(path, index=False)
    return path
