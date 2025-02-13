# Do not use anything outside of the standard distribution of python
# when implementing this class
import math 

class LogisticRegressionSGD:
    """
    Logistic regression with stochastic gradient descent
    """

    def __init__(self, eta, mu, n_feature):
        """
        Initialization of model parameters
        """
        self.eta = eta
        self.weight = [0.0] * n_feature
        self.mu = mu

    def fit(self, X, y):
        """
        Update model using a pair of training sample
        """
        model = 0

        updated_model = self.weight[:]

        for item in X:
            model = model + self.weight[item[0]] * item[1]

        for item in X:
            updateModel = item[1] * (y-1 / (1 + math.exp(-model)))
            updated_model[item[0]] = updated_model[item[0]] + self.eta * updateModel

        for item in range(len(self.weight)):
            updated_model[item] = updated_model[item] - self.eta * self.mu * (self.weight[item] * 2)

        self.weight = updated_model

    def predict(self, X):
        """
        Predict 0 or 1 given X and the current weights in the model
        """
        return 1 if predict_prob(X) > 0.5 else 0

    def predict_prob(self, X):
        """
        Sigmoid function
        """
        return 1.0 / (1.0 + math.exp(-math.fsum((self.weight[f]*v for f, v in X))))
