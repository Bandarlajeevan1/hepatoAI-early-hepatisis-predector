"""
Training script: loads datasets, performs EDA prints, applies FL-KNN imputation,
applies HDPSO feature selection, trains MSEM ensemble, and saves model.

Place `hepatitis.csv` and `ILPD.csv` in `backend/data/` before running.
"""
import os
import pandas as pd
import numpy as np
from model.fl_knn import FLKNNImputer
from model.hdpso import HDPSOFeatureSelector
from model.ensemble import MSEMEnsemble
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import joblib

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "trained_model.pkl")


def load_datasets():
    """Load hepatitis dataset from data directory."""
    print("\n" + "="*60)
    print("LOADING DATASET")
    print("="*60)
    
    # Primary: use hepatitis dataset (has proper class labels)
    hep_path = os.path.join(DATA_DIR, "hepatitis_clean.csv")
    if os.path.exists(hep_path):
        print(f"✓ Loading hepatitis_clean.csv...")
        df = pd.read_csv(hep_path)
        print(f"  Shape: {df.shape}")
        return df
    
    # Fallback: try other filenames
    for fname in ["hepatitis.csv", "bupa.data"]:
        p = os.path.join(DATA_DIR, fname)
        if os.path.exists(p):
            print(f"✓ Loading {fname}...")
            df = pd.read_csv(p)
            print(f"  Shape: {df.shape}")
            return df
    
    raise FileNotFoundError(
        f"No datasets found in {DATA_DIR}. "
        "Run 'python download_datasets.py' first."
    )


def eda(df: pd.DataFrame):
    """Print exploratory data analysis."""
    print("\n" + "="*60)
    print("EXPLORATORY DATA ANALYSIS (EDA)")
    print("="*60)
    print(f"Shape: {df.shape}")
    print(f"\nData Types:\n{df.dtypes.value_counts()}")
    print(f"\nTop 10 Missing Values:\n{df.isnull().sum().sort_values(ascending=False).head(10)}")
    print(f"\nClass Distribution:\n{df.iloc[:, -1].value_counts(dropna=False)}")
    print("="*60)


def preprocess(df: pd.DataFrame):
    """Apply data preprocessing: deduplication, FL-KNN imputation, feature extraction."""
    print("\n" + "="*60)
    print("DATA PREPROCESSING")
    print("="*60)
    
    # Drop duplicates
    initial_shape = df.shape[0]
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Dropped {initial_shape - df.shape[0]} duplicate rows")
    
    # Separate class column (could be first or last)
    if 'class' in df.columns:
        y = df['class'].copy()
        X = df.drop('class', axis=1)
    else:
        # Assume last column is target
        X = df.iloc[:, :-1].copy()
        y = df.iloc[:, -1].copy()
    
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"Class distribution: {y.value_counts().to_dict()}")
    
    # Extract numeric features first
    X_numeric = X.select_dtypes(include=[np.number])
    print(f"Numeric features: {X_numeric.shape}")
    print(f"Missing values before imputation: {X_numeric.isnull().sum().sum()}")
    
    # Apply SimpleImputer (median strategy) for robust NaN handling
    print("\nApplying imputation...")
    imputer = SimpleImputer(strategy='median')
    X_imputed = imputer.fit_transform(X_numeric)
    print(f"Missing values after imputation: {np.isnan(X_imputed).sum()}")
    
    # Ensure target is numeric (0 and 1)
    y_numeric = pd.to_numeric(y, errors="coerce")
    y_numeric = y_numeric.fillna(0).astype(int)
    # Convert to 0-1 if needed (1-2 to 0-1)
    if y_numeric.min() == 1:
        y_numeric = y_numeric - 1
    print(f"Target classes: {np.unique(y_numeric)}")
    print(f"Final class distribution: {np.bincount(y_numeric)}")
    
    print("="*60)
    return X_imputed, y_numeric, X_numeric, imputer


def feature_select(X, y):
    """Apply HDPSO feature selection or use all features if dataset is small."""
    print("\n" + "="*60)
    print("FEATURE SELECTION (HDPSO)")
    print("="*60)
    
    # For small datasets, use simplified feature selection
    from sklearn.feature_selection import SelectKBest, f_classif
    
    if X.shape[0] < 200:  # Small dataset
        print(f"Dataset size ({X.shape[0]}) is small. Using SelectKBest instead of HDPSO...")
        # Select top 80% of features
        k = max(5, int(X.shape[1] * 0.8))
        selector = SelectKBest(f_classif, k=k)
        selector.fit(X, y)
        print(f"Selected {selector.transform(X).shape[1]} features using SelectKBest")
    else:
        print("Using HDPSO for feature selection...")
        selector = HDPSOFeatureSelector(n_particles=15, iters=10, random_state=42)
        base_est = RandomForestClassifier(n_estimators=30, random_state=42)
        selector.fit(base_est, X, y)
        n_selected = selector.support_.sum()
        print(f"Selected {n_selected}/{len(selector.support_)} features (score: {selector.gbest_score_:.4f})")
    
    print("="*60)
    return selector


def train_and_save(X, y, selector, imputer, feature_names):
    """Train MSEM ensemble on selected features and save model."""
    print("\n" + "="*60)
    print("MODEL TRAINING (MSEM Ensemble)")
    print("="*60)
    
    X_selected = selector.transform(X)
    print(f"Training on {X_selected.shape[1]} selected features")
    
    ensemble = MSEMEnsemble(random_state=42)
    ensemble.selector = selector  # Attach selector to ensemble
    # Attach imputer and feature names so prediction can reconstruct inputs
    ensemble.imputer = imputer
    ensemble.feature_names = feature_names
    print("Training base classifiers (RF, SVM, LR, XGBoost)...")
    ensemble.train(X_selected, y)
    
    # Save model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    ensemble.save(MODEL_PATH)
    print(f"\n✓ Model saved to: {MODEL_PATH}")
    print("="*60)


def main():
    """Main training pipeline."""
    print("\n" + "="*70)
    print("HEPATITIS DETECTION - ML TRAINING PIPELINE")
    print("="*70)
    
    try:
        df = load_datasets()
        eda(df)
        X, y, df_clean, imputer = preprocess(df)
        selector = feature_select(X, y)
        feature_names = list(df_clean.columns)
        train_and_save(X, y, selector, imputer, feature_names)
        
        print("\n" + "="*70)
        print("✓ TRAINING COMPLETE!")
        print("="*70)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
