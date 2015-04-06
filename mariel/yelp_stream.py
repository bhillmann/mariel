import codecs
import os
import json
import ujson

def yield_midwest_json():
    midwest = ['MN', 'IL', 'IN', 'WI', 'IA', 'KS', 'MI', 'MO', 'NE', 'ND', 'OH', 'SD']
    path = os.path.join(os.path.dirname(__file__),
                        '../data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json')
    with codecs.open(path, encoding='utf8') as f:
        for line in f:
            json = ujson.loads(line)
            if json['state'] in midwest:
                yield json

def yield_file_names():
    path = os.path.join(os.path.dirname(__file__),
                        '../data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json')
    with codecs.open(path, encoding='utf8') as f:
        for line in f:
            yield json.loads(line)

def yield_first():
    gen = yield_file_names()
    for i, d in enumerate(gen):
        if i < 100000:
            if i % 1000 == 0:
                print(i)
            yield d
        else:
            break
