from yelp_stream import yield_midwest_json
from pandas import Series
import os


def get_star_vector():
    return Series([d['stars'] for d in yield_midwest_json()])

if __name__ == "__main__":
    xx = get_star_vector()
    path = os.path.join(os.path.dirname(__file__), 'cache')
    path = os.path.join(path, 'star_vector.csv')
    xx.to_csv(path)