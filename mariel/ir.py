import yelp_stream
import os
import pandas as pd

path = os.path.join(os.path.dirname(__file__), 'cache')
s = pd.Series.from_csv(os.path.join(path, '0_top_docs.csv'))
s = pd.Series(s)
s.sort()

for ind, json in enumerate(yelp_stream.yield_midwest_json()):
    if ind in s[0:6].index:
        print(s[ind])
        print(s.index.get_loc(ind))
        print(json)