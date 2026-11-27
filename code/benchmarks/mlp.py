"""M4: one hidden layer with a square activation, logit output (usable under CKKS, depth 3).

z = w2 . (W1 x + b1)^2 + b2, trained with full-batch Adam on the logistic loss.
"""
import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin


class SquareMLP(ClassifierMixin, BaseEstimator):
    def __init__(self, hidden=12, epochs=300, lr=0.01, l2=0.01, random_state=42):
        self.hidden = hidden
        self.epochs = epochs
        self.lr = lr
        self.l2 = l2
        self.random_state = random_state

    def fit(self, X, y):
        X, y = np.asarray(X, float), np.asarray(y, float)
        rng = np.random.default_rng(self.random_state)
        n, d = X.shape
        p = [rng.normal(0, 1 / np.sqrt(d), (d, self.hidden)), rng.normal(0, 0.1, self.hidden),
             rng.normal(0, 0.1, self.hidden), np.zeros(1)]
        m = [np.zeros_like(v) for v in p]
        v2 = [np.zeros_like(v) for v in p]
        for t in range(1, self.epochs + 1):
            W1, b1, w2, b2 = p
            a = X @ W1 + b1
            z = (a * a) @ w2 + b2
            err = (1 / (1 + np.exp(-np.clip(z, -30, 30))) - y) / n
            da = np.outer(err, w2) * 2 * a
            grads = [X.T @ da + self.l2 * W1 / n * 10, da.sum(0),
                     (a * a).T @ err + self.l2 * w2 / n * 10, np.array([err.sum()])]
            for i, g in enumerate(grads):
                m[i] = 0.9 * m[i] + 0.1 * g
                v2[i] = 0.999 * v2[i] + 0.001 * g * g
                p[i] = p[i] - self.lr * (m[i] / (1 - 0.9 ** t)) / (np.sqrt(v2[i] / (1 - 0.999 ** t)) + 1e-8)
        self.W1_, self.b1_, self.w2_, self.b2_ = p[0], p[1], p[2], float(p[3][0])
        self.classes_ = np.array([0, 1])
        return self

    def decision_function(self, X):
        a = np.asarray(X, float) @ self.W1_ + self.b1_
        return (a * a) @ self.w2_ + self.b2_

    def predict(self, X):
        return (self.decision_function(X) >= 0).astype(int)
