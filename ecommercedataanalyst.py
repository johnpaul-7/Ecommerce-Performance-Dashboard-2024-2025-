import pandas as pd
import numpy as np
orders = pd.read_csv("C:\\Users\\john paul.d\\OneDrive\\Documents\\Data_analyst\\orders.csv")
order_items = pd.read_csv("C:\\Users\\john paul.d\\OneDrive\\Documents\\Data_analyst\\order_items.csv")
products = pd.read_csv("C:\\Users\\john paul.d\\OneDrive\\Documents\\Data_analyst\\products.csv")
users = pd.read_csv("C:\\Users\\john paul.d\\OneDrive\\Documents\\Data_analyst\\users.csv")
reviews = pd.read_csv("C:\\Users\\john paul.d\\OneDrive\\Documents\\Data_analyst\\reviews.csv")
events = pd.read_csv("C:\\Users\\john paul.d\\OneDrive\\Documents\\Data_analyst\\events.csv")

# Convert dates
orders['order_date'] = pd.to_datetime(orders['order_date'])

# Remove duplicates
orders.drop_duplicates(inplace=True)

# Missing values
orders.isnull().sum()

# Fix negative/invalid values
order_items = order_items[order_items['item_price'] > 0]
temp = order_items.merge(orders, on='order_id', how='left')
print(temp.columns)
# Step 1: Merge order_items + orders
df = order_items.merge(orders, on='order_id', how='left')

# Step 2: Fix duplicate user_id
df = df.rename(columns={'user_id_x': 'user_id'})
df = df.drop(columns=['user_id_y'])

# Step 3: Merge users
df = df.merge(users, on='user_id', how='left')

# Step 4: Merge products
df = df.merge(products, on='product_id', how='left')

df['month'] = df['order_date'].dt.to_period('M')
df['revenue'] = df['price'] * df['quantity']
df['revenue'] = df['item_total']
df['order_date'] = pd.to_datetime(df['order_date'])

monthly_sales = df.groupby('month')['revenue'].sum()
events['event_type'].value_counts()
customer_metrics = df.groupby('user_id')['revenue'].sum()
product_sales = df.groupby('product_name')['revenue'].sum()
reviews.groupby('rating')['order_id'].count()
df.to_csv("final_dataset.csv", index=False)
print(df.columns)
print(df.isnull().sum())

# Check duplicates
print(df.duplicated().sum())

# Check revenue correctness
print((df['item_total'] == df['quantity'] * df['item_price']).all())

print(np.isclose(df['item_total'], df['quantity'] * df['item_price']).all())
diff = df['item_total'] - (df['quantity'] * df['item_price'])
print(diff.abs().max())
df['item_total'] = (df['quantity'] * df['item_price']).round(2)
df['revenue'] = df['item_total']
df.to_csv("final_ecommerce_dataset.csv", index=False)
df.to_csv(r"C:\Users\john paul.d\OneDrive\Documents\Data_analyst\final_ecommerce_dataset.csv", index=False)
import os
print(os.getcwd())