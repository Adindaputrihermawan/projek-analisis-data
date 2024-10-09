import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os
print(os.getcwd())

# Load the dataset
df1 = 'CustomerRFM_model.sav'
model = pickle.load(open(df1, 'rb'))

# Dashboard Title
st.title("Olist Customer Dashboard")

# Menggabungkan frekuensi pembelian dengan kota pelanggan
customer_loyalty = df1.groupby(['customer_unique_id', 'customer_city'])['customer_id'].count().reset_index()

# Memfilter pelanggan yang melakukan pembelian lebih dari satu kali (pelanggan loyal)
loyal_customers = customer_loyalty[customer_loyalty['customer_id'] > 1]

# Menghitung jumlah pelanggan loyal per kota
loyal_customers_per_city = loyal_customers.groupby('customer_city')['customer_unique_id'].count().reset_index()

# Menamai kolom
loyal_customers_per_city.columns = ['customer_city', 'loyal_customers']

# Menambahkan filter untuk memilih kota
selected_city = st.selectbox('Pilih Kota', df1['customer_city'].unique())

# Memfilter data berdasarkan kota yang dipilih
filtered_data = loyal_customers_per_city[loyal_customers_per_city['customer_city'] == selected_city]

# Menampilkan jumlah pelanggan loyal di kota yang dipilih
st.write(f"Pelanggan Loyal di {selected_city}: {filtered_data['loyal_customers'].values[0]}")

# Menghitung frekuensi pembelian per pelanggan unik
customer_purchase_freq = df1.groupby('customer_unique_id')['customer_id'].count()


# Menampilkan Histogram Pendapatan
st.write("Top 10 Customer Cities")
fig, ax = plt.subplots()
top_cities = df1['customer_city'].value_counts().nlargest(10) 
sns.barplot(x=top_cities.values, y=top_cities.index)
plt.title('Top 10 Customer Cities')
plt.xlabel('Number of Customers')
st.pyplot(fig)

st.write("Top 10 Customer State")
fig, ax = plt.subplots()
top_cities = df1['customer_state'].value_counts().nlargest(10) 
sns.barplot(x=top_cities.values, y=top_cities.index)
plt.title('Top 10 Customer State')
plt.xlabel('Number of Customers')
st.pyplot(fig)

df4 = pd.read_csv('dataset/olist_order_payments_dataset.csv')
payment_data = df4.groupby(by="payment_type").order_id.nunique().sort_values(ascending=False).reset_index()
payment_data = payment_data.rename(columns={"order_id": "unique_orders"})

# Streamlit App
st.title("Tipe Pembayaran")

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="unique_orders", y="payment_type", data=payment_data, palette="viridis")
plt.title('Tipe Pembayaran')
plt.xlabel('Number of Unique Orders')
plt.ylabel('Payment Type')
st.pyplot(fig)

df5 = pd.read_csv("dataset/olist_products_dataset.csv")
df6 = pd.read_csv("dataset/product_category_name_translation.csv")
df10 = pd.merge(
    left=df5,
    right=df6,
    how="left",
    left_on="product_category_name",
    right_on="product_category_name"
)

sum_order_items_df = df10.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False)
top_product = sum_order_items_df.head(5)

# Streamlit App
st.title("Top 5 Product Sales")

# Create the plot
fig, ax = plt.subplots(figsize=(18, 6))
colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="products", y="product_category_name_english", data=top_product, palette=colors)
plt.title('Top 5 Penjualan Tertinggi')
plt.xlabel('Number of Customers')
plt.ylabel('Product Category')

# Display plot in Streamlit
st.pyplot(fig)

df2 = pd.read_csv('dataset/olist_order_items_dataset.csv')
# Mengatur judul dashboard
st.title("Pendapatan tiap seller")
st.write("Analisis pendapatan tiap seller ")
# Filter seller secara interaktif
unique_sellers = df2['seller_id'].unique()
selected_seller = st.selectbox('Pilih Seller', unique_sellers)

# Memfilter data berdasarkan seller yang dipilih
filtered_df = df2[df2['seller_id'] == selected_seller]

# Overview Penjualan Dinamis
total_orders = filtered_df['order_id'].nunique()
total_items_sold = filtered_df['order_item_id'].count()
total_revenue = filtered_df['price'].sum()
total_freight = filtered_df['freight_value'].sum()

st.metric("Total Pesanan", total_orders)
st.metric("Total Item Terjual", total_items_sold)
st.metric("Total Pendapatan (BRL)", f"{total_revenue:,.2f}")
st.metric("Total Biaya Pengiriman (BRL)", f"{total_freight:,.2f}")

# Menampilkan Histogram Pendapatan
st.write("Distribusi Pendapatan")
fig, ax = plt.subplots()
sns.histplot(filtered_df['price'], bins=20, kde=True, color='blue', ax=ax)
ax.set_title('Distribusi Pendapatan Produk')
ax.set_xlabel('Harga Produk (BRL)')
ax.set_ylabel('Frekuensi')
st.pyplot(fig)


# Mengatur judul dashboard
st.title("Analisis RFM")
st.write("Analisis Recency, Frequency, dan Monetary dari data penjualan.")

# Memuat dataset
df2['shipping_limit_date'] = pd.to_datetime(df2['shipping_limit_date'], errors='coerce')

# Menghitung RFM
rfm_df = df2.groupby(by="order_id", as_index=False).agg({
    "shipping_limit_date": "max",  # Mengambil tanggal order terakhir
    "order_id": "nunique",  # Menghitung jumlah order (order_id)
    "price": "sum"  # Menghitung jumlah revenue yang dihasilkan
})

rfm_df.columns = ["customer_id", "max_order_timestamp", "monetary"]
rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"], errors='coerce')
rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date

# Menghitung recency
recent_date = df2["shipping_limit_date"].dt.date.max()
rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

# Menghitung frequency
rfm_df["frequency"] = df2.groupby("order_id")["order_id"].transform('nunique')

# Menghapus kolom max_order_timestamp
rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

# Tampilkan hasil RFM
st.subheader("Data RFM")
st.dataframe(rfm_df.head())

# Visualisasi RFM
st.subheader("Visualisasi RFM")
fig, ax = plt.subplots(1, 3, figsize=(18, 5))

# Visualisasi Recency
sns.histplot(rfm_df['recency'], bins=30, ax=ax[0], color='skyblue')
ax[0].set_title('Distribusi Recency')
ax[0].set_xlabel('Hari Sejak Pembelian Terakhir')
ax[0].set_ylabel('Jumlah Pelanggan')

# Visualisasi Frequency
sns.histplot(rfm_df['frequency'], bins=30, ax=ax[1], color='salmon')
ax[1].set_title('Distribusi Frequency')
ax[1].set_xlabel('Jumlah Order')
ax[1].set_ylabel('Jumlah Pelanggan')

# Visualisasi Monetary
sns.histplot(rfm_df['monetary'], bins=30, ax=ax[2], color='lightgreen')
ax[2].set_title('Distribusi Monetary')
ax[2].set_xlabel('Total Revenue')
ax[2].set_ylabel('Jumlah Pelanggan')

plt.tight_layout()
st.pyplot(fig)

# Menampilkan ringkasan statistik RFM
st.subheader("Ringkasan Statistik RFM")
st.write(rfm_df.describe())
