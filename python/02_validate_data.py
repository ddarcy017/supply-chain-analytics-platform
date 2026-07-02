#%%
import pandas as pd

#%%
df = pd.read_csv("/Users/pann017/prac/supply-chain-analytics-platform/data/DataCoSupplyChain_staging.csv")
print(df.head)
print(df.shape)

# %%
print(df.dtypes)

# %% Change to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Shipping_Date"] = pd.to_datetime(df["Shipping_Date"])

# %% Checking missing vals
missing_sum = df.isna().sum()
missing_sum = missing_sum[missing_sum > 0].sort_values(ascending=False)

print(missing_sum)

# %%
df[
    df["Product_Description"].isna() |
    (df["Product_Description"] == " ")
]

# %% All Product_Description isna
df.drop(columns=["Product_Description"])

# %%
df[
    df["Product_Description"].isna() |
    (df["Product_Description"] == " ")
]

# %%
df.loc[
    df["Customer_Zipcode"].isna() |
    (df["Customer_Zipcode"] == " "),
    ["Order_State", "Customer_Zipcode"]
]
# %% All Product_Status == 0
df["Product_Status"].value_counts(dropna=False)
df = df.drop(columns=["Product_Status"])

# %%
duplicate_count = df.duplicated().sum()
print(f"Duplicate rows: {duplicate_count}")

# %%
df.duplicated(subset=["Order_ID"])

# %%
dup_order_ids = df.loc[
    df.duplicated(subset=["Order_ID"], keep=False),
    "Order_ID"
]
dup_orders = (
    df.loc[df["Order_ID"].isin(dup_order_ids),
           ["Order_ID",
            "Customer_ID",
            "Order_Date",
            "Order_Time",
            "Product_Name",
            "Customer_First_Name"]]
        .sort_values("Order_ID")
)

dup_orders

# %%
