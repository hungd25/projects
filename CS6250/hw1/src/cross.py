import models_partc
from sklearn.model_selection import KFold, ShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from numpy import mean, array
import numpy as np
import pandas as pd
from sklearn.metrics import *

import utils

# USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

# USE THIS RANDOM STATE FOR ALL OF YOUR CROSS VALIDATION TESTS, OR THE TESTS WILL NEVER PASS
RANDOM_STATE = 545510477

# input: training data and corresponding labels
# output: accuracy, auc
def get_acc_auc_kfold(X, Y, k=5):
    # TODO:First get the train indices and test indices for each iteration
    # Then train the classifier accordingly
    # Report the mean accuracy and mean auc of all the folds
    k_fold_val = KFold(n_splits=k, random_state=RANDOM_STATE)
    logistic_reg = LogisticRegression()
    acc_scores = []
    auc_scores = []
    for train_idx, test_idx in k_fold_val.split(X):
        k = logistic_reg.fit(X[train_idx], Y[train_idx])
        auc_scores.append(roc_auc_score(k.predict(X[test_idx]), Y[test_idx]))
        acc_scores.append(accuracy_score(k.predict(X[test_idx]), Y[test_idx]))
    accuracy = mean(acc_scores)
    auc = mean(auc_scores)
    return accuracy, auc


# input: training data and corresponding labels
# output: accuracy, auc
def get_acc_auc_randomisedCV(X, Y, iterNo=5, test_percent=0.2):
    # TODO: First get the train indices and test indices for each iteration
    # Then train the classifier accordingly
    # Report the mean accuracy and mean auc of all the iterations
    k_fold_val = ShuffleSplit(
        n_splits=iterNo, test_size=test_percent, random_state=RANDOM_STATE
    )
    logistic_reg = LogisticRegression()
    acc_scores = []
    auc_scores = []
    for train_idx, test_idx in k_fold_val.split(X):
        k = logistic_reg.fit(X[train_idx], Y[train_idx])
        auc_scores.append(roc_auc_score(k.predict(X[test_idx]), Y[test_idx]))
        acc_scores.append(accuracy_score(k.predict(X[test_idx]), Y[test_idx]))
    accuracy = mean(acc_scores)
    auc = mean(auc_scores)
    return accuracy, auc


def main():
    X, Y = utils.get_data_from_svmlight("../deliverables/features_svmlight.train")
    print("Classifier: Logistic Regression__________")
    acc_k, auc_k = get_acc_auc_kfold(X, Y)
    print(("Average Accuracy in KFold CV: " + str(acc_k)))
    print(("Average AUC in KFold CV: " + str(auc_k)))
    acc_r, auc_r = get_acc_auc_randomisedCV(X, Y)
    print(("Average Accuracy in Randomised CV: " + str(acc_r)))
    print(("Average AUC in Randomised CV: " + str(auc_r)))


if __name__ == "__main__":
    main()
