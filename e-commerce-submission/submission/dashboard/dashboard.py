# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Judul Dashboard
st.title("📊 E-Commerce Public Analysis Dashboard")
st.markdown("by Paul David Djukardi")

# Load Data (Pastikan file dataset ada di direktori yang sesuai)
@st.cache_data
def load_data():
    # Sesuaikan path dengan struktur direktori Anda
    dataset_direktori = 'submission/dataset/'
    
    # Debugging: Print the path being used
    st.write(f"Looking for dataset in: {dataset_direktori}")
    
    # Load dataset
    df_customer = pd.read_csv(f"{dataset_direktori}/customers_dataset.csv")
    df_items = pd.read_csv(f"{dataset_direktori}/order_items_dataset.csv")
    df_payments = pd.read_csv(f"{dataset_direktori}/order_payments_dataset.csv")
    df_orders = pd.read_csv(f"{dataset_direktori}/orders_dataset.csv")
    
    # Data wrangling untuk analisis kota
    df_orders_dan_customer = pd.merge(df_orders, df_customer, on='customer_id')
    data_gabungan_final = pd.merge(df_orders_dan_customer, df_items, on='order_id')
    
    return data_gabungan_final, df_payments

try:
    data_gabungan, df_payments = load_data()
except FileNotFoundError as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# Tab untuk Organisasi Konten
tab1, tab2 = st.tabs(["📍 Analisis Kota", "💳 Analisis Pembayaran"])

with tab1:
    st.header("Tren Pembelian per Kota")
    
    # Hitung total transaksi per kota
    total_transaksi_per_kota = data_gabungan.groupby('customer_city', as_index=False)['price'].sum()
    top_kota = total_transaksi_per_kota.sort_values(by='price', ascending=False).head(10)
    bottom_kota = total_transaksi_per_kota.sort_values(by='price', ascending=True).head(10)

    # Visualisasi
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Kota (Nilai Pembelian Tertinggi)")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='price', y='customer_city', data=top_kota, palette='viridis', ax=ax1)
        ax1.set_title("Top 10 Kota dengan Total Nilai Pembelian Tertinggi")
        ax1.set_xlabel("Total Nilai Pembelian (R$)")
        ax1.set_ylabel("Kota")
        st.pyplot(fig1)
    
    with col2:
        st.subheader("Top 10 Kota (Nilai Pembelian Terendah)")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='price', y='customer_city', data=bottom_kota, palette='viridis', ax=ax2)
        ax2.set_title("Top 10 Kota dengan Total Nilai Pembelian Terendah")
        ax2.set_xlabel("Total Nilai Pembelian (R$)")
        ax2.set_ylabel("Kota")
        st.pyplot(fig2)

with tab2:
    st.header("Analisis Metode Pembayaran")
    
    # Hitung frekuensi dan rata-rata
    frekuensi_metode = df_payments['payment_type'].value_counts()
    mean_metode = df_payments.groupby('payment_type')['payment_value'].mean().reset_index()
    total_metode = df_payments.groupby('payment_type')['payment_value'].sum().reset_index()
    
    # Visualisasi 1: Frekuensi Metode Pembayaran
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Frekuensi Metode Pembayaran")
        fig3, ax3 = plt.subplots(figsize=(8, 8))
        ax3.pie(frekuensi_metode, labels=frekuensi_metode.index, autopct='%1.1f%%')
        ax3.set_title("Distribusi Metode Pembayaran")
        st.pyplot(fig3)
    
    with col2:
        st.subheader("Rata-Rata Nilai Pembayaran")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.barplot(x='payment_type', y='payment_value', data=mean_metode, palette='viridis', ax=ax4)
        ax4.set_title("Rata-Rata Nilai Pembayaran per Metode")
        ax4.set_xlabel("Metode Pembayaran")
        ax4.set_ylabel("Rata-Rata Nilai (R$)")
        st.pyplot(fig4)
    
    # Visualisasi 2: Relevansi Metode Pembayaran dengan Besaran Transaksi
    st.subheader("Relevansi Metode Pembayaran dengan Besaran Transaksi")
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x='payment_type', 
        y='payment_value', 
        data=total_metode,  # Gunakan total nilai transaksi
        palette='viridis', 
        ax=ax5
    )
    ax5.set_title("Total Nilai Transaksi per Metode Pembayaran")
    ax5.set_xlabel("Metode Pembayaran")
    ax5.set_ylabel("Total Nilai (R$)")
    st.pyplot(fig5)

# Catatan
st.markdown("---")
st.caption("""
**Catatan:**
- Pastikan semua file dataset telah ditempatkan di folder `submission/dataset/`.
- Dashboard ini menampilkan analisis tren pembelian per kota dan pola penggunaan metode pembayaran.
""")