"""
Simple Fuzzy Logic based KNN imputer for numerical/categorical missing values.

This implementation uses Euclidean distance on available features and
computes fuzzy weights = 1/(dist+eps)^m to compute weighted average for numeric
and weighted mode for categorical attributes.
"""
import numpy as np
import pandas as pd
from collections import Counter


class FLKNNImputer:
    def __init__(self, n_neighbors=5, m=2.0, eps=1e-6):
        self.n_neighbors = n_neighbors
        self.m = m
        self.eps = eps

    def fit(self, X: pd.DataFrame):
        self._fit_df = X.copy()
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        df = X.copy()
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for idx in df.index:
            row = df.loc[idx]
            missing = row[row.isnull()].index.tolist()
            if not missing:
                continue
            # construct distances to other rows using non-missing features
            mask = row.notnull()
            if mask.sum() == 0:
                continue
            candidates = self._fit_df[self._fit_df.index != idx]
            # for candidate rows, only consider columns where both present
            dists = []
            for j, crow in candidates.iterrows():
                common = mask & crow.notnull()
                if common.sum() == 0:
                    dists.append(np.inf)
                    continue
                diff = row[common] - crow[common]
                # treat non-numeric as 0 difference if equal else 1
                diff_num = pd.to_numeric(diff, errors="coerce")
                diff_num = diff_num.fillna((row[common] != crow[common]).astype(float))
                dists.append(np.sqrt((diff_num ** 2).sum()))
            candidates = candidates.assign(_dist=np.array(dists))
            neighbors = candidates.nsmallest(self.n_neighbors, "_dist")
            for col in missing:
                vals = neighbors[col].dropna()
                if vals.empty:
                    continue
                d = neighbors.loc[vals.index, "_dist"].values
                w = 1.0 / (d + self.eps) ** self.m
                if pd.api.types.is_numeric_dtype(vals):
                    df.at[idx, col] = np.sum(w * vals.values) / (w.sum() + self.eps)
                else:
                    # weighted mode
                    counts = {}
                    for v, ww in zip(vals.values, w):
                        counts[v] = counts.get(v, 0.0) + ww
                    df.at[idx, col] = max(counts.items(), key=lambda x: x[1])[0]
        return df

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self.fit(X)
        return self.transform(X)


if __name__ == "__main__":
    print("FL-KNN Imputer module")
