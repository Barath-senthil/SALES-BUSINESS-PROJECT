import pandas as pd
import matplotlib
from sqlalchemy import distinct

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns


sales = pd.read_excel("python use.xlsx")
sales.columns = sales.columns.str.strip().str.lower()
sales['order_date'] = pd.to_datetime(sales['order_date'])

sales['total'] = sales['sales'] * sales['quantity']

# check negative or zero sales
print(sales[sales['sales'] <= 0])

# check duplicate based on order_id + product
print(sales.duplicated(subset=['order_id','product_name']).sum())

# percentage of missing values
print((sales.isnull().sum()/len(sales))*100)

# find columns with wrong datatype
print(sales.dtypes)

# unique values in each categorical column
for col in sales.select_dtypes(include='object'):
    print(col, sales[col].nunique())

# fill missing numeric with median
sales['sales'].fillna(sales['sales'].median(), inplace=True)

# fill missing categorical with mode
sales['city'].fillna(sales['city'].mode()[0], inplace=True)

# remove outliers using iqr
q1 = sales['sales'].quantile(0.25)
q3 = sales['sales'].quantile(0.75)
iqr = q3 - q1
sales = sales[(sales['sales'] >= q1 - 1.5*iqr) & (sales['sales'] <= q3 + 1.5*iqr)]

# standardize text columns
for col in sales.select_dtypes(include='object'):
    sales[col] = sales[col].str.strip().str.lower()

# drop rows with critical nulls
sales = sales.dropna(subset=['order_id','sales'])

# create month & year
sales['month'] = sales['order_date'].dt.month
sales['year'] = sales['order_date'].dt.year

# average order value per order
aov = sales.groupby('order_id')['total'].sum().mean()
print(aov)

# order size category
sales['order_size'] = pd.cut(sales['total'],
                            bins=[0,5000,20000,999999],
                            labels=['small','medium','large'])

# repeat customer
sales['repeat_customer'] = sales.duplicated(subset='customer_name', keep=False)

# revenue share per category
cat_share = sales.groupby('category')['total'].sum()
print(cat_share / cat_share.sum())

# top 5 cities by revenue
print(sales.groupby('city')['total'].sum().sort_values(ascending=False).head())

# bottom 5 products
print(sales.groupby('product_name')['total'].sum().sort_values().head())

# monthly trend
print(sales.groupby('month')['total'].sum())

# most profitable category (assuming profit exists)
# print(sales.groupby('category')['profit'].sum().idxmax())

# highest avg order value by city
print(sales.groupby('city')['total'].mean().idxmax())

# customers with >5 orders
print(sales['customer_name'].value_counts()[lambda x: x>5])

# most frequent product
print(sales['product_name'].mode()[0])

# payment mode distribution
print(sales['payment_mode'].value_counts(normalize=True)*100)

# peak sales month
print(sales.groupby('month')['total'].sum().idxmax())

# day of week analysis
sales['day'] = sales['order_date'].dt.day_name()
print(sales.groupby('day')['total'].sum())

import matplotlib.pyplot as plt

# monthly trend
sales.groupby('month')['total'].sum().plot()
plt.show()

# category sales
sales.groupby('category')['total'].sum().plot(kind='bar')
plt.show()

# correlation
print(sales[['sales','quantity','total']].corr())

# city contributing highest % revenue
city_rev = sales.groupby('city')['total'].sum()
print((city_rev / city_rev.sum()).sort_values(ascending=False).head())

# worst performing product
print(sales.groupby('product_name')['total'].sum().idxmin())

# which city contributes highest revenue
city_sales = sales.groupby('city')['total'].sum().sort_values(ascending=False)
plt.figure()
city_sales.plot(kind='bar')
plt.title("sales by city")
plt.show()

# how sales change month-wise (trend)
monthly = sales.groupby('month')['total'].sum()

plt.figure()
plt.plot(monthly)
plt.title("monthly sales trend")
plt.show()

# which category performs best
cat = sales.groupby('category')['total'].sum().reset_index()

plt.figure()
sns.barplot(data=cat, x='category', y='total')
plt.title("category sales")
plt.show()

# is there relationship between quantity and sales
plt.figure()
sns.scatterplot(data=sales, x='quantity', y='sales')
plt.title("quantity vs sales")
plt.show()

# are there outliers in sales
plt.figure()
sns.boxplot(x=sales['sales'])
plt.title("sales outliers")
plt.show()
sales projeect
