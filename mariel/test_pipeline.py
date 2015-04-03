from yelp_stream import yield_file_names
import yelp_dictionary

def test_pipeline():
    gen = yield_file_names()
    for d in gen:
        yield yelp_dictionary.preprocess_line(d['text'])

dictionary = yelp_dictionary.build_dictionary(test_pipeline())
dictionary.save('cache/real.dict')