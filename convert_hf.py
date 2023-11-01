import pandas as pd


df = pd.read_csv("output/df_large.csv", index_col=0)


df = df.div(df.sum(axis=1), axis=0)
print(df)
df.to_csv('output/df_large_norm.csv', index=True, header=True, sep=',')