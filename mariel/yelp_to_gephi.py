import pandas as pd
import os

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), 'cache')
    phi = pd.DataFrame.from_csv(os.path.join(path, 'phi.csv'))
    theta = pd.DataFrame.from_csv(os.path.join(path, 'theta.csv'))