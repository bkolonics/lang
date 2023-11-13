import streamlit as st
from datasets import load_dataset
import string
import pandas as pd
from unidecode import unidecode
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from st_keyup import st_keyup

user_input = ""
# input text
user_input = st_keyup("Enter a value", key="0", value=user_input)


# get bigrams

alphabet = string.ascii_lowercase + ' '

A = 0

names = [_ for _ in alphabet]
df = pd.DataFrame(A, index=names, columns=names)

dataset = user_input

bigram_counts = defaultdict(int)
try:
    phrase = dataset
    phrase = phrase.replace('\n', ' ')
    phrase = phrase.lower()
    phrase = unidecode(phrase)
    phrase = ''.join(e for e in phrase if e in alphabet or e == ' ')

    for i in range(0, len(phrase) - 1, 2):
        if i+1 < len(phrase):
            bigram = (phrase[i], phrase[i+1])
            bigram_counts[bigram] += 1


except KeyboardInterrupt:
    # put bigram_counts into a dataframe
    for bigram, count in bigram_counts.items():
        df.loc[bigram[0], bigram[1]] = count


for bigram, count in bigram_counts.items():
    df.loc[bigram[0], bigram[1]] = count

# compare bigrams to bigrams in different languages

# load dataset
df_fr = pd.read_csv("output/fr_df_large_norm.csv", index_col=0)
df_en = pd.read_csv("output/en_df_large_norm.csv", index_col=0)

df_langs = {
    'fr': df_fr,
    'en': df_en
}
df_langs_diff = {}
# compare bigrams to bigrams in different languages


for lang, df_lang in df_langs.items():
    df_comp = df_lang - df
    df_comp = df_comp.fillna(0)
    df_comp = df_comp.abs()
    df_comp = df_comp.sum().sum()
    df_langs_diff[lang] = df_comp


#print(df_langs_diff)

# score each language

language = min(df_langs_diff, key=df_langs_diff.get)

# return language with highest score
print("Your text is most likely in the language: ")
print(language)
st.write("Your text is most likely in the language: ")
st.write(language)
