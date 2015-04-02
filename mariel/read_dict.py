import pandas as pd

dicts = []
with open('subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.tff') as f:
    for line in f:
        l = line.split()
        ls = [item for st in l for item in st.split('=')]
        ls[-1] = ls[-1].strip()
        i = iter(ls)
        dicts.append(dict(zip(i, i)))

df = pd.DataFrame(dicts)
print(df)
