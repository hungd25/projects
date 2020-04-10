import numpy as np
from sklearn.datasets import load_svmlight_file
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import *

import utils

# setup the randoms tate
RANDOM_STATE = 545510477

# input: X_train, Y_train
# output: Y_pred
def logistic_regression_pred(X_train, Y_train):
    # train a logistic regression classifier using X_train and Y_train. Use this to predict labels of X_train
    # use default params for the classifier
    logistic_reg_classifier = LogisticRegression(random_state=RANDOM_STATE).fit(
        X_train, Y_train
    )
    Y_pred = logistic_reg_classifier.predict(X_train)
    return Y_pred


# input: X_train, Y_train
# output: Y_pred
def svm_pred(X_train, Y_train):
    # train a SVM classifier using X_train and Y_train. Use this to predict labels of X_train
    # use default params for the classifier
    linear_svc = LinearSVC(random_state=RANDOM_STATE).fit(X_train, Y_train)
    Y_pred = linear_svc.predict(X_train)
    return Y_pred


# input: X_train, Y_train
# output: Y_pred
def decisionTree_pred(X_train, Y_train):
    # train a logistic regression classifier using X_train and Y_train. Use this to predict labels of X_train
    # use max_depth as 5
    decision_tree = DecisionTreeClassifier(random_state=RANDOM_STATE, max_depth=5).fit(
        X_train, Y_train
    )
    Y_pred = decision_tree.predict(X_train)
    return Y_pred


# input: Y_pred,Y_true
# output: accuracy, auc, precision, recall, f1-score
def classification_metrics(Y_pred, Y_true):
    # NOTE: It is important to provide the output in the same order
    acc_scores = accuracy_score(Y_pred, Y_true)
    auc_scores = roc_auc_score(Y_pred, Y_true)
    prec_scores = precision_score(Y_pred, Y_true)
    rec_scores = recall_score(Y_pred, Y_true)
    f_scores = f1_score(Y_pred, Y_true)
    return acc_scores, auc_scores, prec_scores, rec_scores, f_scores


# input: Name of classifier, predicted labels, actual labels
def display_metrics(classifierName, Y_pred, Y_true):
    print("______________________________________________")
    print(("Classifier: " + classifierName))
    acc, auc_, precision, recall, f1score = classification_metrics(Y_pred, Y_true)
    print(("Accuracy: " + str(acc)))
    print(("AUC: " + str(auc_)))
    print(("Precision: " + str(precision)))
    print(("Recall: " + str(recall)))
    print(("F1-score: " + str(f1score)))
    print("______________________________________________")
    print("")


def main():
    X_train, Y_train = utils.get_data_from_svmlight(
        "../deliverables/features_svmlight.train"
    )

    display_metrics(
        "Logistic Regression", logistic_regression_pred(X_train, Y_train), Y_train
    )
    display_metrics("SVM", svm_pred(X_train, Y_train), Y_train)
    display_metrics("Decision Tree", decisionTree_pred(X_train, Y_train), Y_train)


if __name__ == "__main__":
    main()
