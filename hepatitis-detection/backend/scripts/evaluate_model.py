"""
Evaluate trained model on the full hepatitis dataset and print metrics.
"""
import os
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
from model.ensemble import MSEMEnsemble

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "trained_model.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "hepatitis_clean.csv")


def build_full_input(model, df_row):
    fn = getattr(model, 'feature_names', None)
    if fn:
        row = {f: np.nan for f in fn}
        for k, v in df_row.items():
            if k in row:
                row[k] = v
        df_full = pd.DataFrame([row])
        df_full = df_full.apply(pd.to_numeric, errors='coerce')
        X_full = df_full.to_numpy()
        imp = getattr(model, 'imputer', None)
        if imp is not None:
            try:
                X_imputed = imp.transform(X_full)
            except Exception:
                X_imputed = np.nan_to_num(X_full, nan=np.nanmedian(X_full, axis=0))
        else:
            X_imputed = np.nan_to_num(X_full, nan=np.nanmedian(X_full, axis=0))
        return X_imputed
    else:
        df = pd.DataFrame([df_row])
        X_numeric = df.select_dtypes(include=[np.number]).to_numpy()
        X_numeric = np.nan_to_num(X_numeric, nan=np.nanmedian(X_numeric))
        return X_numeric


if __name__ == '__main__':
    print("Evaluating model on full dataset...")
    if not os.path.exists(MODEL_PATH):
        raise SystemExit(f"Model not found: {MODEL_PATH}")
    model = MSEMEnsemble.load(MODEL_PATH)
    df = pd.read_csv(DATA_PATH)

    # Determine target column: prefer explicit 'class' column used in training
    if 'class' in df.columns:
        y = pd.to_numeric(df['class'], errors='coerce').fillna(0).astype(int).to_numpy()
    else:
        # Fallback: use last column
        y = pd.to_numeric(df.iloc[:, -1], errors='coerce').fillna(0).astype(int).to_numpy()

    probs = []
    preds = []

    for _, row in df.iterrows():
        X = build_full_input(model, row.to_dict())
        if X.ndim == 1:
            X = X.reshape(1, -1)
        # Ensure we apply the same selector used during training (support_ fallback)
        sel = getattr(model, 'selector', None)
        if sel is not None:
            try:
                X = sel.transform(X)
            except Exception:
                # Fallback: if selector exposes support_ mask, use it
                if hasattr(sel, 'support_'):
                    mask = np.asarray(sel.support_, dtype=bool)
                    # If mask length matches columns, apply mask
                    if mask.shape[0] == X.shape[1]:
                        X = X[:, mask]
        p = model.predict_proba(X)
        # p is array shape (1,2) hopefully
        if p.ndim == 1:
            prob_pos = float(p[0])
            pred = 1 if prob_pos >= 0.5 else 0
        elif p.shape[1] > 1:
            prob_pos = float(p[0, 1])
            pred = 1 if prob_pos >= 0.5 else 0
        else:
            prob_pos = float(p[0, 0])
            pred = 1 if prob_pos >= 0.5 else 0
        probs.append(prob_pos)
        preds.append(pred)

    probs = np.array(probs)
    preds = np.array(preds)

    cm = confusion_matrix(y, preds)
    report = classification_report(y, preds, digits=4)

    print(f"Dataset size: {len(y)}")
    print("Confusion matrix (rows=true, cols=pred):")
    print(cm)
    print("\nClassification report:")
    print(report)
    print("\nPositive rate (predicted): {:.2%}".format(preds.mean()))
    print("Average positive probability: {:.4f}".format(probs.mean()))
