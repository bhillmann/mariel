import codecs
import os
import json
import ujson

def yield_midwest_json():
    ids = get_midwest_ids()
    path = os.path.join(os.path.dirname(__file__),
                        '../data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json')
    s = 0
    with codecs.open(path, encoding='utf8') as f:
        for line in f:
            json = ujson.loads(line)
            if json['business_id'] in ids:
                s += 1
                if s % 1000 == 0:
                    print(s)
                yield json

def get_midwest_ids():
    midwest = ['MN', 'IL', 'IN', 'WI', 'IA', 'KS', 'MI', 'MO', 'NE', 'ND', 'OH', 'SD']
    ids = set()
    path = os.path.join(os.path.dirname(__file__),
                        '../data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json')
    with codecs.open(path, encoding='utf8') as f:
        for line in f:
            json = ujson.loads(line)
            if json['state'] in midwest:
                ids.add(json['business_id'])
    return ids

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
