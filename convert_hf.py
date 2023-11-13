import pandas as pd

def normalize_and_save():
    df = pd.read_csv("output/df_large.csv", index_col=0)
    sum_df = df.values.sum()
    df = df.map(lambda x: (x * 100 / sum_df).round(2))
    df.to_csv('output/df_large_norm.csv', index=True, header=True, sep=',')

if __name__ == "__main__":
    normalize_and_save()