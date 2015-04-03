from yelp_stream import yield_file_names
import yelp_dictionary
from joblib import Parallel, delayed

def test_pipeline():
    gen = yield_file_names()
    for d in gen:
        yield yelp_dictionary.preprocess_line(d['text'])

if __name__ == '__main__':
    dictionaries = Parallel(n_jobs=8)(delayed(yelp_dictionary.build_dictionary)(file) for file in test_pipeline())