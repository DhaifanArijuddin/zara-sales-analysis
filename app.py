import streamlit as st
import pandas as pd
import plotly.express as px

# ===== Custom CSS untuk styling =====
st.markdown("""
    <style>
    /* Background utama */
    .stApp {
        background-color: #f9fafd;
        color: #0a1f44;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Sidebar style */
    .css-1d391kg {
        background-color: #e3f2fd;
        padding: 20px;
        border-radius: 8px;
    }
    /* Header judul */
    .css-18e3th9 h1 {
        color: #0a1f44;
        font-weight: 700;
    }
    /* Subheader style */
    .css-1v0mbdj {
        color: #0a1f44;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# =====================
# 📂 Load Dataset
# =====================
@st.cache_data
def load_data():
    return pd.read_csv("zara_cleaned.csv")

df = load_data()

df['scraped_at'] = pd.to_datetime(df['scraped_at'], errors='coerce')
df['year'] = df['scraped_at'].dt.year.fillna(2024).astype(int)

# =====================
# 🎯 Title
# =====================
st.title("📊 Zara Sales Analysis Dashboard")
st.markdown("Analisis penjualan Zara berdasarkan dataset yang telah diproses di Google Colab.")

# =====================
# 📌 Filter
# =====================
st.sidebar.header("🔍 Filter Data")

options_year = sorted(df['year'].unique())
default_year = options_year

selected_year = st.sidebar.multiselect(
    "Pilih Tahun",
    options_year,
    default=default_year
)

options_category = sorted(df['terms'].unique())
selected_category = st.sidebar.multiselect(
    "Pilih Kategori",
    options=options_category,
    default=options_category
)

filtered_df = df[
    (df['year'].isin(selected_year)) &
    (df['terms'].isin(selected_category))
]

# =====================
# 📊 Kategori Terlaris
# =====================
st.subheader("📊 Kategori Produk Berdasarkan Pendapatan")
category_sales = (
    filtered_df.groupby('terms')['Revenue']
    .sum()
    .reset_index()
    .sort_values(by='Revenue', ascending=False)
)

fig_category_sales = px.bar(
    category_sales,
    x='Revenue',
    y='terms',
    orientation='h',
    title="Total Pendapatan per Kategori Produk",
    text_auto='.2s',
    color_discrete_sequence=px.colors.sequential.Tealgrn
)
fig_category_sales.update_yaxes(categoryorder="total ascending")
st.plotly_chart(fig_category_sales)

# =====================
# 🛍️ Top Produk
# =====================

st.subheader("🏆 Top 10 Produk Terlaris")
top_products = (
    filtered_df.groupby('name')['Revenue']
    .sum()
    .reset_index()
    .sort_values(by='Revenue', ascending=False)
    .head(10)
)

fig_top_products = px.bar(
    top_products,
    x='Revenue',
    y='name',
    orientation='h',
    title="Top 10 Produk Terlaris",
    text_auto=True,
    color_discrete_sequence=px.colors.sequential.Teal
)
st.plotly_chart(fig_top_products) 

# =====================
# 📊 Distribusi Harga
# =====================
st.subheader("💰 Distribusi Harga Produk")
fig_price_dist = px.histogram(
    filtered_df,
    x='price',
    nbins=30,
    title="Distribusi Harga Produk Zara dalam USD",
    color_discrete_sequence=['#008080']
)
st.plotly_chart(fig_price_dist)

# =====================
# 📌 Tabel Data
# =====================
st.subheader("📄 Data Penjualan (Filtered)")
st.dataframe(filtered_df)

