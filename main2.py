from datasets import load_dataset
import string
import pandas as pd
from unidecode import unidecode
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

alphabet = string.ascii_lowercase + ' '

A = 0

names = [_ for _ in alphabet]
df = pd.DataFrame(A, index=names, columns=names)

dataset = load_dataset("oscar-corpus/OSCAR-2301",
                       token=True, # required
                        language="fr", 
                        streaming=True, # optional
                        split="train") # optional)

try:
    for d in tqdm(dataset, total=780000):
        #print(d["text"])
        phrase = d["text"]
        phrase = phrase.replace('\n', ' ')
        phrase = phrase.lower()
        phrase = unidecode(phrase)
        phrase = ''.join(e for e in phrase if e in alphabet)


        for i in range(len(phrase)-1):
            df.at[phrase[i], phrase[i+1]] += 1
except KeyboardInterrupt:
    plt.xticks(ticks=np.arange(len(alphabet)), labels=alphabet)
    plt.yticks(ticks=np.arange(len(alphabet)), labels=alphabet)
    plt.title("Digramme")
    plt.imshow(df, interpolation='none')
    plt.savefig("output/result_large.jpg")
    df.to_csv('output/df_large.csv', index=True, header=True, sep=',')




plt.xticks(ticks=np.arange(len(alphabet)), labels=alphabet)
plt.yticks(ticks=np.arange(len(alphabet)), labels=alphabet)
plt.title("Digramme")
plt.imshow(df, interpolation='none')
plt.savefig("output/result_large.jpg")
df.to_csv('output/df_large.csv', index=True, header=True, sep=',')