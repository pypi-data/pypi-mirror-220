import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
# from sklearn.pipeline import Pipeline   # No data leakage issue (using Pipeline, comment-out to trigger code smell)
from sklearn.datasets import load_iris


def data_leakage_example():
    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Data leakage issue (no Pipeline)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    clf = LogisticRegression()
    clf.fit(X_train_scaled, y_train)

    score = clf.score(X_test_scaled, y_test)
    print("Data leakage example score:", score)


def no_data_leakage_example():
    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Code smell - If sklearn is imported and Pipeline is not being used
    # No data leakage issue (using Pipeline, comment-out to trigger code smell)

    # pipe = Pipeline([
    #     ('scaler', StandardScaler()),
    #     ('clf', LogisticRegression())
    # ])
    # pipe = sklearn.pipeline.Pipeline([
    #     ('scaler', StandardScaler()),
    #     ('clf', LogisticRegression())
    # ])


if __name__ == "__main__":
    data_leakage_example()
    no_data_leakage_example()
