import pandas as pd

file_path = "/Users/pann017/prac/supply-chain-analytics-platform/data/DataCoSupplyChainDataset.csv"

df = pd.read_csv(file_path, encoding="latin1")

print(df.head())
print(df.shape)