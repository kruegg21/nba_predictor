import numpy as np
import pandas as pd
import pickle
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

def linear_model(df,
                 dependent_variable,
                 ridge = True,
                 lasso = True,
                 svr = True,
                 train = True):
    """
    Input:
        df -- DataFrame with dependent and independent variables
        dependent_variable -- string of column name of dependent variable
        ridge -- boolean indicating whether to consider Ridge Regression
        lasso -- boolean indicating whether to consider Lasso Regression
        svr -- boolean indicating whether to consider SVR
        train -- boolean indicating whether to train linear model
    Output:
        A Series of predictions for dependent variable
    """

    # Print information
    models = [model for model in [ridge, lasso, svr] if model == True]
    "Using {} models to predict {}".format(models, dependent_variable)

    # Get independent variables
    independent_variables = get_independent_variables(df.columns,
                                                      dependent_variable)

    # Find rows of DataFrame that do not have any NaN values for any independent_variables
    prediction_indices = np.where(np.all(np.isfinite(df[independent_variables]), axis = 1))[0]
    train_indices = np.where(np.all(np.isfinite(df), axis = 1))[0]

    # Subset DataFrame to only include full independent variable indices
    train_set = df.iloc[train_indices,:]
    prediction_set = df.iloc[prediction_indices,:]

    # Make numpy arrays
    y_train = train_set.pop(dependent_variable).values
    X_train = train_set.values

    y_pred = prediction_set.pop(dependent_variable).values
    X_pred = prediction_set.values

    # Standardize data
    scale = StandardScaler()
    X_train = scale.fit_transform(X_train)
    X_pred = scale.fit_transform(X_pred)

    # Create degree 3 polynomial features
    poly = PolynomialFeatures(degree = 3)
    X_train = poly.fit_transform(X_train)
    X_pred = poly.fit_transform(X_pred)

    if train:
        # Parameters for grid search
        cv = 5
        verbose = 20
        param_grid_lasso = {'alpha': [0,0.01,0.05,0.1]}
        param_grid_ridge = {'alpha': [0,0.01,0.05,0.1]}
        param_grid_svr = {'C': [1,2,5],
                          'gamma': [.2,.4,.6]}

        # Keep track of scores for all our models where the scores are the R2 for CV
        score_dict = {'lasso': (0, None), 'ridge': (0, None), 'svr': (0, None)}

        if lasso:
            # Train Lasso Regression Model
            lasso = Lasso()

            # Grid Search
            gscv_lasso = GridSearchCV(lasso,
                                      param_grid = param_grid_lasso,
                                      verbose = verbose,
                                      n_jobs = -1,
                                      cv = cv)
            gscv_lasso.fit(X_train, y_train)

            # Remember best score and estimator
            score_dict['lasso'] = (gscv_lasso.best_score_, \
                                   gscv_lasso.best_estimator_)

            # Print results
            print "Best params for Lasso: {}".format(gscv_lasso.best_params_)
            print "Best score for Lasso: {}".format(gscv_lasso.best_score_)
            print "Coefs for Lasso: {}".format(gscv_lasso.best_estimator_.coef_)

        if ridge:
            # Train Lasso Regression Model
            ridge = Ridge()
            gscv_ridge = GridSearchCV(ridge,
                                      param_grid = param_grid_ridge,
                                      verbose = verbose,
                                      n_jobs = -1,
                                      cv = cv)
            gscv_ridge.fit(X_train, y_train)

            # Remember best score and estimator
            score_dict['ridge'] = (gscv_ridge.best_score_, \
                                   gscv_ridge.best_estimator_)

            # Print results
            print "Best parameters for ridge: {}".format(gscv_ridge.best_params_)
            print "Best score for ridge: {}".format(gscv_ridge.best_score_)
            print "Coefficients for rideg: {}".format(gscv_ridge.best_estimator_.coef_)

        if svr:
            # Train SVM Regression Model
            ridge = SVR()
            gscv_svm = GridSearchCV(ridge,
                                    param_grid = param_grid_svr,
                                    verbose = verbose,
                                    n_jobs = -1,
                                    cv = cv)
            gscv_svm.fit(X_train, y_train)

            # Remember best score and estimator
            score_dict['svr'] = (gscv_svm.best_score_, \
                                 gscv_svm.best_estimator_)

             # Print results
            print "Best parameters for SVM: {}".format(gscv_svm.best_params_)
            print "Best score for SVM: {}".format(gscv_svm.best_score_)

        # Find best model
        best = score_dict[max(score_dict, key = lambda x: score_dict[x])]
        print "Best score overall: {}".format(best[0])

        # Pickle model
        with open('models/{}LinearModel.obj'.format(dependent_variable), 'w+') as f:
            pickle.dump(best[1], f)
        linear_model = best[1]

    else:
        # Load pickled model
        with open('models/{}LinearModel.obj'.format(dependent_variable), 'r') as f:
            linear_model = pickle.load(f)

    # Predict using pickle model
    return pd.Series(linear_model.predict(X_pred), index = prediction_indices)

def get_independent_variables(all_columns, dependent_variable):
    """
    Input:
        all_columns -- list of strings of all columns
        dependent_variable -- string of dependent_variable
    Output:
        list of strings of all the columns that are independent variables
    """
    return list(set(all_columns) - set([dependent_variable]))
