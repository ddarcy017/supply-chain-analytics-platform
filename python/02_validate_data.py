#%% Read file
import pandas as pd

#%%
df = pd.read_csv("/Users/pann017/prac/supply-chain-analytics-platform/data/DataCoSupplyChain_staging.csv")
print(df.head)
print(df.shape)

# %% Check data types
print(df.dtypes)

# %% Change to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Shipping_Date"] = pd.to_datetime(df["Shipping_Date"])

# %% Change to boolean
df["Late_Delivery_Risk"].isin([0, 1]).all()
df["Late_Delivery_Risk"] = df["Late_Delivery_Risk"].astype(bool)

# %% Check missing vals
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
    df["Order_Zipcode"].isna() |
    (df["Order_Zipcode"] == " ")
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

# %% No duplicated Order
duplicate_count = df.duplicated().sum()
print(f"Duplicate rows: {duplicate_count}")

# %% Recheck duplicated
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

# %% Select all column title data types is int64
num_col = df.select_dtypes(include=["int64"]).columns
print(num_col)

# %%
df[["Order_Item_Cardprod_ID", "Product_Card_ID"]].head(5)

# %%
(df["Order_Item_Cardprod_ID"] == df["Product_Card_ID"]).all()

# %% Same value as Produce_Card_ID
df = df.drop(columns=["Order_Item_Cardprod_ID"])

# %%
(df["Days_For_Shipment_Scheduled"] == 0).any()

# %%
id_cols = [
    col
    for col in df.columns
    if col.endswith("ID")
]

for col in id_cols + ["Order_Item_Quantity"]:
    if (df[col] < 0).any():
        print(f"{col}: Invalid")

# %%
for column in ["Days_For_Shipment_Scheduled", "Days_For_Shipping_Real"]:
    if (df[column] < 0).any():
        print(f"{column}: Invalid")

# %%
df = df.rename(
    columns={
            "Days_For_Shipment_Scheduled": "Days_Shipping_Scheduled",
            "Days_For_Shipping_Real": "Days_Shipping_Actual"
    }
    )
# %%
