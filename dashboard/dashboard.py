import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the data
main_data_df = pd.read_csv("dashboard/main_data.csv")
main_data_df['order_purchase_timestamp'] = pd.to_datetime(main_data_df['order_purchase_timestamp'])

# Sidebar for navigation
st.sidebar.title("E-commerce Dashboard")
page = st.sidebar.selectbox("Pilih Visualisasi", ["Produk Terjual Banyak dan Sedikit", "Negara dengan Pembelian Terbanyak"])

# Produk Terjual Banyak dan Sedikit
if page == "Produk Terjual Banyak dan Sedikit":
    st.title("Produk yang Terjual Banyak dan Sedikit")

    product_sales_df = main_data_df.groupby('product_category_name_english').agg({
        'order_item_id': 'count',
        'price': 'sum'
    }).reset_index()

    product_sales_df.columns = ['product_category', 'total_sales', 'total_revenue']
    product_sales_df = product_sales_df.sort_values(by='total_sales', ascending=False)

    most_sold = product_sales_df.head(5)
    least_sold = product_sales_df.tail(5)

    # Visualisasi produk yang paling banyak terjual
    st.write("**Top 5 Produk yang Paling Banyak Terjual**")
    fig, ax = plt.subplots()
    sns.barplot(data=most_sold, x='product_category', y='total_sales', palette='Blues_d', ax=ax)
    ax.set_title("Top 5 Produk yang Paling Banyak Terjual", fontsize=18)
    ax.set_xlabel("Kategori Produk", fontsize=12)
    ax.set_ylabel("Jumlah Penjualan", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

    # Visualisasi produk yang paling sedikit terjual
    st.write("**Top 5 Produk yang Paling Sedikit Terjual**")
    fig, ax = plt.subplots()
    sns.barplot(data=least_sold, x='product_category', y='total_sales', palette='Oranges_d', ax=ax)
    ax.set_title("Top 5 Produk yang Paling Sedikit Terjual", fontsize=18)
    ax.set_xlabel("Kategori Produk", fontsize=12)
    ax.set_ylabel("Jumlah Penjualan", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

    # Visualisasi produk dengan pendapatan terbesar
    st.write("**Top 5 Produk dengan Pendapatan Terbanyak**")
    fig, ax = plt.subplots()
    sns.barplot(data=most_sold, x='product_category', y='total_revenue', palette='Greens_d', ax=ax)
    ax.set_title("Top 5 Produk dengan Pendapatan Terbanyak", fontsize=18)
    ax.set_xlabel("Kategori Produk", fontsize=12)
    ax.set_ylabel("Total Pendapatan", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

# Negara dengan Pembelian Terbanyak
elif page == "Negara dengan Pembelian Terbanyak":
    st.title("Negara dengan Pembelian Produk Terbanyak")

    if 'customer_state' not in main_data_df.columns:
        st.write("Kolom 'customer_state' tidak ditemukan.")
    else:
        state_sales_df = main_data_df.groupby('customer_state').agg({
            'order_id': 'count',
            'price': 'sum',
            'freight_value': 'sum'
        }).reset_index()

        state_sales_df['total_revenue'] = state_sales_df['price'] + state_sales_df['freight_value']
        state_sales_df = state_sales_df.sort_values(by='order_id', ascending=False)

        top_states_by_orders = state_sales_df.head(5)
        top_states_by_revenue = state_sales_df.sort_values(by='total_revenue', ascending=False).head(5)

        # Visualisasi negara/state dengan pembelian terbanyak
        st.write("**Top 5 Negara/State dengan Pembelian Terbanyak**")
        fig, ax = plt.subplots()
        sns.barplot(data=top_states_by_orders, x='customer_state', y='order_id', palette='Blues_d', ax=ax)
        ax.set_title("Top 5 Negara/State dengan Pembelian Terbanyak", fontsize=18)
        ax.set_xlabel("Negara/State", fontsize=12)
        ax.set_ylabel("Jumlah Pembelian", fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)

        # Visualisasi negara/state dengan pendapatan terbanyak
        st.write("**Top 5 Negara/State dengan Pendapatan Terbanyak**")
        fig, ax = plt.subplots()
        sns.barplot(data=top_states_by_revenue, x='customer_state', y='total_revenue', palette='Greens_d', ax=ax)
        ax.set_title("Top 5 Negara/State dengan Pendapatan Terbanyak", fontsize=18)
        ax.set_xlabel("Negara/State", fontsize=12)
        ax.set_ylabel("Total Pendapatan", fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        st.pyplot(fig)

        # Visualisasi jumlah pembelian per negara/state
        st.write("**Jumlah Pembelian per Negara/State**")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=state_sales_df, x='customer_state', y='order_id', palette='Purples_d', ax=ax)
        ax.set_title("Jumlah Pembelian per Negara/State", fontsize=18)
        ax.set_xlabel("Negara/State", fontsize=12)
        ax.set_ylabel("Jumlah Pembelian", fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        st.pyplot(fig)
