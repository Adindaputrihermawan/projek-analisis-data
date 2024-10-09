import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


# Load the pre-trained model from 'CustomerRFM_model.sav'
filename = 'CustomerRFM_model.sav'
try:
    model = pickle.load(open(filename, 'rb'))
    st.success(f"Model '{filename}' berhasil dimuat.")
except FileNotFoundError:
    st.error(f"File model '{filename}' tidak ditemukan.")
    st.stop()

# Dashboard Title
st.title("Olist Customer Dashboard")

# Misalkan data pelanggan dimasukkan sebagai input manual atau dari sumber lain (bukan CSV)
st.header("Masukkan Data Pelanggan")

# Input fitur dari pengguna
customer_id = st.text_input("Masukkan Customer ID")
recency = st.number_input("Masukkan Recency (hari sejak pembelian terakhir)", min_value=0)
frequency = st.number_input("Masukkan Frequency (jumlah pembelian)", min_value=1)
monetary = st.number_input("Masukkan Monetary (total pendapatan)", min_value=0.0)

# Memastikan semua input sudah diberikan
if st.button("Prediksi Kategori Pelanggan"):
    if customer_id and recency >= 0 and frequency > 0 and monetary >= 0:
        # Membuat dataframe dari input pengguna
        input_data = pd.DataFrame({
            "customer_id": [customer_id],
            "recency": [recency],
            "frequency": [frequency],
            "monetary": [monetary]
        })

        # Menampilkan input data
        st.write("Data Pelanggan:")
        st.dataframe(input_data)

        # Melakukan prediksi dengan model
        prediction = model.predict(input_data[['recency', 'frequency', 'monetary']])

        # Menampilkan hasil prediksi
        st.subheader(f"Prediksi Kategori Pelanggan: {prediction[0]}")
    else:
        st.error("Pastikan semua input sudah terisi dengan benar.")

# Bagian untuk menampilkan distribusi data RFM (misalkan dari model atau data internal)
st.subheader("Distribusi Data RFM (Recency, Frequency, Monetary)")

# Simulasi data untuk distribusi (untuk visualisasi)
simulated_rfm_data = pd.DataFrame({
    "recency": [30, 45, 12, 60, 5, 20, 15],
    "frequency": [3, 5, 2, 1, 10, 4, 3],
    "monetary": [300, 500, 150, 100, 700, 350, 200]
})

# Visualisasi histogram untuk Recency, Frequency, dan Monetary
fig, ax = plt.subplots(1, 3, figsize=(18, 5))

# Recency distribution
sns.histplot(simulated_rfm_data['recency'], bins=30, ax=ax[0], color='skyblue')
ax[0].set_title('Distribusi Recency')
ax[0].set_xlabel('Hari Sejak Pembelian Terakhir')
ax[0].set_ylabel('Jumlah Pelanggan')

# Frequency distribution
sns.histplot(simulated_rfm_data['frequency'], bins=30, ax=ax[1], color='salmon')
ax[1].set_title('Distribusi Frequency')
ax[1].set_xlabel('Jumlah Pembelian')
ax[1].set_ylabel('Jumlah Pelanggan')

# Monetary distribution
sns.histplot(simulated_rfm_data['monetary'], bins=30, ax=ax[2], color='lightgreen')
ax[2].set_title('Distribusi Monetary')
ax[2].set_xlabel('Total Pendapatan')
ax[2].set_ylabel('Jumlah Pelanggan')

# Menampilkan plot
st.pyplot(fig)

# ----------- Tambahan Visualisasi Menarik untuk Dashboard ----------- #

# Misalkan kita memiliki dataset produk yang telah di-load ke dalam dataframe df_products
df_products = pd.DataFrame({
    'product_category_name_english': ['bed bath table', 'health beauty', 'sports leisure', 'furniture decor', 'computers accessories'],
    'sales': [3029, 2001, 1580, 1250, 980]
})

st.subheader("Top 5 Produk dengan Penjualan Tertinggi")

# Bar plot menggunakan Plotly
fig = px.bar(df_products, x='product_category_name_english', y='sales', 
             color='sales', labels={'product_category_name_english': 'Kategori Produk', 'sales': 'Jumlah Penjualan'},
             title='Top 5 Produk dengan Penjualan Tertinggi')
st.plotly_chart(fig)

# ---------- Visualisasi Tipe Pembayaran yang Sering Digunakan ---------- #
df_payments = pd.DataFrame({
    'payment_type': ['credit_card', 'boleto', 'voucher', 'debit_card'],
    'unique_orders': [58770, 19784, 5772, 1523]
})

st.subheader("Tipe Pembayaran yang Paling Sering Digunakan")

fig = px.pie(df_payments, names='payment_type', values='unique_orders', 
             title='Distribusi Tipe Pembayaran yang Sering Digunakan')
st.plotly_chart(fig)

# ---------- Visualisasi Distribusi Pelanggan Berdasarkan Kota ---------- #
df_customers = pd.DataFrame({
    'customer_city': ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Brasília', 'Curitiba'],
    'customer_count': [1574, 1234, 987, 654, 432]
})

st.subheader("Distribusi Pelanggan Berdasarkan Kota")

fig = px.bar(df_customers, x='customer_city', y='customer_count', 
             title='Top 5 Kota dengan Jumlah Pelanggan Terbanyak', 
             labels={'customer_city': 'Kota', 'customer_count': 'Jumlah Pelanggan'})
st.plotly_chart(fig)
