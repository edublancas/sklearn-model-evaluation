import pytest
from sklearn_evaluation.models import evaluate_model

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


@pytest.fixture
def get_model_a():
    import urllib.request
    import pandas as pd

    file_name = "heart.csv"

    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/sharmaroshan/"
        "Heart-UCI-Dataset/master/heart.csv",
        filename=file_name,
    )

    data = pd.read_csv(file_name)

    column = "fbs"
    X = data.drop(column, axis=1)
    y = data[column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=2023
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    return model, X_test, y_test, file_name


@pytest.fixture
def get_model_b():
    import urllib.request
    import pandas as pd

    file_name = "heart.csv"

    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/sharmaroshan/"
        "Heart-UCI-Dataset/master/heart.csv",
        filename=file_name,
    )

    data = pd.read_csv(file_name)

    column = "restecg"
    X = data.drop(column, axis=1)
    y = data[column]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=2023
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    return model, X_test, y_test, file_name


def test_evaluate_model(get_model_a):

    model, X_test, y_test, file_name = get_model_a

    y_pred = model.predict(X_test)
    y_score = model.predict_proba(X_test)

    report = evaluate_model(y_test, y_pred, model=model, y_score=y_score)  # noqa
    report.save("example-report.html")

    _clean_file(file_name)


def test_compare_models(get_model_b, capsys):
    model, X_test, y_test, file_name = get_model_b

    y_pred = model.predict(X_test)
    y_score = model.predict_proba(X_test)

    # report = evaluate_model(y_test, y_pred, model=model, y_score=y_score)  # noqa
    # report.save("example-compare-report.html")
    with capsys.disabled():
        print(model.n_outputs_)
    _clean_file(file_name)


def _clean_file(file):
    import pathlib
    file = pathlib.Path("heart.csv")
    file.unlink()
