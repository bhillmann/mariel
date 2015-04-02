import pandas as pd
import os

def read_subjectivity_clues():
    dicts = []
    path = os.path.join(os.path.dirname(__file__), '../data/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff')
    with open(path) as f:
        for line in f:
            l = line.split()
            ls = [item for st in l for item in st.split('=')]
            ls[-1] = ls[-1].strip()
            i = iter(ls)
            dicts.append(dict(zip(i, i)))

    df = pd.DataFrame(dicts)
    print(df)

if __name__ == '__main__':
    read_subjectivity_clues()