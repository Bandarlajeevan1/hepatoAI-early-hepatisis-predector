"""
Multistage Ensemble Model (MSEM): trains base classifiers and a stacking meta-learner.
Exposes `train` and `predict_proba` interfaces and saves the trained pipeline.
"""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.base import clone
import joblib
import xgboost as xgb


class MSEMEnsemble:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.selector = None  # Feature selector (e.g., SelectKBest, HDPSO)
        self.imputer = None
        self.feature_names = None
        self.base_clfs = {
            "rf": RandomForestClassifier(n_estimators=100, random_state=random_state),
            "svm": SVC(probability=True, kernel="rbf", random_state=random_state),
            "lr": LogisticRegression(max_iter=1000, random_state=random_state),
            "xgb": xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=random_state)
        }
        self.meta = LogisticRegression(max_iter=1000)

    def train(self, X, y):
        # scale
        Xs = self.scaler.fit_transform(X)
        # train base classifiers
        self.fitted_bases = {}
        meta_features = np.zeros((Xs.shape[0], len(self.base_clfs)))
        for i, (k, clf) in enumerate(self.base_clfs.items()):
            model = clone(clf)
            model.fit(Xs, y)
            self.fitted_bases[k] = model
            meta_features[:, i] = model.predict_proba(Xs)[:, 1]
        # train meta-learner on base predictions
        self.meta.fit(meta_features, y)
        return self

    def predict_proba(self, X):
        # Apply feature selector if available
        if self.selector is not None:
            X = self.selector.transform(X)
        Xs = self.scaler.transform(X)
        meta_features = np.column_stack([clf.predict_proba(Xs)[:, 1] for clf in self.fitted_bases.values()])
        meta_proba = self.meta.predict_proba(meta_features)[:, 1]
        return meta_proba

    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)

    def save(self, path):
        joblib.dump({
            "scaler": self.scaler,
            "selector": self.selector,
            "imputer": self.imputer,
            "feature_names": self.feature_names,
            "bases": self.fitted_bases,
            "meta": self.meta
        }, path)

    @staticmethod
    def load(path):
        data = joblib.load(path)
        obj = MSEMEnsemble()
        obj.scaler = data["scaler"]
        obj.selector = data.get("selector", None)  # Support old models without selector
        obj.imputer = data.get("imputer", None)
        obj.feature_names = data.get("feature_names", None)
        obj.fitted_bases = data["bases"]
        obj.meta = data["meta"]
        return obj


if __name__ == "__main__":
    print("MSEM ensemble module")
