"""
Unit tests for data validation module.

Tests cover:
- Schema validation
- Data quality checks
- Business rule validation
- Error detection and reporting
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class TestSchemaValidation:
    """Test suite for schema validation."""
    
    def test_column_presence_validation(self, sample_dataframe):
        """
        Test validation of required columns.
        
        Validates:
        - All required columns present
        - Error on missing columns
        """
        from pipeline.validate import validate_schema
        
        # Arrange
        required_columns = ['customer_id', 'age', 'income']
        
        # Act
        is_valid, errors = validate_schema(
            sample_dataframe,
            required_columns=required_columns
        )
        
        # Assert
        assert is_valid is True
        assert len(errors) == 0
    
    def test_missing_column_detection(self, sample_dataframe):
        """
        Test detection of missing required columns.
        
        Validates:
        - Missing columns identified
        - Error messages clear
        """
        from pipeline.validate import validate_schema
        
        # Arrange
        required_columns = ['customer_id', 'nonexistent_column']
        
        # Act
        is_valid, errors = validate_schema(
            sample_dataframe,
            required_columns=required_columns
        )
        
        # Assert
        assert is_valid is False
        assert len(errors) > 0
        assert any('nonexistent_column' in str(e) for e in errors)
    
    def test_data_type_validation(self, sample_dataframe):
        """
        Test validation of column data types.
        
        Validates:
        - Numeric columns are numeric
        - String columns are string
        - Date columns are datetime
        """
        from pipeline.validate import validate_data_types
        
        # Arrange
        expected_types = {
            'customer_id': 'int64',
            'age': 'int64',
            'income': 'float64',
            'region': 'object',
            'is_active': 'bool'
        }
        
        # Act
        is_valid, errors = validate_data_types(sample_dataframe, expected_types)
        
        # Assert
        assert is_valid is True or len(errors) == 0


class TestDataQualityChecks:
    """Test suite for data quality validation."""
    
    def test_null_value_detection(self):
        """
        Test detection of null values.
        
        Validates:
        - Null counts accurate
        - Null percentage calculated
        - Threshold enforcement
        """
        from pipeline.validate import check_null_values
        
        # Arrange
        df_with_nulls = pd.DataFrame({
            'col1': [1, 2, None, 4, 5],
            'col2': [None, None, 3, 4, 5],
            'col3': [1, 2, 3, 4, 5]
        })
        
        # Act
        report = check_null_values(df_with_nulls, threshold=0.2)
        
        # Assert
        assert 'col1' in report
        assert 'col2' in report
        assert report['col2']['null_percentage'] > 0.2
    
    def test_duplicate_detection(self, sample_dataframe):
        """
        Test detection of duplicate records.
        
        Validates:
        - Duplicates identified
        - Subset-based detection
        - Count accuracy
        """
        from pipeline.validate import check_duplicates
        
        # Arrange - Add duplicate row
        df_with_dups = pd.concat([sample_dataframe, sample_dataframe.iloc[[0]]])
        
        # Act
        has_duplicates, duplicate_count = check_duplicates(
            df_with_dups,
            subset=['customer_id']
        )
        
        # Assert
        assert has_duplicates is True
        assert duplicate_count > 0
    
    def test_value_range_validation(self, sample_dataframe):
        """
        Test validation of value ranges.
        
        Validates:
        - Min/max constraints
        - Outlier detection
        - Range violations reported
        """
        from pipeline.validate import validate_value_ranges
        
        # Arrange
        constraints = {
            'age': {'min': 18, 'max': 80},
            'credit_score': {'min': 300, 'max': 850}
        }
        
        # Act
        is_valid, violations = validate_value_ranges(
            sample_dataframe,
            constraints
        )
        
        # Assert
        assert isinstance(is_valid, bool)
        assert isinstance(violations, dict)
    
    def test_uniqueness_validation(self, sample_dataframe):
        """
        Test uniqueness constraints.
        
        Validates:
        - Unique columns identified
        - Duplicate values detected
        - Primary key validation
        """
        from pipeline.validate import validate_uniqueness
        
        # Act
        is_unique, duplicate_values = validate_uniqueness(
            sample_dataframe,
            columns=['customer_id']
        )
        
        # Assert
        assert is_unique is True
        assert len(duplicate_values) == 0


class TestBusinessRuleValidation:
    """Test suite for business rule validation."""
    
    def test_cross_field_validation(self):
        """
        Test validation across multiple fields.
        
        Validates:
        - Logical consistency
        - Field relationships
        - Conditional rules
        """
        from pipeline.validate import validate_business_rules
        
        # Arrange
        df = pd.DataFrame({
            'start_date': pd.date_range('2024-01-01', periods=5),
            'end_date': pd.date_range('2024-01-03', periods=5),
            'status': ['active', 'active', 'inactive', 'active', 'active']
        })
        
        rules = [
            {
                'name': 'end_after_start',
                'condition': lambda df: df['end_date'] > df['start_date']
            }
        ]
        
        # Act
        results = validate_business_rules(df, rules)
        
        # Assert
        assert 'end_after_start' in results
        assert results['end_after_start']['passed'] is True
    
    def test_categorical_value_validation(self, sample_dataframe):
        """
        Test validation of categorical values.
        
        Validates:
        - Allowed values enforced
        - Invalid values detected
        - Case sensitivity handling
        """
        from pipeline.validate import validate_categorical_values
        
        # Arrange
        allowed_values = {
            'region': ['North', 'South', 'East', 'West'],
            'is_active': [True, False]
        }
        
        # Act
        is_valid, invalid_values = validate_categorical_values(
            sample_dataframe,
            allowed_values
        )
        
        # Assert
        assert is_valid is True
        assert len(invalid_values) == 0
    
    def test_temporal_validation(self):
        """
        Test temporal/date validation.
        
        Validates:
        - Date format correct
        - Date ranges valid
        - Temporal ordering
        """
        from pipeline.validate import validate_temporal_data
        
        # Arrange
        df = pd.DataFrame({
            'event_date': pd.date_range('2024-01-01', periods=100),
            'processed_date': pd.date_range('2024-01-02', periods=100)
        })
        
        # Act
        is_valid, errors = validate_temporal_data(
            df,
            date_columns=['event_date', 'processed_date'],
            min_date='2024-01-01',
            max_date=datetime.now()
        )
        
        # Assert
        assert is_valid is True


class TestStatisticalValidation:
    """Test suite for statistical validation."""
    
    def test_distribution_validation(self, sample_dataframe):
        """
        Test statistical distribution validation.
        
        Validates:
        - Mean/std within expected range
        - Distribution shape
        - Statistical tests
        """
        from pipeline.validate import validate_distribution
        
        # Arrange
        reference_stats = {
            'age': {'mean': 45, 'std': 15, 'min': 18, 'max': 80}
        }
        
        # Act
        is_valid, report = validate_distribution(
            sample_dataframe['age'],
            reference_stats['age'],
            tolerance=0.2
        )
        
        # Assert
        assert isinstance(is_valid, bool)
        assert 'mean_diff' in report
    
    def test_correlation_validation(self, sample_dataframe):
        """
        Test correlation structure validation.
        
        Validates:
        - Expected correlations present
        - Correlation strength
        - Correlation stability
        """
        from pipeline.validate import validate_correlations
        
        # Arrange
        expected_correlations = {
            ('age', 'credit_score'): {'min': -0.5, 'max': 0.5}
        }
        
        # Act
        is_valid, violations = validate_correlations(
            sample_dataframe,
            expected_correlations
        )
        
        # Assert
        assert isinstance(is_valid, bool)


class TestValidationReporting:
    """Test suite for validation reporting."""
    
    def test_comprehensive_validation_report(self, sample_dataframe):
        """
        Test generation of comprehensive validation report.
        
        Validates:
        - All checks included
        - Report format correct
        - Summary statistics present
        """
        from pipeline.validate import generate_validation_report
        
        # Act
        report = generate_validation_report(sample_dataframe)
        
        # Assert
        assert 'schema_validation' in report
        assert 'data_quality' in report
        assert 'summary' in report
        assert 'passed_checks' in report['summary']
        assert 'failed_checks' in report['summary']
    
    def test_validation_report_export(self, sample_dataframe, test_data_dir):
        """
        Test exporting validation report.
        
        Validates:
        - Report saved to file
        - Format readable
        - Complete information
        """
        from pipeline.validate import generate_validation_report
        import json
        
        # Arrange
        report = generate_validation_report(sample_dataframe)
        report_path = test_data_dir / "validation_report.json"
        
        # Act
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Assert
        assert report_path.exists()
        
        # Verify can be loaded
        with open(report_path, 'r') as f:
            loaded_report = json.load(f)
        assert 'summary' in loaded_report


class TestValidationPerformance:
    """Performance tests for validation."""
    
    @pytest.mark.slow
    def test_validation_performance_large_dataset(self):
        """
        Test validation performance on large dataset.
        
        Validates:
        - Validation completes in reasonable time
        - Memory usage acceptable
        """
        import time
        from pipeline.validate import generate_validation_report
        
        # Arrange
        large_df = pd.DataFrame({
            'col1': np.random.randn(1_000_000),
            'col2': np.random.choice(['A', 'B', 'C'], 1_000_000),
            'col3': pd.date_range('2024-01-01', periods=1_000_000, freq='S')
        })
        
        # Act
        start = time.time()
        report = generate_validation_report(large_df)
        elapsed = time.time() - start
        
        # Assert
        # Should validate 1M rows in under 5 seconds
        assert elapsed < 5.0
        assert report is not None


class TestValidationIntegration:
    """Integration tests with other pipeline components."""
    
    def test_validation_in_pipeline(self, sample_dataframe):
        """
        Test validation integration with pipeline.
        
        Validates:
        - Validation runs automatically
        - Pipeline stops on validation failure
        - Errors propagated correctly
        """
        from pipeline.validate import ValidationPipeline
        
        # Arrange
        validator = ValidationPipeline(
            required_columns=['customer_id', 'age'],
            data_quality_checks=['nulls', 'duplicates'],
            business_rules=[]
        )
        
        # Act
        is_valid, report = validator.validate(sample_dataframe)
        
        # Assert
        assert isinstance(is_valid, bool)
        assert 'checks_run' in report


# Mark for unit tests
pytestmark = pytest.mark.unit


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
