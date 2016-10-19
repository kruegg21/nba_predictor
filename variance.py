import numpy as np
import matplotlib.pyplot as plt

def get_variance(model, X_pred, player, element, plot = False):
    """
    Input:
        model -- sklearn RandomForestRegressor model
        X_pred -- np.array or list of independent variables that we want to get
                  variance for
    Output:
        variance_list -- list of the estimated variance for each data point in
                         X_pred

    Estimates the variance of our prediction by summing the variance of the
    leaves that each data point maps to in our random forest model and dividing
    by the total number of training examples that each data point maps to.

    This is inexact because it does not take into account the variance that
    occurs within each leaf.
    """

    # Cast 'X_pred' to np.array
    X_pred = np.array(X_pred)

    variance_list = list()
    for row, player in zip(X_pred, player):
        prediction_list = list()
        for tree in model.estimators_:
            # Get the leaf that each data point is assigned to
            leaf = tree.apply(row)

            # Get the prediction for each data point
            prediction = tree.predict(row)

            # Get the number of elements in each node
            n_elements = tree.tree_.n_node_samples[leaf]

            # Add to list of predictions
            prediction_list += [prediction[0]] * n_elements[0]
        variance_list.append(np.var(prediction_list))
        if plot:
            plt.hist(prediction_list)
            plt.title("{} {}".format(player, element))
            plt.show()
    return variance_list
