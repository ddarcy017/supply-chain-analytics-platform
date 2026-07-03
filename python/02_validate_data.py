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

# %%
rep_cols = [
    col
    for col in df.columns
    if df [col].nunique(dropna=False) == 1
]

print(rep_cols)
df.loc[:, rep_cols].head(5)

# %%
df = df.drop(columns=["Product_Description"])

# %% No duplicated Order
dup_row = df.duplicated().sum()
print(f"Duplicate rows: {dup_row}")

# %% Check duplicated columns
dup_cols = []

for i in range(len(df.columns)):
    for j in range(i + 1, len(df.columns)):
        if df.iloc[:, i].equals(df.iloc[:, j]):
            dup_cols.append((df.columns[i], df.columns[j]))

print(dup_cols)

# %% Double check 
dup_pairs = [
    ("Order_Profit_Per_Order", "Benefit_Per_Order"),
    ("Order_Item_Total", "Sales_Per_Customer"),
    ("Category_ID", "Product_Category_ID"),
    ("Customer_ID", "Order_Customer_ID"),
    ("Product_Card_ID", "Order_Item_Cardprod_ID"),
    ("Product_Price", "Order_Item_Product_Price"),
]

# %% Delete duplicated cols
drop_cols = []

for left, right in dup_pairs:
    if df[left].equals(df[right]):
        drop_cols.append(right)
        print(f"Dropped: {right}")
df = df.drop(columns=drop_cols)

# %% Rename Columns
df = df.rename(
    columns={
    "Order_Profit_Per_Order" : "Order_Profit",
    "Days_For_Shipment_Scheduled": "Shipping_Days_Scheduled",
    "Days_For_Shipping_Real": "Shipping_Days_Actual",
    "Order_Item_Discount" : "Order_Item_Discount_Value"
    }
)

# %% Check duplicate by Order_ID
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
num_cols = df.select_dtypes(include=["int64"]).columns
print(num_cols)

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
for column in ["Shipping_Days_Scheduled", "Shipping_Days_Actual"]:
    if (df[column] < 0).any():
        print(f"{column}: Invalid")

# %%
fl_cols = df.select_dtypes(include=["float64"]).columns
print(fl_cols)

# %%
df.loc[:, ['Customer_Zipcode', 'Latitude', 'Longitude',
       'Order_Item_Discount_Value', 'Order_Item_Discount_Rate',
       'Order_Item_Profit_Ratio', 'Sales', 'Order_Item_Total', 'Order_Profit',
       'Order_Zipcode', 'Product_Price'
            ]].head(5)

# %% Change zipcode to type string
df["Customer_Zipcode"] = df["Customer_Zipcode"].astype("string")
df["Order_Zipcode"] = df["Order_Zipcode"].astype("string")

# %% Latitude, Longtitue all valid
for col, min, max in [
    ("Latitude", -90, 90),
    ("Longitude", -180, 180),
    ("Order_Item_Discount_Rate", 0, 1)
]:
    if (~df[col].between(min,max)).any():
        print(f"{col}: Invalid")

# %%
for col in ["Sales","Order_Item_Total", "Product_Price"]:
    if (df[col] <= 0).any():
        print(f"{col}: Invalid")
        
# %%
for col in ["Order_Item_Discount_Value"]:
    if (df[col] < 0).any():
        print(f"{col}: Invalid")
        
# %%
