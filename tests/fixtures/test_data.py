"""
Test fixtures and sample data for testing.

This module provides reusable test data that can be loaded
for various test scenarios.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_customer_data(n_rows=1000, seed=42):
    """
    Generate synthetic customer data for testing.
    
    Args:
        n_rows: Number of rows to generate
        seed: Random seed for reproducibility
        
    Returns:
        pd.DataFrame: Customer data
    """
    np.random.seed(seed)
    
    return pd.DataFrame({
        'customer_id': range(1, n_rows + 1),
        'age': np.random.randint(18, 80, n_rows),
        'income': np.random.uniform(20000, 200000, n_rows),
        'credit_score': np.random.randint(300, 850, n_rows),
        'account_balance': np.random.uniform(-1000, 50000, n_rows),
        'transaction_count': np.random.randint(0, 100, n_rows),
        'is_active': np.random.choice([True, False], n_rows, p=[0.8, 0.2]),
        'region': np.random.choice(['North', 'South', 'East', 'West'], n_rows),
        'signup_date': [
            datetime.now() - timedelta(days=np.random.randint(1, 365))
            for _ in range(n_rows)
        ],
        'last_transaction': [
            datetime.now() - timedelta(days=np.random.randint(0, 90))
            for _ in range(n_rows)
        ]
    })


def generate_transaction_data(n_rows=5000, seed=42):
    """
    Generate synthetic transaction data for testing.
    
    Args:
        n_rows: Number of rows to generate
        seed: Random seed for reproducibility
        
    Returns:
        pd.DataFrame: Transaction data
    """
    np.random.seed(seed)
    
    return pd.DataFrame({
        'transaction_id': range(1, n_rows + 1),
        'customer_id': np.random.randint(1, 1000, n_rows),
        'amount': np.random.uniform(10, 5000, n_rows),
        'category': np.random.choice(
            ['Groceries', 'Dining', 'Travel', 'Shopping', 'Bills'],
            n_rows
        ),
        'merchant': [f"Merchant_{i % 100}" for i in range(n_rows)],
        'timestamp': [
            datetime.now() - timedelta(hours=np.random.randint(0, 720))
            for _ in range(n_rows)
        ],
        'is_fraud': np.random.choice([True, False], n_rows, p=[0.02, 0.98])
    })


def generate_time_series_data(n_points=1000, seed=42):
    """
    Generate synthetic time series data for testing.
    
    Args:
        n_points: Number of time points
        seed: Random seed for reproducibility
        
    Returns:
        pd.DataFrame: Time series data
    """
    np.random.seed(seed)
    
    dates = pd.date_range(start='2024-01-01', periods=n_points, freq='H')
    trend = np.linspace(100, 200, n_points)
    seasonality = 20 * np.sin(np.arange(n_points) * 2 * np.pi / 24)
    noise = np.random.normal(0, 5, n_rows)
    
    return pd.DataFrame({
        'timestamp': dates,
        'value': trend + seasonality + noise,
        'metric_type': np.random.choice(['A', 'B', 'C'], n_points)
    })


def generate_corrupted_data(n_rows=100, corruption_rate=0.3, seed=42):
    """
    Generate data with intentional quality issues for testing validation.
    
    Args:
        n_rows: Number of rows
        corruption_rate: Fraction of rows to corrupt
        seed: Random seed
        
    Returns:
        pd.DataFrame: Data with quality issues
    """
    np.random.seed(seed)
    
    df = generate_customer_data(n_rows, seed)
    
    # Introduce nulls
    null_indices = np.random.choice(n_rows, int(n_rows * corruption_rate), replace=False)
    df.loc[null_indices, 'age'] = None
    
    # Introduce out-of-range values
    df.loc[null_indices[:len(null_indices)//2], 'credit_score'] = -1
    
    # Introduce duplicates
    df = pd.concat([df, df.iloc[:10]], ignore_index=True)
    
    return df


# Sample configurations for testing
SAMPLE_CONFIGS = {
    'basic': {
        'data_source': {'type': 'csv'},
        'feature_engineering': {
            'numerical_features': ['age', 'income'],
            'categorical_features': ['region']
        }
    },
    'advanced': {
        'data_source': {'type': 'postgresql'},
        'feature_engineering': {
            'numerical_features': ['age', 'income', 'credit_score'],
            'categorical_features': ['region', 'is_active'],
            'scaling_method': 'standard',
            'interaction_features': True
        },
        'model': {
            'type': 'random_forest',
            'hyperparameters': {'n_estimators': 100}
        }
    }
}


# Sample validation rules
SAMPLE_VALIDATION_RULES = {
    'customer_data': {
        'required_columns': ['customer_id', 'age', 'income'],
        'constraints': {
            'age': {'min': 18, 'max': 120},
            'credit_score': {'min': 300, 'max': 850}
        },
        'unique_columns': ['customer_id']
    }
}
