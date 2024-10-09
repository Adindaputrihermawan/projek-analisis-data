import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Load RFM model
filename = 'CustomerRFM_model.sav'
rfm_df = pickle.load(open(filename, 'rb'))

# Title of the application
st.title("Analisis Data E-Commerce Olist")

# Menu selection
options = st.sidebar.selectbox("Pilih Analisis:", ["Item Terlaris", "Demografi Pelanggan", "Tipe Pembayaran", "RFM Analysis"])

if options == "Item Terlaris":
    st.header("Item dengan Tingkat Penjualan Tertinggi")
    
    # Calculate top selling items
    sum_order_items_df = df2.groupby("product_id")["order_id"].count().reset_index()
    sum_order_items_df = sum_order_items_df.sort_values(by="order_id", ascending=False).head(5)
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="order_id", y="product_id", data=sum_order_items_df, palette="viridis")
    plt.title('Top 5 Penjualan Tertinggi')
    plt.xlabel('Jumlah Penjualan')
    plt.ylabel('ID Produk')
    st.pyplot(fig)

elif options == "Demografi Pelanggan":
    st.header("Demografi Pelanggan")
    
    # Customer city distribution
    top_cities = df1['customer_city'].value_counts().nlargest(10)
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_cities.values, y=top_cities.index)
    plt.title('Top 10 Kota Pelanggan')
    plt.xlabel('Jumlah Pelanggan')
    st.pyplot(fig)

elif options == "Tipe Pembayaran":
    st.header("Tipe Pembayaran yang Sering Digunakan")
    
    payment_data = df4.groupby(by="payment_type").order_id.nunique().sort_values(ascending=False).reset_index()
    payment_data = payment_data.rename(columns={"order_id": "unique_orders"})
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="unique_orders", y="payment_type", data=payment_data, palette="viridis")
    plt.title('Jumlah Pesanan Unik per Tipe Pembayaran')
    plt.xlabel('Jumlah Pesanan Unik')
    plt.ylabel('Tipe Pembayaran')
    st.pyplot(fig)

elif options == "RFM Analysis":
    st.header("Analisis RFM")
    
    st.write(rfm_df)

# Footer
st.write("Aplikasi ini menggunakan dataset Olist Brazilian E-Commerce dan melakukan analisis untuk memahami pola pembelian.")
