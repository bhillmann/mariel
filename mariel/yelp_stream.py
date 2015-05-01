import codecs
import os
import json
import ujson

def yield_midwest_json():
    path = os.path.join(os.path.dirname(__file__), 'cache')
    try:
        for line in open(os.path.join(path, 'docs.txt')):
            yield ujson.loads(line)
    except:
        yield_from_source()
    
def yield_from_source():
    ids = get_midwest_ids()
    path = os.path.join(os.path.dirname(__file__),
                        '../data/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json')
    s = 0
    with codecs.open(path, encoding='utf8') as f:
        for i, line in enumerate(f):
            if i == 0:
                d = {'text': "I enjoy Cafe Mac's zesty burgers but sometimes I distate their unorthodox pizza.", 'stars': 3}
                yield d
            else:
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

if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), 'cache')
    with open(os.path.join(path, 'docs.txt'), 'w') as f:
        for json in yield_from_source():
            f.write(ujson.dumps(json)+'\n')
