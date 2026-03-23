"""
Quick prediction script to validate model outputs on a few sample rows.
Prints probabilities and derived labels for inspection.
"""
import os
import numpy as np
import pandas as pd
from model.ensemble import MSEMEnsemble

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "trained_model.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "hepatitis_clean.csv")


def build_input_from_row(model, row_series):
    # If model provides feature_names, build full vector like the API
    fn = getattr(model, 'feature_names', None)
    if fn:
        row = {f: np.nan for f in fn}
        for k, v in row_series.items():
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
        # Leave selector transformation to model.predict_proba (avoid double-transform)
        return X_imputed
    else:
        df = pd.DataFrame([row_series.to_dict()])
        X_numeric = df.select_dtypes(include=[np.number]).to_numpy()
        X_numeric = np.nan_to_num(X_numeric, nan=np.nanmedian(X_numeric))
        return X_numeric


if __name__ == '__main__':
    print("Quick predict: loading model...")
    model = None
    if os.path.exists(MODEL_PATH):
        model = MSEMEnsemble.load(MODEL_PATH)
        print(f"Loaded model from: {MODEL_PATH}")
    else:
        print(f"Model file not found at {MODEL_PATH}. Exiting.")
        raise SystemExit(1)

    df = pd.read_csv(DATA_PATH)
    samples = df.head(3)

    for i, row in samples.iterrows():
        print('\n--- Sample row index:', i, '---')
        X = build_input_from_row(model, row)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        probs = model.predict_proba(X)
        # Determine positive probability robustly
        if getattr(probs, 'ndim', None) == 1:
            prob_pos = float(probs[0])
        elif probs.shape[1] > 1:
            prob_pos = float(probs[0, 1])
        else:
            prob_pos = float(probs[0, 0])
        pred_label = 'Positive' if prob_pos >= 0.5 else 'Negative'
        print(f"Predicted: {pred_label} | Positive probability: {prob_pos:.4f} | Raw probs: {probs}")

    print('\nQuick predict done.')
