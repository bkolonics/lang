import streamlit as st
import string
import pandas as pd
from unidecode import unidecode
from collections import defaultdict
from st_keyup import st_keyup

user_input = ""
# input text
st.title("Language Detector")
st.caption("This app uses a simple bigram model to detect the language of a text. This may not be accurate for short texts, or texts that contain a lot of numbers or symbols. The model is trained on the [OSCAR Corpus](https://oscar-project.org/) dataset, which contains scrapped text from the web. The model is trained on the following languages: English, French, German.")
st.write("Enter some text below ")
user_input = st_keyup("Enter something", key="0", value=user_input)


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
df_de = pd.read_csv("output/de_df_large_norm.csv", index_col=0)

df_langs = {
    'french': df_fr,
    'english': df_en,
    'german': df_de
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
st.success(language)

baseline = df_langs_diff[language]

# table of scores
df_langs_diff = pd.DataFrame(df_langs_diff, index=[0])
df_langs_diff = df_langs_diff.T
df_langs_diff.columns = ['score']
df_langs_diff = df_langs_diff.sort_values(by='score', ascending=True)
df_langs_diff = df_langs_diff.reset_index()
df_langs_diff.columns = ['language', 'score']
df_langs_diff['score'] = "-" + ((df_langs_diff['score'] / baseline - 1) *100).astype(str)
df_langs_diff = df_langs_diff.iloc[1:]
st.write(df_langs_diff)