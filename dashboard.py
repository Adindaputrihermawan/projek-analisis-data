import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle


# Load the model
filename = 'CustomerRFM_model.sav'
model = pickle.load(open(filename, 'rb'))

# Convert model into DataFrame
df1 = pd.DataFrame(model)

# Cek kolom yang ada dalam df1
st.write("Kolom yang ada dalam DataFrame:", df1.columns.tolist())

# Menggabungkan frekuensi pembelian dengan kota pelanggan
if 'customer_unique_id' in df1.columns and 'customer_city' in df1.columns and 'customer_id' in df1.columns:
    customer_loyalty = df1.groupby(['customer_unique_id', 'customer_city'])['customer_id'].count().reset_index()
else:
    st.error("Kolom 'customer_unique_id', 'customer_city', atau 'customer_id' tidak ditemukan dalam DataFrame.")
    st.stop()

# Memfilter pelanggan yang melakukan pembelian lebih dari satu kali (pelanggan loyal)
loyal_customers = customer_loyalty[customer_loyalty['customer_id'] > 1]

# Menghitung jumlah pelanggan loyal per kota
loyal_customers_per_city = loyal_customers.groupby('customer_city')['customer_unique_id'].count().reset_index()
loyal_customers_per_city.columns = ['customer_city', 'loyal_customers']

# Menambahkan filter untuk memilih kota
selected_city = st.selectbox('Pilih Kota', df1['customer_city'].unique())

# Memfilter data berdasarkan kota yang dipilih
filtered_data = loyal_customers_per_city[loyal_customers_per_city['customer_city'] == selected_city]

# Menampilkan jumlah pelanggan loyal di kota yang dipilih
st.write(f"Pelanggan Loyal di {selected_city}: {filtered_data['loyal_customers'].values[0]}")

# Menampilkan Histogram Pendapatan
st.write("Top 10 Customer Cities")
fig, ax = plt.subplots()
top_cities = df1['customer_city'].value_counts().nlargest(10)
sns.barplot(x=top_cities.values, y=top_cities.index, ax=ax)
plt.title('Top 10 Customer Cities')
plt.xlabel('Number of Customers')
st.pyplot(fig)

st.write("Top 10 Customer State")
fig, ax = plt.subplots()
top_states = df1['customer_state'].value_counts().nlargest(10)
sns.barplot(x=top_states.values, y=top_states.index, ax=ax)
plt.title('Top 10 Customer States')
plt.xlabel('Number of Customers')
st.pyplot(fig)

# Tipe Pembayaran
st.title("Tipe Pembayaran")

# Simulasi data pembayaran, karena tidak memuat CSV
# Anda bisa mengganti ini dengan data yang sesuai dari df1 jika ada
payment_data = df1.groupby('payment_type')['customer_id'].count().reset_index()
payment_data.columns = ['payment_type', 'unique_orders']

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="unique_orders", y="payment_type", data=payment_data, palette="viridis", ax=ax)
plt.title('Tipe Pembayaran')
plt.xlabel('Number of Unique Orders')
plt.ylabel('Payment Type')
st.pyplot(fig)

# Menampilkan Top 5 Product Sales
st.title("Top 5 Product Sales")

# Simulasi data produk, karena tidak memuat CSV
# Anda bisa mengganti ini dengan data yang sesuai dari df1 jika ada
top_product = df1['product_category_name'].value_counts().nlargest(5).reset_index()
top_product.columns = ['product_category_name', 'products']

# Create the plot
fig, ax = plt.subplots(figsize=(18, 6))
colors = ["#068DA9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(x="products", y="product_category_name", data=top_product, palette=colors, ax=ax)
plt.title('Top 5 Penjualan Tertinggi')
plt.xlabel('Number of Customers')
plt.ylabel('Product Category')
st.pyplot(fig)

# Mengatur judul dashboard
st.title("Pendapatan tiap seller")
st.write("Analisis pendapatan tiap seller ")

# Simulasi analisis pendapatan seller
unique_sellers = df1['seller_id'].unique()
selected_seller = st.selectbox('Pilih Seller', unique_sellers)

# Memfilter data berdasarkan seller yang dipilih
filtered_df = df1[df1['seller_id'] == selected_seller]

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

# Menghitung RFM
rfm_df = df1.groupby(by="order_id", as_index=False).agg({
    "shipping_limit_date": "max",  # Mengambil tanggal order terakhir
    "order_id": "nunique",  # Menghitung jumlah order (order_id)
    "price": "sum"  # Menghitung jumlah revenue yang dihasilkan
})

rfm_df.columns = ["customer_id", "max_order_timestamp", "monetary"]
rfm_df["max_order_timestamp"] = pd.to_datetime(rfm_df["max_order_timestamp"], errors='coerce')
rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date

# Menghitung recency
recent_date = df1["shipping_limit_date"].dt.date.max()
rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)

# Menghitung frequency
rfm_df["frequency"] = df1.groupby("order_id")["order_id"].transform('nunique')

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
