from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn_evaluation import ClassifierEvaluator

# Import some data to play with
iris = datasets.load_iris()
X = iris.data
y = iris.target

# shuffle and split training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)

# Learn to predict each class against the other
classifier = RandomForestClassifier()
classifier = classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
y_score = classifier.predict_proba(X_test)

feature_list = range(4)
target_names = ["setosa", "versicolor", "virginica"]

# Create a trained model instance
ce = ClassifierEvaluator(
    classifier,
    y_test,
    y_pred,
    y_score,
    feature_list,
    target_names,
    estimator_name="super awesome SVC",
)

report = ce.make_report()

# this will automativally render in Jupyter, or you can do report.save('/path')
report
