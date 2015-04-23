import os
import pandas as pd
import numpy as np
from sklearn import datasets, linear_model

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), 'cache')
    theta = pd.DataFrame.from_csv(os.path.join(path, 'theta.csv'))
    stars = pd.Series.from_csv(os.path.join(path, 'stars.csv'))

    # Split the data into training/testing sets
    yelp_X_train = theta.values[:-1000]
    yelp_X_test = theta.values[-1000:]

    # Split the targets into training/testing sets
    yelp_y_train = stars.values[:-1000]
    yelp_y_test = stars.values[-1000:]

    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(yelp_X_train, yelp_y_train)
    # The coefficients
    print('Coefficients: \n', regr.coef_)
    # The mean square error
    print("Residual sum of squares: %.2f" %
           np.mean((regr.predict(yelp_X_test) - yelp_y_test) ** 2))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regr.score(yelp_X_test, yelp_y_test))


