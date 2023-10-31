import pandas as pd
import string
from unidecode import unidecode
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os, glob

alphabet = string.ascii_lowercase + ' '

path = 'datasets'

A = 0

names = [_ for _ in alphabet]
df = pd.DataFrame(A, index=names, columns=names)

for filename in glob.glob(os.path.join(path, '*.txt')):
    with open(os.path.join(os.getcwd(), filename), 'r') as fr:
        phrase = fr.read().replace('\n', ' ')
        phrase = phrase.lower()
        phrase = unidecode(phrase)
        phrase = ''.join(e for e in phrase if e in alphabet)


        for i in tqdm(range(len(phrase)-1)):
            df.at[phrase[i], phrase[i+1]] += 1



plt.xticks(ticks=np.arange(len(alphabet)), labels=alphabet)
plt.yticks(ticks=np.arange(len(alphabet)), labels=alphabet)
plt.title("Digramme de"+ filename)
plt.imshow(df, interpolation='none')
plt.savefig("output/result.jpg")
df.to_csv('output/df.csv', index=True, header=True, sep=',')