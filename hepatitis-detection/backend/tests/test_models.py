"""
Tests for ML models and transformers
"""
import pytest
import numpy as np
import pandas as pd


class TestFLKNNImputer:
    """Test FL-KNN imputer."""

    @pytest.fixture
    def sample_data_with_nans(self):
        """Create sample data with NaN values."""
        data = pd.DataFrame({
            'feature1': [1.0, 2.0, np.nan, 4.0, 5.0],
            'feature2': [10.0, np.nan, 30.0, 40.0, 50.0],
            'feature3': [100.0, 200.0, 300.0, 400.0, 500.0],
        })
        return data

    def test_imputer_initialization(self):
        """FL-KNN imputer should initialize correctly."""
        from model.fl_knn import FLKNNImputer
        imputer = FLKNNImputer(n_neighbors=5)
        assert imputer.n_neighbors == 5

    def test_imputer_fit_transform(self, sample_data_with_nans):
        """Imputer should fit and transform data."""
        from model.fl_knn import FLKNNImputer
        imputer = FLKNNImputer(n_neighbors=3)
        result = imputer.fit_transform(sample_data_with_nans)
        assert result.shape == sample_data_with_nans.shape
        # Check for NaN after imputation
        assert not pd.isna(result).any().any()


class TestEnsemble:
    """Test MSEM ensemble."""

    @pytest.fixture
    def sample_train_data(self):
        """Create sample training data."""
        np.random.seed(42)
        X = np.random.randn(100, 10)
        y = np.random.randint(0, 2, 100)
        return X, y

    def test_ensemble_initialization(self):
        """Ensemble should initialize correctly."""
        from model.ensemble import MSEMEnsemble
        ensemble = MSEMEnsemble(random_state=42)
        assert ensemble is not None

    def test_ensemble_train(self, sample_train_data):
        """Ensemble should train on data."""
        from model.ensemble import MSEMEnsemble
        X, y = sample_train_data
        ensemble = MSEMEnsemble(random_state=42)
        ensemble.train(X, y)
        # Should not raise error

    def test_ensemble_predict(self, sample_train_data):
        """Ensemble should make predictions."""
        from model.ensemble import MSEMEnsemble
        X, y = sample_train_data
        ensemble = MSEMEnsemble(random_state=42)
        ensemble.train(X, y)
        
        predictions = ensemble.predict(X[:5])
        assert predictions.shape == (5,)
        assert all(p in [0, 1] for p in predictions)

    def test_ensemble_predict_proba(self, sample_train_data):
        """Ensemble should return probabilities."""
        from model.ensemble import MSEMEnsemble
        X, y = sample_train_data
        ensemble = MSEMEnsemble(random_state=42)
        ensemble.train(X, y)
        
        probs = ensemble.predict_proba(X[:5])
        assert probs.shape == (5, 2)
        # Probabilities should sum to 1
        assert np.allclose(probs.sum(axis=1), 1.0)

    def test_ensemble_save_load(self, sample_train_data, tmp_path):
        """Ensemble should save and load correctly."""
        from model.ensemble import MSEMEnsemble
        X, y = sample_train_data
        ensemble = MSEMEnsemble(random_state=42)
        ensemble.train(X, y)
        
        # Save
        model_path = tmp_path / "model.pkl"
        ensemble.save(str(model_path))
        assert model_path.exists()
        
        # Load
        loaded = MSEMEnsemble.load(str(model_path))
        assert loaded is not None


class TestFeatureSelection:
    """Test HDPSO feature selector."""

    @pytest.fixture
    def sample_data_for_selection(self):
        """Create sample data for feature selection."""
        np.random.seed(42)
        X = np.random.randn(50, 15)
        y = np.random.randint(0, 2, 50)
        return X, y

    def test_selector_initialization(self):
        """Feature selector should initialize correctly."""
        from model.hdpso import HDPSOFeatureSelector
        selector = HDPSOFeatureSelector(n_particles=10, iters=5)
        assert selector.n_particles == 10

    def test_selector_fit(self, sample_data_for_selection):
        """Feature selector should fit on data."""
        from model.hdpso import HDPSOFeatureSelector
        from sklearn.ensemble import RandomForestClassifier
        
        X, y = sample_data_for_selection
        selector = HDPSOFeatureSelector(n_particles=5, iters=2)
        estimator = RandomForestClassifier(n_estimators=10, random_state=42)
        
        selector.fit(estimator, X, y)
        assert selector.support_ is not None

    def test_selector_transform(self, sample_data_for_selection):
        """Feature selector should transform data."""
        from model.hdpso import HDPSOFeatureSelector
        from sklearn.ensemble import RandomForestClassifier
        
        X, y = sample_data_for_selection
        selector = HDPSOFeatureSelector(n_particles=5, iters=2)
        estimator = RandomForestClassifier(n_estimators=10, random_state=42)
        
        selector.fit(estimator, X, y)
        X_selected = selector.transform(X)
        
        # Selected features should be fewer than original (usually)
        assert X_selected.shape[1] <= X.shape[1]
        assert X_selected.shape[0] == X.shape[0]
