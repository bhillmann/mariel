import pandas as pd
import os
from kaggle_preprocessing import preprocess_pipeline

class Codeword:
    def __init__(self):
        self.df, self.word_dict = self.read_subjectivity_clues()

    @staticmethod
    def read_subjectivity_clues():
        dicts = []
        path = os.path.join(os.path.dirname(__file__),
                            '../data/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff')
        with open(path) as f:
            for line in f:
                l = line.split()
                ls = [item for st in l for item in st.split('=')]
                ls[-1] = ls[-1].strip()
                i = iter(ls)
                dicts.append(dict(zip(i, i)))
        df = pd.DataFrame(dicts)
        df = Codeword.df_preprocess(df)
        d = dict(zip(df['word1'], df.index))
        return df, d

    @staticmethod
    def df_preprocess(df):
        df = df[(df['pos1'] == 'adj') | (df['pos1'] == 'anypos')]
        # p = 0
        # n = 0
        # xx = set()
        # [xx.add(preprocess_pipeline(word)[0]) for word in df['word1']]
        # for pp in df['priorpolarity']:
        #     if pp == 'positive':
        #         p += 1
        #     elif pp == 'negative':
        #         n += 1
        return df

    def get_codeword_tokens(self, tokens):
        codeword_tokens = []
        # s = 0
        for token in tokens:
            if token in self.word_dict:
                ix = self.word_dict[token]
                prior = self.df.get_value(ix, 'priorpolarity')
                if prior == 'positive':
                   codeword_tokens.append('GOODREVIEW')
                   # s += 1
                elif prior == 'negative':
                    codeword_tokens.append('BADREVIEW')
                    # s -= 1
        # if s >= 0:
        #     # codeword_tokens = ['GOODREVIEW' for v in range(s)]
        #     codeword_tokens = ['GOODREVIEW']
        # else:
        #     # codeword_tokens = ['BADREVIEW' for v in range(s*-1)]
        #     codeword_tokens = ['BADREVIEW']
        return codeword_tokens

if __name__ == '__main__':
    codeword = Codeword()
    codeword.get_codeword_tokens(["hello", "world", "hate"])