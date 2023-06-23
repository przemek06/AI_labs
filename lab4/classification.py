from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import f1_score
from sklearn.tree import DecisionTreeClassifier

bayes_hyperparameters = [
    (0.1, 0.0),
    (0.25, 0.0),
    (0.50, 0.0),
    (0.1, 0.5),
    (0.25, 0.5),
    (0.50, 0.5),
    (0.1, 0.25),
    (0.25, 0.25),
    (0.50, 0.25),
    (0.1, 0.35),
    (0.25, 0.35),
    (0.50, 0.35),
]

decision_tree_hyperparameters = [
    ("gini", 4),
    ("entropy", 4),
    ("gini", 6),
    ("entropy", 6),
    ("gini", 7),
    ("entropy", 7),
    ("gini", 9),
    ("entropy", 9),
    ("gini", 10),
    ("entropy", 10),
    ("gini", 12),
    ("entropy", 12),
]

def train_bayes_model(X_train, Y_train, X_valid, Y_valid):
    best = bayes_hyperparameters[0]
    best_accuracy = float("-inf")

    for alpha, binarize in bayes_hyperparameters:
        classifier = BernoulliNB(alpha=alpha, binarize=binarize)
        classifier.fit(X_train, Y_train)
        y_pred = classifier.predict(X_valid)
        accuracy = f1_score(Y_valid, y_pred, average='micro')

        if accuracy > best_accuracy:
            best = alpha, binarize

    classifier = BernoulliNB(alpha=best[0], binarize=best[1])
    classifier.fit(X_train, Y_train)

    return classifier, best

def train_decision_tree_model(X_train, Y_train, X_valid, Y_valid):
    best = decision_tree_hyperparameters[0]
    best_accuracy = float("-inf")

    for criterion, max_depth in decision_tree_hyperparameters:
        classifier = DecisionTreeClassifier(criterion=criterion, max_depth=max_depth)
        classifier.fit(X_train, Y_train)
        y_pred = classifier.predict(X_valid)
        accuracy = f1_score(Y_valid, y_pred, average='micro')

        print("F1 score for parameters " + str((criterion, max_depth)) + ": " + str(accuracy)) 

        if accuracy > best_accuracy:
            best = criterion, max_depth
            best_accuracy = accuracy

    classifier = DecisionTreeClassifier(criterion=best[0], max_depth=best[1])
    classifier.fit(X_train, Y_train)

    return classifier, best