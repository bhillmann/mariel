import json
import codecs
from joblib import Parallel, delayed

def save_file(i, line):
    if i%20 == 1:
        print(i)
        review = json.loads(line)
        f = codecs.open('reviews/' + review['review_id'] + '.txt', 'w', encoding='utf8')
        f.write(review['text'])
        f.close()
        return 'reviews/' + review['review_id']

def yield_file_names():
    with codecs.open('./yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json', encoding='utf8') as f:
        for i, line in enumerate(f):
            yield i, line


if __name__ == '__main__':
    review_ids = Parallel(n_jobs=8)(delayed(save_file)(i, line) for i, line in yield_file_names())

    f = open('review_doclist.txt', 'w')
    for doc in review_ids:
        if doc:
            f.write(doc)
    f.close()
