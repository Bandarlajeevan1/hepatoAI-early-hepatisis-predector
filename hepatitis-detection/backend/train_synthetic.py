"""
Training script using Synthetic Hepatitis Dataset
Trains MSEM ensemble on synthetic data with clear class separation
Output: trained_model_synthetic.pkl ready for API predictions
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
import joblib
import warnings
warnings.filterwarnings('ignore')

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
SYNTHETIC_DATA_PATH = os.path.join(DATA_DIR, "synthetic_training_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model", "trained_model_synthetic.pkl")


class SyntheticDataTrainer:
    """Train models on synthetic hepatitis dataset"""
    
    def __init__(self):
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.model = None
        self.metrics = {}
    
    def load_data(self):
        """Load synthetic training data"""
        print("\n" + "="*70)
        print("🔬 LOADING SYNTHETIC HEPATITIS DATASET")
        print("="*70)
        
        if not os.path.exists(SYNTHETIC_DATA_PATH):
            raise FileNotFoundError(f"Synthetic data not found at: {SYNTHETIC_DATA_PATH}")
        
        df = pd.read_csv(SYNTHETIC_DATA_PATH)
        print(f"\n✓ Loaded synthetic dataset")
        print(f"  Location: {SYNTHETIC_DATA_PATH}")
        print(f"  Samples: {len(df):,}")
        print(f"  Features: {len(df.columns)}")
        print(f"  File Size: 134 KB")
        
        # Extract features and target
        self.X = df.drop('Outcome', axis=1)
        self.y = df['Outcome']
        
        print(f"\n✓ Extracted features and target")
        print(f"  Features shape: {self.X.shape}")
        print(f"  Target classes: {sorted(self.y.unique())}")
        print(f"  Class distribution:")
        print(f"    - Healthy (0): {sum(self.y==0):,} ({sum(self.y==0)/len(self.y)*100:.1f}%)")
        print(f"    - Hepatitis (1): {sum(self.y==1):,} ({sum(self.y==1)/len(self.y)*100:.1f}%)")
        
        # Feature statistics
        print(f"\n✓ Feature Statistics (by class):")
        print(f"\n  NEGATIVE CASES (Healthy):")
        neg_X = self.X[self.y == 0]
        print(f"    Bilirubin: {neg_X['Bilirubin'].mean():.2f} ± {neg_X['Bilirubin'].std():.2f} mg/dL")
        print(f"    SGOT (AST): {neg_X['SGOT_AST'].mean():.2f} ± {neg_X['SGOT_AST'].std():.2f} U/L")
        print(f"    SGPT (ALT): {neg_X['SGPT_ALT'].mean():.2f} ± {neg_X['SGPT_ALT'].std():.2f} U/L")
        print(f"    Albumin: {neg_X['Albumin'].mean():.2f} ± {neg_X['Albumin'].std():.2f} g/dL")
        
        print(f"\n  POSITIVE CASES (Hepatitis):")
        pos_X = self.X[self.y == 1]
        print(f"    Bilirubin: {pos_X['Bilirubin'].mean():.2f} ± {pos_X['Bilirubin'].std():.2f} mg/dL")
        print(f"    SGOT (AST): {pos_X['SGOT_AST'].mean():.2f} ± {pos_X['SGOT_AST'].std():.2f} U/L")
        print(f"    SGPT (ALT): {pos_X['SGPT_ALT'].mean():.2f} ± {pos_X['SGPT_ALT'].std():.2f} U/L")
        print(f"    Albumin: {pos_X['Albumin'].mean():.2f} ± {pos_X['Albumin'].std():.2f} g/dL")
        
        print("\n" + "="*70)
        return self
    
    def split_and_normalize(self, test_size=0.2, random_state=42):
        """Split data and normalize features"""
        print("\n" + "="*70)
        print("📊 TRAIN-TEST SPLIT & NORMALIZATION")
        print("="*70)
        
        # Stratified split to maintain class balance
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y,
            test_size=test_size,
            random_state=random_state,
            stratify=self.y
        )
        
        print(f"\n✓ Data split:")
        print(f"  Training set: {len(self.X_train):,} samples")
        print(f"    - Healthy (0): {sum(self.y_train==0):,}")
        print(f"    - Hepatitis (1): {sum(self.y_train==1):,}")
        print(f"  Test set: {len(self.X_test):,} samples")
        print(f"    - Healthy (0): {sum(self.y_test==0):,}")
        print(f"    - Hepatitis (1): {sum(self.y_test==1):,}")
        
        # Normalize features
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
        
        print(f"\n✓ Features normalized using StandardScaler")
        print(f"  Training set: {self.X_train.shape}")
        print(f"  Test set: {self.X_test.shape}")
        
        print("\n" + "="*70)
        return self
    
    def train_ensemble(self):
        """Train ensemble model with multiple classifiers"""
        print("\n" + "="*70)
        print("🤖 TRAINING ENSEMBLE MODEL")
        print("="*70)
        
        # Calculate class weights for imbalance handling
        neg_count = sum(self.y_train == 0)
        pos_count = sum(self.y_train == 1)
        scale_pos_weight = neg_count / pos_count if pos_count > 0 else 1.0
        
        print(f"\n✓ Training base classifiers:")
        print(f"  Class weight scale: {scale_pos_weight:.2f}")
        
        # Base classifiers
        rf = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced',
            n_jobs=-1
        )
        print(f"  ✓ Random Forest initialized")
        
        svm = SVC(
            kernel='rbf',
            C=1.0,
            gamma='scale',
            probability=True,
            random_state=42,
            class_weight='balanced'
        )
        print(f"  ✓ SVM initialized")
        
        lr = LogisticRegression(
            max_iter=1000,
            random_state=42,
            class_weight='balanced',
            solver='lbfgs'
        )
        print(f"  ✓ Logistic Regression initialized")
        
        xgb_model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42,
            use_label_encoder=False,
            eval_metric='logloss',
            scale_pos_weight=scale_pos_weight
        )
        print(f"  ✓ XGBoost initialized")
        
        # Create voting ensemble
        self.model = VotingClassifier(
            estimators=[
                ('rf', rf),
                ('svm', svm),
                ('lr', lr),
                ('xgb', xgb_model)
            ],
            voting='soft'
        )
        
        print(f"\n✓ Training Voting Ensemble (soft voting)...")
        self.model.fit(self.X_train, self.y_train)
        print(f"  ✓ Model trained successfully!")
        
        print("\n" + "="*70)
        return self
    
    def evaluate(self):
        """Evaluate model on test set"""
        print("\n" + "="*70)
        print("📈 MODEL EVALUATION")
        print("="*70)
        
        from sklearn.metrics import (
            accuracy_score, precision_score, recall_score, f1_score,
            roc_auc_score, confusion_matrix, classification_report
        )
        
        # Predictions
        y_pred = self.model.predict(self.X_test)
        y_pred_proba = self.model.predict_proba(self.X_test)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(self.y_test, y_pred)
        precision = precision_score(self.y_test, y_pred, zero_division=0)
        recall = recall_score(self.y_test, y_pred, zero_division=0)
        f1 = f1_score(self.y_test, y_pred, zero_division=0)
        auc_roc = roc_auc_score(self.y_test, y_pred_proba)
        
        # Confusion matrix
        cm = confusion_matrix(self.y_test, y_pred)
        tn, fp, fn, tp = cm.ravel()
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        
        self.metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'auc_roc': auc_roc,
            'specificity': specificity
        }
        
        print(f"\n✓ Performance Metrics:")
        print(f"  Accuracy:   {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"  Precision:  {precision:.4f}")
        print(f"  Recall:     {recall:.4f}")
        print(f"  Specificity: {specificity:.4f}")
        print(f"  F1-Score:   {f1:.4f}")
        print(f"  AUC-ROC:    {auc_roc:.4f}")
        
        print(f"\n✓ Confusion Matrix:")
        print(f"  True Negatives:  {tn}")
        print(f"  False Positives: {fp}")
        print(f"  False Negatives: {fn}")
        print(f"  True Positives:  {tp}")
        
        print(f"\n✓ Classification Report:")
        print(classification_report(self.y_test, y_pred, 
                                   target_names=['Healthy', 'Hepatitis']))
        
        print("\n" + "="*70)
        return self
    
    def save_model(self):
        """Save trained model and scaler"""
        print("\n" + "="*70)
        print("💾 SAVING MODEL")
        print("="*70)
        
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        
        # Save model and scaler together
        model_package = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': list(self.X.columns),
            'metrics': self.metrics
        }
        
        joblib.dump(model_package, MODEL_PATH)
        
        print(f"\n✓ Model package saved")
        print(f"  Location: {MODEL_PATH}")
        print(f"  Contains: Model + Scaler + Feature names + Metrics")
        print(f"\n✓ Features ({len(model_package['feature_names'])}):")
        for i, name in enumerate(model_package['feature_names'], 1):
            print(f"  {i:2d}. {name}")
        
        print("\n" + "="*70)
        return self


def generate_test_samples():
    """Generate sample test data for manual testing"""
    print("\n" + "="*70)
    print("📝 GENERATING TEST SAMPLES")
    print("="*70)
    
    test_samples = {
        'negative_case_1': {
            'Age': 45,
            'Sex': 1,
            'Bilirubin': 0.8,
            'Alkaline_Phosphatase': 90.0,
            'SGOT_AST': 28.0,
            'SGPT_ALT': 32.0,
            'Albumin': 4.1,
            'Total_Proteins': 7.2,
            'Fatigue': 0,
            'Malaise': 0,
            'Anorexia': 0,
            'Liver_Big': 0,
            'Liver_Firm': 0,
            'Spleen_Palpable': 0,
            'Ascites': 0,
            'Varices': 0,
            'description': 'HEALTHY: All markers normal, no symptoms'
        },
        'negative_case_2': {
            'Age': 62,
            'Sex': 0,
            'Bilirubin': 0.5,
            'Alkaline_Phosphatase': 105.0,
            'SGOT_AST': 22.0,
            'SGPT_ALT': 29.0,
            'Albumin': 4.4,
            'Total_Proteins': 7.5,
            'Fatigue': 0,
            'Malaise': 0,
            'Anorexia': 0,
            'Liver_Big': 0,
            'Liver_Firm': 0,
            'Spleen_Palpable': 0,
            'Ascites': 0,
            'Varices': 0,
            'description': 'HEALTHY: Elderly patient, all values normal'
        },
        'positive_case_1': {
            'Age': 38,
            'Sex': 1,
            'Bilirubin': 3.2,
            'Alkaline_Phosphatase': 240.0,
            'SGOT_AST': 185.0,
            'SGPT_ALT': 220.0,
            'Albumin': 2.9,
            'Total_Proteins': 5.9,
            'Fatigue': 1,
            'Malaise': 1,
            'Anorexia': 1,
            'Liver_Big': 1,
            'Liver_Firm': 1,
            'Spleen_Palpable': 1,
            'Ascites': 0,
            'Varices': 0,
            'description': 'HEPATITIS: Clear signs - elevated enzymes (6-7x), low albumin, symptoms present, hepatomegaly'
        },
        'positive_case_2': {
            'Age': 52,
            'Sex': 0,
            'Bilirubin': 4.8,
            'Alkaline_Phosphatase': 310.0,
            'SGOT_AST': 380.0,
            'SGPT_ALT': 420.0,
            'Albumin': 2.7,
            'Total_Proteins': 5.6,
            'Fatigue': 1,
            'Malaise': 1,
            'Anorexia': 0,
            'Liver_Big': 1,
            'Liver_Firm': 1,
            'Spleen_Palpable': 1,
            'Ascites': 1,
            'Varices': 0,
            'description': 'HEPATITIS SEVERE: Very high enzymes (11-13x), ascites present, severe signs'
        }
    }
    
    # Save test samples to file
    test_file = os.path.join(BASE_DIR, "test_samples.json")
    import json
    with open(test_file, 'w') as f:
        json.dump(test_samples, f, indent=2)
    
    print(f"\n✓ Generated 4 test samples:")
    for name, sample in test_samples.items():
        print(f"\n  {name.upper()}:")
        print(f"    {sample['description']}")
        print(f"    Bilirubin: {sample['Bilirubin']}, AST: {sample['SGOT_AST']}, ALT: {sample['SGPT_ALT']}")
    
    print(f"\n✓ Test samples saved to: {test_file}")
    print("\n" + "="*70)
    
    return test_samples


def main():
    """Main training pipeline"""
    print("\n" + "="*80)
    print(" "*20 + "HEPATITIS DETECTION - SYNTHETIC DATA TRAINING")
    print("="*80)
    print(f"Timestamp: {pd.Timestamp.now()}")
    
    try:
        # Initialize trainer
        trainer = SyntheticDataTrainer()
        
        # Training pipeline
        trainer.load_data()\
               .split_and_normalize()\
               .train_ensemble()\
               .evaluate()\
               .save_model()
        
        # Generate test samples
        test_samples = generate_test_samples()
        
        print("\n" + "="*80)
        print(" "*25 + "✅ TRAINING COMPLETE")
        print("="*80)
        print(f"\n✓ Model saved: {MODEL_PATH}")
        print(f"✓ Model accuracy: {trainer.metrics['accuracy']:.2%}")
        print(f"✓ Model AUC-ROC: {trainer.metrics['auc_roc']:.4f}")
        print(f"\n✓ Ready for API predictions!")
        print(f"\nNext steps:")
        print(f"  1. Run backend API: python app.py")
        print(f"  2. Run frontend: cd frontend && npm start")
        print(f"  3. Use test samples in test_samples.json for manual testing")
        
        return trainer
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    trainer = main()
