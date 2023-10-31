import pandas as pd
import string
from unidecode import unidecode
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

alphabet = string.ascii_lowercase + ' '



A = 0

names = [_ for _ in alphabet]
df = pd.DataFrame(A, index=names, columns=names)

with open("les_miserable.txt", 'r') as fr:
    phrase = fr.read().replace('\n', ' ')
    phrase = phrase.lower()
    phrase = unidecode(phrase)
    phrase = ''.join(e for e in phrase if e in alphabet)


    for i in tqdm(range(len(phrase)-1)):
        df.at[phrase[i], phrase[i+1]] += 1


    plt.xticks(ticks=np.arange(len(alphabet)), labels=alphabet)
    plt.yticks(ticks=np.arange(len(alphabet)), labels=alphabet)
    plt.imshow(df, interpolation='none')
    plt.show()


df.to_csv('df.csv', index=True, header=True, sep=',')