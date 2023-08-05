import numpy as np

from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB
from sklearn.datasets import load_iris

from scikit_endpoint.map import convert_estimator
from scikit_endpoint.utils import shape

METHODS = ["predict", "predict_proba", "predict_log_proba", "_joint_log_likelihood"]


def test_import():
    from scikit_endpoint import naive_bayes  # noqa F403

    assert True


def test_gaussian():
    X, y = load_iris(return_X_y=True)
    X_ = X.tolist()
    for y_ in [y, (y == 0).astype(int), (y == 2).astype(int)]:
        clf = GaussianNB()
        clf.fit(X, y_)
        clf_ = convert_estimator(clf)

        for method in METHODS:
            scores = getattr(clf, method)(X)
            scores_ = getattr(clf_, method)(X_)
            assert np.allclose(scores.shape, shape(scores_))
            assert np.allclose(scores, scores_, equal_nan=True)


def test_multinomial():
    X, y = load_iris(return_X_y=True)
    X_ = X.tolist()
    for y_ in [y, (y == 0).astype(int), (y == 2).astype(int)]:
        clf = MultinomialNB()
        clf.fit(X, y_)
        clf_ = convert_estimator(clf)

        for method in METHODS:
            scores = getattr(clf, method)(X)
            scores_ = getattr(clf_, method)(X_)
            assert np.allclose(scores.shape, shape(scores_))
            assert np.allclose(scores, scores_, equal_nan=True)


def test_complement():
    X, y = load_iris(return_X_y=True)
    X_ = X.tolist()
    for y_ in [y, (y == 0).astype(int), (y == 2).astype(int)]:
        clf = ComplementNB()
        clf.fit(X, y_)
        clf_ = convert_estimator(clf)

        for method in METHODS:
            scores = getattr(clf, method)(X)
            scores_ = getattr(clf_, method)(X_)
            assert np.allclose(scores.shape, shape(scores_))
            assert np.allclose(scores, scores_, equal_nan=True)
