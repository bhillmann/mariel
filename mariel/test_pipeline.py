from yelp_stream import yield_file_names
import yelp_dictionary

gen = yield_file_names()
for i in range(20):
    d = next(gen)
    print(yelp_dictionary.preprocess_line(d['text']))