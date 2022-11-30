"""
Test cases for elbow curve and silhouette score

NOTE: this has a few test cases from the scikit-plot test module. License below.

MIT License

Copyright (c) [2018] [Reiichiro Nakano]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pytest
import numpy as np
from unittest.mock import Mock
import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison

from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.datasets import load_iris as load_data
from sklearn_evaluation import plot
import sklearn_evaluation.plot.clustering as cl


def convert_labels_into_string(y_true):
    return ["A" if x == 0 else x for x in y_true]


np.random.seed(0)
X, y = load_data(return_X_y=True)


def test_n_clusters_in_clf():

    class DummyClusterer:

        def __init__(self):
            pass

        def fit(self):
            pass

        def fit_predict(self):
            pass

    clf = DummyClusterer()
    with pytest.raises(TypeError):
        plot.elbow_curve(X, clf)


def test_cluster_ranges():
    clf = KMeans()
    plot.elbow_curve(X, clf, n_clusters=range(1, 10))


@image_comparison(baseline_images=['elbow_curve_from_results'],
                  extensions=['png'],
                  remove_text=False)
def test_elbow_curve_from_results():
    n_clusters = range(1, 10, 2)
    sum_of_squares = np.array([4572.2, 470.7, 389.9, 335.1, 305.5])
    plot.elbow_curve_from_results(n_clusters, sum_of_squares, times=None)


@image_comparison(baseline_images=['elbow_curve_from_results'],
                  extensions=['png'],
                  remove_text=False)
def test_elbow_curve_from_results_unsorted():
    n_clusters = [5, 3, 9, 1, 7]
    sum_of_squares = np.array([389.9, 470.7, 305.5, 4572.2, 335.1])
    plot.elbow_curve_from_results(n_clusters, sum_of_squares, times=None)


def test_ax_elbow():
    clf = KMeans()
    fig, ax = plt.subplots(1, 1)
    out_ax = plot.elbow_curve(X, clf, ax=ax)
    assert ax is out_ax


def test_n_jobs():
    clf = KMeans()
    plot.elbow_curve(X, clf, n_jobs=2)


@image_comparison(baseline_images=[
    'silhouette_plot_two_clusters', 'silhouette_plot_three_clusters',
    'silhouette_plot_four_clusters', 'silhouette_plot_five_clusters',
    'silhouette_plot_six_clusters'
],
                  extensions=['png'],
                  remove_text=False)
def test_plot_silhouette():
    clf = KMeans()
    plot.silhouette_analysis(X, clf)


@image_comparison(baseline_images=[
    'silhouette_plot_four_clusters', 'silhouette_plot_five_clusters'
],
                  extensions=['png'],
                  remove_text=False)
def test_plot_silhouette_with_cluster_range():
    clf = KMeans(random_state=10)
    plot.silhouette_analysis(X, clf, range_n_clusters=[4, 5])


@image_comparison(baseline_images=[
    'silhouette_plot_four_clusters_minibatchkmeans',
    'silhouette_plot_five_clusters_minibatchkmeans'
],
                  extensions=['png'],
                  remove_text=False)
def test_plot_silhouette_with_minibatchkmeans():
    clf = MiniBatchKMeans(random_state=10)
    plot.silhouette_analysis(X, clf, range_n_clusters=[4, 5])


@image_comparison(baseline_images=['silhouette_plot_spectral'],
                  extensions=['png'],
                  remove_text=False)
def test_cmap():
    clf = KMeans()
    plot.silhouette_analysis(X, clf, range_n_clusters=[2], cmap='Spectral')


@image_comparison(baseline_images=['silhouette_plot_cosine'],
                  extensions=['png'],
                  remove_text=False)
def test_metric():
    clf = KMeans()
    plot.silhouette_analysis(X, clf, range_n_clusters=[6], metric='cosine')


def test_string_classes():
    clf = KMeans()
    cluster_labels = clf.fit_predict(X)
    plot.silhouette_analysis_from_results(
        X, convert_labels_into_string(cluster_labels))


@image_comparison(baseline_images=['silhouette_plot_array_like'],
                  extensions=['png'],
                  remove_text=False)
def test_array_like():
    plot.silhouette_analysis_from_results(X.tolist(), y.tolist())


@image_comparison(baseline_images=['silhouette_plot_array_like_string_label'],
                  extensions=['png'],
                  remove_text=False)
def test_array_like_string():
    plot.silhouette_analysis_from_results(X.tolist(),
                                          convert_labels_into_string(y))


def test_ax_silhouette():
    clf = KMeans()
    cluster_labels = clf.fit_predict(X)
    plot.silhouette_analysis_from_results(X, cluster_labels)
    fig, ax = plt.subplots(1, 1)
    out_ax = plot.silhouette_analysis_from_results(X, cluster_labels)
    assert ax is not out_ax
    out_ax = plot.silhouette_analysis_from_results(X, cluster_labels, ax=ax)
    assert ax is out_ax


def test_ax_params():
    clf = KMeans()
    cluster_labels = clf.fit_predict(X)
    out_ax = plot.silhouette_analysis_from_results(X,
                                                   cluster_labels,
                                                   text_fontsize="large")
    assert out_ax.get_title() == 'Silhouette Analysis'
    assert out_ax.get_ylim() == (0.0, 250.0)


def test_invalid_clusterer():
    clf = DecisionTreeClassifier()
    with pytest.raises(TypeError):
        plot.silhouette_analysis(X, clf)


def test_from_results_call(monkeypatch):
    mock = Mock()
    monkeypatch.setattr(cl, 'silhouette_analysis_from_results', mock)
    clf = KMeans()
    fig, ax = plt.subplots(1, 1)
    ax = plot.silhouette_analysis(X, clf, range_n_clusters=[2, 3], ax=ax)
    assert mock.call_count == 2
    assert mock.return_value == ax
