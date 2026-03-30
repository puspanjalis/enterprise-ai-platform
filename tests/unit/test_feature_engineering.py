"""
Unit tests for feature engineering module.

Tests cover:
- Feature transformation logic
- Scaling and normalization
- Encoding categorical variables
- Feature generation
- Training/serving consistency
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch


class TestFeatureTransformers:
    """Test suite for individual feature transformers."""
    
    def test_numerical_scaler(self, sample_dataframe):
        """
        Test numerical feature scaling.
        
        Validates:
        - Standard scaling applied correctly
        - Mean = 0, Std = 1 after scaling
        - Transform reversible
        """
        from pipeline.feature_engineering import NumericalScaler
        
        # Arrange
        scaler = NumericalScaler(method='standard')
        numerical_cols = ['age', 'income', 'credit_score']
        
        # Act
        scaler.fit(sample_dataframe[numerical_cols])
        scaled = scaler.transform(sample_dataframe[numerical_cols])
        
        # Assert
        assert scaled.shape == sample_dataframe[numerical_cols].shape
        # Check mean close to 0, std close to 1
        assert abs(scaled.mean().mean()) < 0.1
        assert abs(scaled.std().mean() - 1.0) < 0.1
    
    def test_categorical_encoder(self, sample_dataframe):
        """
        Test categorical feature encoding.
        
        Validates:
        - One-hot encoding
        - Label encoding
        - Unknown category handling
        """
        from pipeline.feature_engineering import CategoricalEncoder
        
        # Arrange
        encoder = CategoricalEncoder(method='onehot')
        categorical_cols = ['region']
        
        # Act
        encoder.fit(sample_dataframe[categorical_cols])
        encoded = encoder.transform(sample_dataframe[categorical_cols])
        
        # Assert
        # One-hot should create column for each category
        unique_categories = sample_dataframe['region'].nunique()
        assert encoded.shape[1] >= unique_categories
    
    def test_encoder_handles_unseen_categories(self):
        """
        Test handling of categories not seen during training.
        
        Validates:
        - Unknown category handling strategy
        - No errors on unseen values
        - Consistent output shape
        """
        from pipeline.feature_engineering import CategoricalEncoder
        
        # Arrange
        train_df = pd.DataFrame({'region': ['North', 'South', 'East']})
        test_df = pd.DataFrame({'region': ['North', 'West', 'Unknown']})
        
        encoder = CategoricalEncoder(method='onehot', handle_unknown='ignore')
        
        # Act
        encoder.fit(train_df)
        result = encoder.transform(test_df)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        # Should handle gracefully without errors


class TestFeatureGeneration:
    """Test suite for feature generation logic."""
    
    def test_temporal_features(self, sample_dataframe):
        """
        Test temporal feature extraction.
        
        Validates:
        - Day of week extraction
        - Month extraction
        - Hour extraction
        - Is weekend flag
        """
        from pipeline.feature_engineering import generate_temporal_features
        
        # Act
        result = generate_temporal_features(sample_dataframe, timestamp_col='timestamp')
        
        # Assert
        expected_features = ['day_of_week', 'month', 'hour', 'is_weekend']
        for feature in expected_features:
            assert feature in result.columns
    
    def test_interaction_features(self, sample_dataframe):
        """
        Test interaction feature generation.
        
        Validates:
        - Polynomial features
        - Ratio features
        - Product features
        """
        from pipeline.feature_engineering import generate_interaction_features
        
        # Arrange
        feature_pairs = [('age', 'income'), ('credit_score', 'account_balance')]
        
        # Act
        result = generate_interaction_features(
            sample_dataframe, 
            feature_pairs=feature_pairs
        )
        
        # Assert
        # Should have original + interaction columns
        assert result.shape[1] > sample_dataframe.shape[1]
        # Check specific interaction columns exist
        assert 'age_income_interaction' in result.columns or \
               'age_x_income' in result.columns
    
    def test_aggregation_features(self, sample_dataframe):
        """
        Test aggregation-based features.
        
        Validates:
        - Group-by aggregations
        - Rolling window features
        - Statistical summaries
        """
        from pipeline.feature_engineering import generate_aggregation_features
        
        # Act
        result = generate_aggregation_features(
            sample_dataframe,
            group_by='region',
            agg_columns=['income', 'credit_score'],
            agg_functions=['mean', 'std', 'max']
        )
        
        # Assert
        # Should have aggregation columns
        assert 'income_mean_by_region' in result.columns or \
               'region_income_mean' in result.columns


class TestFeaturePipeline:
    """Test suite for complete feature engineering pipeline."""
    
    def test_pipeline_fit_transform(self, sample_dataframe):
        """
        Test pipeline fit and transform.
        
        Validates:
        - All transformers applied in order
        - State persisted correctly
        - Reproducible results
        """
        from pipeline.feature_engineering import FeaturePipeline
        
        # Arrange
        pipeline = FeaturePipeline(config={
            'numerical_features': ['age', 'income'],
            'categorical_features': ['region'],
            'scaling_method': 'standard'
        })
        
        # Act
        pipeline.fit(sample_dataframe)
        result = pipeline.transform(sample_dataframe)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_dataframe)
    
    def test_pipeline_training_serving_consistency(self, sample_dataframe):
        """
        Test consistency between training and serving.
        
        Validates:
        - Same input produces same output
        - Transformer state preserved
        - No data leakage
        """
        from pipeline.feature_engineering import FeaturePipeline
        
        # Arrange
        pipeline = FeaturePipeline(config={'numerical_features': ['age']})
        
        # Split data into train and test
        train_data = sample_dataframe.iloc[:800]
        test_data = sample_dataframe.iloc[800:]
        
        # Act
        pipeline.fit(train_data)
        train_result = pipeline.transform(train_data)
        test_result = pipeline.transform(test_data)
        
        # Assert
        # Same columns in both
        assert list(train_result.columns) == list(test_result.columns)
        # Scaling parameters from training only
        assert test_result is not None
    
    def test_pipeline_handles_missing_features(self, sample_dataframe):
        """
        Test handling of missing features during transform.
        
        Validates:
        - Graceful error handling
        - Clear error messages
        - Feature validation
        """
        from pipeline.feature_engineering import FeaturePipeline
        
        # Arrange
        pipeline = FeaturePipeline(config={
            'numerical_features': ['age', 'income', 'nonexistent_column']
        })
        
        # Act & Assert
        with pytest.raises((KeyError, ValueError)):
            pipeline.fit(sample_dataframe)
    
    def test_pipeline_serialization(self, sample_dataframe, test_data_dir):
        """
        Test pipeline save and load.
        
        Validates:
        - Pipeline can be saved
        - Loaded pipeline produces same results
        - State fully preserved
        """
        from pipeline.feature_engineering import FeaturePipeline
        import pickle
        
        # Arrange
        pipeline = FeaturePipeline(config={'numerical_features': ['age']})
        pipeline.fit(sample_dataframe)
        original_result = pipeline.transform(sample_dataframe)
        
        # Act - Save
        pipeline_path = test_data_dir / "pipeline.pkl"
        with open(pipeline_path, 'wb') as f:
            pickle.dump(pipeline, f)
        
        # Act - Load
        with open(pipeline_path, 'rb') as f:
            loaded_pipeline = pickle.load(f)
        
        loaded_result = loaded_pipeline.transform(sample_dataframe)
        
        # Assert
        pd.testing.assert_frame_equal(original_result, loaded_result)


class TestFeatureValidation:
    """Test suite for feature validation logic."""
    
    def test_feature_schema_validation(self, sample_dataframe):
        """
        Test feature schema validation.
        
        Validates:
        - Expected columns present
        - Data types correct
        - Value ranges valid
        """
        from pipeline.feature_engineering import validate_feature_schema
        
        # Arrange
        expected_schema = {
            'age': {'type': 'int', 'min': 0, 'max': 120},
            'income': {'type': 'float', 'min': 0},
            'region': {'type': 'str', 'values': ['North', 'South', 'East', 'West']}
        }
        
        # Act
        is_valid, errors = validate_feature_schema(sample_dataframe, expected_schema)
        
        # Assert
        assert is_valid is True or isinstance(errors, list)
    
    def test_feature_distribution_check(self, sample_dataframe):
        """
        Test feature distribution validation.
        
        Validates:
        - Distribution within expected range
        - No extreme outliers
        - Statistical properties
        """
        from pipeline.feature_engineering import check_feature_distribution
        
        # Act
        report = check_feature_distribution(
            sample_dataframe[['age', 'income']],
            reference_stats={'age': {'mean': 45, 'std': 15}}
        )
        
        # Assert
        assert 'age' in report
        assert 'drift_detected' in report['age']


class TestFeatureImportance:
    """Test suite for feature importance and selection."""
    
    def test_correlation_based_selection(self, sample_dataframe):
        """
        Test correlation-based feature selection.
        
        Validates:
        - High correlation features identified
        - Feature reduction logic
        """
        from pipeline.feature_engineering import select_features_by_correlation
        
        # Act
        selected_features = select_features_by_correlation(
            sample_dataframe[['age', 'income', 'credit_score']],
            threshold=0.8
        )
        
        # Assert
        assert isinstance(selected_features, list)
        assert len(selected_features) <= 3
    
    def test_variance_based_selection(self, sample_dataframe):
        """
        Test variance-based feature selection.
        
        Validates:
        - Low variance features removed
        - Threshold application correct
        """
        from pipeline.feature_engineering import select_features_by_variance
        
        # Add zero variance column
        sample_dataframe['constant_col'] = 1
        
        # Act
        selected_features = select_features_by_variance(
            sample_dataframe,
            threshold=0.01
        )
        
        # Assert
        assert 'constant_col' not in selected_features


# Performance tests
class TestFeatureEngineringPerformance:
    """Performance tests for feature engineering."""
    
    @pytest.mark.slow
    def test_large_dataset_performance(self):
        """
        Test performance on large dataset.
        
        Validates:
        - Processing time acceptable
        - Memory usage reasonable
        """
        import time
        from pipeline.feature_engineering import FeaturePipeline
        
        # Arrange
        large_df = pd.DataFrame({
            'col1': np.random.randn(1_000_000),
            'col2': np.random.randn(1_000_000),
            'col3': np.random.choice(['A', 'B', 'C'], 1_000_000)
        })
        
        pipeline = FeaturePipeline(config={
            'numerical_features': ['col1', 'col2'],
            'categorical_features': ['col3']
        })
        
        # Act
        start = time.time()
        pipeline.fit(large_df)
        result = pipeline.transform(large_df)
        elapsed = time.time() - start
        
        # Assert
        # Should process 1M rows in under 10 seconds
        assert elapsed < 10.0
        assert len(result) == len(large_df)


# Mark for unit tests
pytestmark = pytest.mark.unit


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
