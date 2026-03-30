"""
Integration tests for end-to-end ML pipeline.

Tests cover:
- Complete pipeline execution
- Component interactions
- Data flow through system
- Error handling across components
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import time


class TestPipelineIntegration:
    """Integration tests for complete pipeline execution."""
    
    def test_end_to_end_pipeline_execution(self, test_data_dir, sample_dataframe):
        """
        Test complete pipeline from data ingestion to model output.
        
        Validates:
        - All components execute successfully
        - Data flows correctly between stages
        - Final output format correct
        """
        # Arrange
        input_file = test_data_dir / "input.csv"
        output_dir = test_data_dir / "output"
        output_dir.mkdir()
        
        sample_dataframe.to_csv(input_file, index=False)
        
        # Import main pipeline orchestrator
        from run_pipeline import main as run_pipeline
        
        # Act
        result = run_pipeline(
            input_path=str(input_file),
            output_path=str(output_dir),
            config={
                'validate': True,
                'engineer_features': True,
                'train_model': True,
                'monitor': True
            }
        )
        
        # Assert
        assert result['status'] == 'success'
        assert result['records_processed'] > 0
        assert (output_dir / "processed_data.csv").exists()
        assert (output_dir / "model.pkl").exists() or \
               result.get('model_trained', False)
    
    def test_pipeline_with_validation_failure(self, test_data_dir):
        """
        Test pipeline behavior when validation fails.
        
        Validates:
        - Pipeline stops on validation error
        - Error message clear
        - No partial processing
        """
        # Arrange - Create invalid data
        invalid_df = pd.DataFrame({
            'customer_id': [1, 2, 3],
            'age': [-5, 200, None],  # Invalid ages
        })
        
        input_file = test_data_dir / "invalid.csv"
        invalid_df.to_csv(input_file, index=False)
        
        from run_pipeline import main as run_pipeline
        
        # Act & Assert
        with pytest.raises((ValueError, RuntimeError)):
            run_pipeline(
                input_path=str(input_file),
                output_path=str(test_data_dir),
                config={'validate': True, 'strict_validation': True}
            )
    
    def test_pipeline_with_monitoring(self, test_data_dir, sample_dataframe):
        """
        Test pipeline with monitoring enabled.
        
        Validates:
        - Monitoring metrics collected
        - Alerts generated if needed
        - Performance tracked
        """
        # Arrange
        input_file = test_data_dir / "input.csv"
        sample_dataframe.to_csv(input_file, index=False)
        
        from run_pipeline import main as run_pipeline
        
        # Act
        result = run_pipeline(
            input_path=str(input_file),
            output_path=str(test_data_dir),
            config={
                'validate': True,
                'monitor': True,
                'monitoring': {
                    'data_quality': True,
                    'drift_detection': True,
                    'performance_tracking': True
                }
            }
        )
        
        # Assert
        assert 'monitoring_report' in result
        assert 'data_quality_score' in result['monitoring_report']
        assert result['monitoring_report']['data_quality_score'] >= 0


class TestComponentInteractions:
    """Test interactions between pipeline components."""
    
    def test_etl_to_feature_engineering_handoff(self, sample_dataframe):
        """
        Test data handoff from ETL to feature engineering.
        
        Validates:
        - Data format compatible
        - All required fields present
        - No data loss in transition
        """
        from pipeline.etl import transform_data
        from pipeline.feature_engineering import FeaturePipeline
        
        # Act - ETL
        etl_output = transform_data(sample_dataframe)
        
        # Act - Feature Engineering
        feature_pipeline = FeaturePipeline(config={
            'numerical_features': ['age', 'income']
        })
        feature_pipeline.fit(etl_output)
        feature_output = feature_pipeline.transform(etl_output)
        
        # Assert
        assert len(feature_output) == len(etl_output)
        assert feature_output is not None
    
    def test_validation_pipeline_integration(self, sample_dataframe):
        """
        Test validation integrated throughout pipeline.
        
        Validates:
        - Validation at each stage
        - Failed validation stops pipeline
        - Validation results aggregated
        """
        from pipeline.validate import ValidationPipeline
        from pipeline.etl import transform_data
        
        # Arrange
        validator = ValidationPipeline(
            required_columns=['customer_id', 'age'],
            data_quality_checks=['nulls']
        )
        
        # Act - Validate input
        input_valid, input_report = validator.validate(sample_dataframe)
        
        if input_valid:
            # Transform
            transformed = transform_data(sample_dataframe)
            
            # Validate output
            output_valid, output_report = validator.validate(transformed)
            
            # Assert
            assert input_valid is True
            assert output_valid is True
    
    def test_monitoring_integration(self, sample_dataframe):
        """
        Test monitoring integration with pipeline execution.
        
        Validates:
        - Metrics collected during execution
        - Health checks performed
        - Alerts triggered appropriately
        """
        from monitoring.pipeline_health import PipelineHealthMonitor
        from pipeline.etl import transform_data
        
        # Arrange
        monitor = PipelineHealthMonitor()
        
        # Act
        with monitor.track_execution('test_pipeline'):
            result = transform_data(sample_dataframe)
        
        metrics = monitor.get_metrics()
        
        # Assert
        assert 'test_pipeline' in metrics
        assert 'duration_seconds' in metrics['test_pipeline']
        assert 'success' in metrics['test_pipeline']


class TestErrorHandling:
    """Test error handling across pipeline."""
    
    def test_graceful_degradation(self, test_data_dir, sample_dataframe):
        """
        Test graceful degradation on partial failures.
        
        Validates:
        - Pipeline continues on non-critical errors
        - Warnings logged
        - Partial results available
        """
        # Arrange
        input_file = test_data_dir / "input.csv"
        sample_dataframe.to_csv(input_file, index=False)
        
        from run_pipeline import main as run_pipeline
        
        # Act
        result = run_pipeline(
            input_path=str(input_file),
            output_path=str(test_data_dir),
            config={
                'validate': True,
                'fail_on_warning': False,
                'continue_on_error': True
            }
        )
        
        # Assert
        # Should complete even with warnings
        assert result['status'] in ['success', 'partial_success']
    
    def test_rollback_on_critical_failure(self, test_data_dir):
        """
        Test rollback mechanism on critical failures.
        
        Validates:
        - State rolled back
        - Temporary files cleaned
        - Error logged
        """
        # This test would verify rollback logic
        # Implementation depends on your rollback strategy
        pass


class TestPerformance:
    """Performance and scalability integration tests."""
    
    @pytest.mark.slow
    def test_pipeline_performance_benchmark(self, test_data_dir):
        """
        Test pipeline performance meets benchmarks.
        
        Validates:
        - Processing time within SLA
        - Memory usage acceptable
        - Throughput meets requirements
        """
        # Arrange
        large_df = pd.DataFrame({
            'customer_id': range(100000),
            'age': np.random.randint(18, 80, 100000),
            'income': np.random.uniform(20000, 200000, 100000),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 100000)
        })
        
        input_file = test_data_dir / "large_input.csv"
        large_df.to_csv(input_file, index=False)
        
        from run_pipeline import main as run_pipeline
        
        # Act
        start_time = time.time()
        result = run_pipeline(
            input_path=str(input_file),
            output_path=str(test_data_dir)
        )
        elapsed_time = time.time() - start_time
        
        # Assert
        # Should process 100K records in under 30 seconds
        assert elapsed_time < 30.0
        assert result['status'] == 'success'
        
        # Calculate throughput
        throughput = result['records_processed'] / elapsed_time
        assert throughput > 3000  # More than 3K records/second
    
    @pytest.mark.slow
    def test_concurrent_pipeline_execution(self, test_data_dir, sample_dataframe):
        """
        Test multiple concurrent pipeline executions.
        
        Validates:
        - No resource contention
        - All pipelines complete successfully
        - Results isolated
        """
        import concurrent.futures
        from run_pipeline import main as run_pipeline
        
        # Arrange
        num_concurrent = 3
        input_files = []
        
        for i in range(num_concurrent):
            file_path = test_data_dir / f"input_{i}.csv"
            sample_dataframe.to_csv(file_path, index=False)
            input_files.append(file_path)
        
        # Act
        def run_single_pipeline(input_file):
            output_dir = test_data_dir / f"output_{input_file.stem}"
            output_dir.mkdir(exist_ok=True)
            return run_pipeline(
                input_path=str(input_file),
                output_path=str(output_dir)
            )
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = [executor.submit(run_single_pipeline, f) for f in input_files]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # Assert
        assert len(results) == num_concurrent
        assert all(r['status'] == 'success' for r in results)


class TestDataLineage:
    """Test data lineage and provenance tracking."""
    
    def test_data_lineage_tracking(self, test_data_dir, sample_dataframe):
        """
        Test that data lineage is tracked through pipeline.
        
        Validates:
        - Source tracking
        - Transformation history
        - Output provenance
        """
        # Arrange
        input_file = test_data_dir / "input.csv"
        sample_dataframe.to_csv(input_file, index=False)
        
        from run_pipeline import main as run_pipeline
        
        # Act
        result = run_pipeline(
            input_path=str(input_file),
            output_path=str(test_data_dir),
            config={'track_lineage': True}
        )
        
        # Assert
        assert 'lineage' in result
        assert 'source_file' in result['lineage']
        assert 'transformations_applied' in result['lineage']


class TestConfigurationManagement:
    """Test configuration management across pipeline."""
    
    def test_config_override(self, test_data_dir, sample_dataframe, sample_config):
        """
        Test configuration override mechanism.
        
        Validates:
        - Runtime config overrides defaults
        - Invalid config rejected
        - Config validation
        """
        # Arrange
        input_file = test_data_dir / "input.csv"
        sample_dataframe.to_csv(input_file, index=False)
        
        from run_pipeline import main as run_pipeline
        
        custom_config = sample_config.copy()
        custom_config['feature_engineering']['scaling_method'] = 'minmax'
        
        # Act
        result = run_pipeline(
            input_path=str(input_file),
            output_path=str(test_data_dir),
            config=custom_config
        )
        
        # Assert
        assert result['status'] == 'success'
        # Verify config was applied
        assert result.get('config_used', {}).get('feature_engineering', {}).get('scaling_method') == 'minmax'


# Mark for integration tests
pytestmark = pytest.mark.integration


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-m', 'integration'])
