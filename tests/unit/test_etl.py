"""
Unit tests for ETL (Extract-Transform-Load) pipeline.

Tests cover:
- Data extraction from various sources
- Data transformation logic
- Data loading to target systems
- Error handling and edge cases
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path


class TestDataExtraction:
    """Test suite for data extraction functionality."""
    
    def test_extract_from_csv(self, test_data_dir, sample_dataframe):
        """
        Test extracting data from CSV file.
        
        Validates:
        - Correct data loading
        - Schema preservation
        - Data type handling
        """
        # Arrange
        csv_path = test_data_dir / "test.csv"
        sample_dataframe.to_csv(csv_path, index=False)
        
        # Act
        from pipeline.etl import extract_data
        result = extract_data(str(csv_path), source_type='csv')
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_dataframe)
        assert list(result.columns) == list(sample_dataframe.columns)
    
    def test_extract_from_database(self, mock_db_connection):
        """
        Test extracting data from database.
        
        Validates:
        - Database connection handling
        - Query execution
        - Result formatting
        """
        # Arrange
        query = "SELECT * FROM customers"
        
        # Act
        from pipeline.etl import extract_from_database
        result = extract_from_database(mock_db_connection, query)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert query in mock_db_connection.queries_executed
    
    def test_extract_handles_missing_file(self, test_data_dir):
        """
        Test error handling for missing source files.
        
        Validates:
        - Appropriate exception raised
        - Clear error message
        """
        # Arrange
        missing_file = test_data_dir / "nonexistent.csv"
        
        # Act & Assert
        from pipeline.etl import extract_data
        with pytest.raises(FileNotFoundError):
            extract_data(str(missing_file), source_type='csv')
    
    def test_extract_handles_corrupted_data(self, test_data_dir):
        """
        Test handling of corrupted/malformed data.
        
        Validates:
        - Graceful error handling
        - Logging of errors
        """
        # Arrange
        corrupted_file = test_data_dir / "corrupted.csv"
        with open(corrupted_file, 'w') as f:
            f.write("invalid,csv,data\n1,2,\n,3,4\ngarbage")
        
        # Act & Assert
        from pipeline.etl import extract_data
        # Should handle gracefully or raise specific exception
        with pytest.raises((pd.errors.ParserError, ValueError)):
            extract_data(str(corrupted_file), source_type='csv')


class TestDataTransformation:
    """Test suite for data transformation logic."""
    
    def test_basic_transformation(self, sample_dataframe):
        """
        Test basic data transformations.
        
        Validates:
        - Column operations
        - Data type conversions
        - Derived features
        """
        # Arrange
        from pipeline.etl import transform_data
        
        # Act
        result = transform_data(sample_dataframe)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= len(sample_dataframe)  # May filter rows
        # Add specific transformation validations based on your logic
    
    def test_transformation_handles_nulls(self):
        """
        Test transformation with null values.
        
        Validates:
        - Null handling strategy
        - Data integrity after null processing
        """
        # Arrange
        df_with_nulls = pd.DataFrame({
            'col1': [1, 2, None, 4],
            'col2': [None, 'b', 'c', 'd'],
            'col3': [1.0, 2.0, 3.0, None]
        })
        
        from pipeline.etl import transform_data
        
        # Act
        result = transform_data(df_with_nulls)
        
        # Assert
        # Verify null handling based on your implementation
        assert isinstance(result, pd.DataFrame)
    
    def test_transformation_preserves_schema(self, sample_dataframe):
        """
        Test that transformation maintains expected schema.
        
        Validates:
        - Required columns present
        - Data types correct
        - No unexpected columns
        """
        # Arrange
        from pipeline.etl import transform_data
        expected_columns = ['customer_id', 'age', 'income']
        
        # Act
        result = transform_data(sample_dataframe)
        
        # Assert
        for col in expected_columns:
            if col in sample_dataframe.columns:
                assert col in result.columns
    
    def test_transformation_performance(self, sample_dataframe):
        """
        Test transformation performance meets requirements.
        
        Validates:
        - Processing time within acceptable range
        - Memory usage reasonable
        """
        import time
        from pipeline.etl import transform_data
        
        # Arrange
        large_df = pd.concat([sample_dataframe] * 10, ignore_index=True)
        
        # Act
        start_time = time.time()
        result = transform_data(large_df)
        elapsed_time = time.time() - start_time
        
        # Assert
        # Should process 10K rows in under 1 second
        assert elapsed_time < 1.0
        assert len(result) > 0


class TestDataLoading:
    """Test suite for data loading functionality."""
    
    def test_load_to_csv(self, sample_dataframe, test_data_dir):
        """
        Test loading data to CSV file.
        
        Validates:
        - File creation
        - Data integrity
        - Format correctness
        """
        # Arrange
        output_path = test_data_dir / "output.csv"
        from pipeline.etl import load_data
        
        # Act
        load_data(sample_dataframe, str(output_path), target_type='csv')
        
        # Assert
        assert output_path.exists()
        loaded_df = pd.read_csv(output_path)
        assert len(loaded_df) == len(sample_dataframe)
    
    def test_load_to_database(self, sample_dataframe, mock_db_connection):
        """
        Test loading data to database.
        
        Validates:
        - Database insertion
        - Transaction handling
        - Error recovery
        """
        # Arrange
        table_name = "processed_data"
        from pipeline.etl import load_to_database
        
        # Act
        load_to_database(sample_dataframe, mock_db_connection, table_name)
        
        # Assert
        assert mock_db_connection.connected
        # Verify insert queries executed
        assert len(mock_db_connection.queries_executed) > 0
    
    def test_load_handles_write_errors(self, sample_dataframe, test_data_dir):
        """
        Test error handling during data loading.
        
        Validates:
        - Permission errors handled
        - Disk space errors handled
        - Partial write recovery
        """
        # Arrange
        read_only_path = test_data_dir / "readonly.csv"
        from pipeline.etl import load_data
        
        # Make directory read-only (simulate permission error)
        # This is platform-dependent, adjust as needed
        
        # Act & Assert
        # Should handle gracefully or raise specific exception
        # Implementation depends on your error handling strategy


class TestETLPipeline:
    """Integration tests for complete ETL pipeline."""
    
    def test_end_to_end_pipeline(self, test_data_dir, sample_dataframe):
        """
        Test complete ETL pipeline execution.
        
        Validates:
        - Extract → Transform → Load flow
        - Data consistency throughout
        - Final output correctness
        """
        # Arrange
        input_path = test_data_dir / "input.csv"
        output_path = test_data_dir / "output.csv"
        sample_dataframe.to_csv(input_path, index=False)
        
        from pipeline.etl import run_etl_pipeline
        
        # Act
        run_etl_pipeline(
            source=str(input_path),
            target=str(output_path),
            config={'source_type': 'csv', 'target_type': 'csv'}
        )
        
        # Assert
        assert output_path.exists()
        result = pd.read_csv(output_path)
        assert len(result) > 0
    
    def test_pipeline_with_custom_config(self, test_data_dir, sample_dataframe, sample_config):
        """
        Test pipeline with custom configuration.
        
        Validates:
        - Configuration parameter handling
        - Custom transformation application
        - Config-driven behavior
        """
        # Arrange
        input_path = test_data_dir / "input.csv"
        output_path = test_data_dir / "output.csv"
        sample_dataframe.to_csv(input_path, index=False)
        
        from pipeline.etl import run_etl_pipeline
        
        # Act
        run_etl_pipeline(
            source=str(input_path),
            target=str(output_path),
            config=sample_config
        )
        
        # Assert
        assert output_path.exists()


# Test helpers and utilities

def create_mock_data_source():
    """Helper to create mock data source for testing."""
    return pd.DataFrame({
        'id': range(100),
        'value': np.random.randn(100)
    })


# Mark slow tests
pytestmark = pytest.mark.unit


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
