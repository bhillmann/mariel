import pandas as pd
import os

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
        d = dict(zip(df['word1'], df.index))
        return df, d

    def get_codeword_tokens(self, tokens):
        codeword_tokens = []
        codeword_dict = {}
        codeword_dict['negative'] = 'badword'
        codeword_dict['positive'] = 'goodword'
        for token in tokens:
            if token in self.word_dict:
                ix = self.word_dict[token]
                prior = self.df.irow(ix)['priorpolarity']
                if prior in codeword_dict:
                    codeword_tokens.append(codeword_dict[prior])
        return codeword_tokens

if __name__ == '__main__':
    codeword = Codeword()
    codeword.get_codeword_tokens(["hello", "world", "hate"])