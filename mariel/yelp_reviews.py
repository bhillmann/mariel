from yelp_stream import yield_midwest_json
from pandas import Series


def get_star_vector():
    return Series([d['stars'] for d in yield_midwest_json()])


if __name__ == "__main__":
    xx = get_star_vector()
    path = 'C:/Users/Benjamin/Projects/mariel/mariel/cache/star_vector.csv'
    xx.to_csv(path)