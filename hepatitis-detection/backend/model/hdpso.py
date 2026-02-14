"""
Hybrid Dingo + Particle Swarm Optimization (HDPSO) simple binary feature selector.

This is a lightweight, readable implementation suitable for small datasets.
Fitness is evaluated via cross-validated accuracy of a provided estimator.
"""
import numpy as np
from sklearn.model_selection import cross_val_score


class HDPSOFeatureSelector:
    def __init__(self, n_particles=20, iters=30, w=0.72, c1=1.5, c2=1.5, random_state=None):
        self.n_particles = n_particles
        self.iters = iters
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.rs = np.random.RandomState(random_state)

    def _init_particles(self, dim):
        # binary positions and continuous velocities
        pos = self.rs.rand(self.n_particles, dim) > 0.5
        vel = self.rs.randn(self.n_particles, dim) * 0.1
        return pos.astype(float), vel

    def _fitness(self, estimator, X, y, mask):
        # if no features selected, return very low score
        if mask.sum() == 0:
            return 0.0
        Xs = X[:, mask.astype(bool)]
        try:
            scores = cross_val_score(estimator, Xs, y, cv=3, scoring="accuracy")
            return scores.mean()
        except Exception:
            return 0.0

    def fit(self, estimator, X, y):
        n_features = X.shape[1]
        pos, vel = self._init_particles(n_features)
        pbest = pos.copy()
        pbest_score = np.zeros(self.n_particles)
        gbest = pos[0].copy()
        gbest_score = 0.0

        for i in range(self.n_particles):
            mask = pos[i] > 0.5
            pbest_score[i] = self._fitness(estimator, X, y, mask)
            if pbest_score[i] > gbest_score:
                gbest_score = pbest_score[i]
                gbest = pos[i].copy()

        for t in range(self.iters):
            for i in range(self.n_particles):
                r1 = self.rs.rand(n_features)
                r2 = self.rs.rand(n_features)
                vel[i] = self.w * vel[i] + self.c1 * r1 * (pbest[i] - pos[i]) + self.c2 * r2 * (gbest - pos[i])
                # Dingo-inspired random leap: occasional large random perturbation
                if self.rs.rand() < 0.05:
                    vel[i] += self.rs.randn(n_features) * 0.5
                pos[i] = pos[i] + vel[i]
                # sigmoid to map to probability then threshold
                prob = 1.0 / (1.0 + np.exp(-pos[i]))
                pos_bin = (prob > 0.5).astype(float)
                score = self._fitness(estimator, X, y, pos_bin)
                if score > pbest_score[i]:
                    pbest_score[i] = score
                    pbest[i] = pos_bin.copy()
                    if score > gbest_score:
                        gbest_score = score
                        gbest = pos_bin.copy()

        self.support_ = (gbest > 0.5).astype(bool)
        self.gbest_score_ = gbest_score
        return self

    def transform(self, X):
        return X[:, self.support_]

    def fit_transform(self, estimator, X, y):
        self.fit(estimator, X, y)
        return self.transform(X)


if __name__ == "__main__":
    print("HDPSO feature selector module")
