# %%
import pandas as pd
import chardet as cd
file_path = "/Users/pann017/prac/supply-chain-analytics-platform/data/DataCoSupplyChainDataset.csv"

#%%
with open (file_path, "rb") as f:
    original_encoding = cd.detect(f.read())
print (original_encoding)

# %% Read file in latin1 encoding
df= pd.read_csv(file_path, encoding = "latin1")
print(df.head())

# %%
df.info()

# %% Standardize Column Titles
df.columns = (
    df.columns
    .str.strip()
    .str.title()
    .str.replace("Fname", "First_Name")
    .str.replace("Id", "ID")
    .str.replace("Lname", "Last_Name")
    .str.replace(" ","_")
    .str.replace(r"[()]", "", regex=True)
)

# %%
df["Order_Date_Dateorders"] = pd.to_datetime(df["Order_Date_Dateorders"])
df["Order_Date"] = df["Order_Date_Dateorders"].dt.date
df["Order_Time"] = df["Order_Date_Dateorders"].dt.time
df[["Order_Date", "Order_Time"]].head()

# %%
df["Shipping_Date_Dateorders"] = pd.to_datetime(df["Shipping_Date_Dateorders"])
df["Shipping_Date"] = df["Shipping_Date_Dateorders"].dt.date
df["Shipping_Time"] = df["Shipping_Date_Dateorders"].dt.time
df[["Shipping_Date", "Shipping_Time"]].head()

# %%
print((df["Order_Time"] == df["Shipping_Time"]).all())
df.drop(columns=["Order_Date_Dateorders", "Shipping_Date_Dateorders"], inplace=True)

# %%
df = df[sorted(df.columns)]

cols = df.columns.tolist()
cols.remove("Order_Time")
order_date_index = cols.index("Order_Date")
cols.insert(order_date_index + 1, "Order_Time")

cols.remove("Shipping_Time")
shipping_date_index = cols.index("Shipping_Date")
cols.insert(shipping_date_index + 1, "Shipping_Time")

cols.remove("Customer_Last_Name")
customer_fname_index = cols.index("Customer_First_Name")
cols.insert(customer_fname_index + 1, "Customer_Last_Name")

df = df[cols]
print(df.dtypes)

#%%
staging_path = "/Users/pann017/prac/supply-chain-analytics-platform/data/DataCoSupplyChain_staging.csv"
df.to_csv(staging_path, index=False, encoding="utf-8")
print("DataCoSupplyChain_staging.csv saved")
