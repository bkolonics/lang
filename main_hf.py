from datasets import load_dataset
import string
import pandas as pd
from unidecode import unidecode
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

alphabet = string.ascii_lowercase + ' '

A = 0

names = [_ for _ in alphabet]
df = pd.DataFrame(A, index=names, columns=names)

dataset = load_dataset("oscar-corpus/OSCAR-2301",
                       token=True, # required
                        language="fr", 
                        streaming=True, # optional
                        split="train") # optional)

dataset = dataset.shuffle()
#dataset = dataset.take(1)
#dataset = [{"text" : "Quoique ce détail ne touche en aucune manière au fond même de ce quenous avons à raconter, il n'est peut-être pas inutile, ne fût-ce quepour être exact en tout, d'indiquer ici les bruits et les propos quiavaient couru sur son compte au moment où il était arrivé dans lediocèse. Vrai ou faux, ce qu'on dit des hommes tient souvent autant deplace dans leur vie et surtout dans leur destinée que ce qu'ils font. M.Myriel était fils d'un conseiller au parlement d'Aix; noblesse de robe.On contait de lui que son père, le réservant pour hériter de sa charge,l'avait marié de fort bonne heure, à dix-huit ou vingt ans, suivant unusage assez répandu dans les familles parlementaires. Charles Myriel,nonobstant ce mariage, avait, disait-on, beaucoup fait parler de lui. Ilétait bien fait de sa personne, quoique d'assez petite taille, élégant,gracieux, spirituel; toute la première partie de sa vie avait été donnéeau monde et aux galanteries. La révolution survint, les événements seprécipitèrent, les familles parlementaires décimées, chassées, traquées,se dispersèrent. M. Charles Myriel, dès les premiers jours de larévolution, émigra en Italie. Sa femme y mourut d'une maladie depoitrine dont elle était atteinte depuis longtemps. Ils n'avaient pointd'enfants. Que se passa-t-il ensuite dans la destinée de M. Myriel?L'écroulement de l'ancienne société française, la chute de sa proprefamille, les tragiques spectacles de 93, plus effrayants encorepeut-être pour les émigrés qui les voyaient de loin avec legrossissement de l'épouvante, firent-ils germer en lui des idées derenoncement et de solitude? Fut-il, au milieu d'une de ces distractionset de ces affections qui occupaient sa vie, subitement atteint d'un deces coups mystérieux et terribles qui viennent quelquefois renverser, enle frappant au coeur, l'homme que les catastrophes publiquesn'ébranleraient pas en le frappant dans son existence et dans safortune? Nul n'aurait pu le dire; tout ce qu'on savait, c'est que,lorsqu'il revint d'Italie, il était prêtre."}]
bigram_counts = defaultdict(int)
try:
    for d in tqdm(dataset, total=780000):
        phrase = d["text"]
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
    plt.xticks(ticks=np.arange(len(alphabet)), labels=alphabet)
    plt.yticks(ticks=np.arange(len(alphabet)), labels=alphabet)
    plt.title("Digramme")
    plt.imshow(df, interpolation='none')
    plt.savefig("output/result_large.jpg")
    df.to_csv('output/df_large.csv', index=True, header=True, sep=',')


for bigram, count in bigram_counts.items():
    df.loc[bigram[0], bigram[1]] = count
plt.xticks(ticks=np.arange(len(alphabet)), labels=alphabet)
plt.yticks(ticks=np.arange(len(alphabet)), labels=alphabet)
plt.title("Digramme")
plt.imshow(df, interpolation='none')
plt.savefig("output/result_large.jpg")
df.to_csv('output/df_large.csv', index=True, header=True, sep=',')