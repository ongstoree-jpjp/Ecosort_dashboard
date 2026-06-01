import streamlit as st
import pandas as pd
import plotly.express as px

# KONFIGURASI HALAMAN

st.set_page_config(
    page_title="EcoSort Prepocessing Dashboard",
    page_icon="♻️",
    layout="wide"
)

# LOAD DATA

df = pd.read_csv("dataset_info.csv")

# Ringkasan per kelas
summary_df = (
    df["kelas"]
    .value_counts()
    .reset_index()
)

summary_df.columns = ["Kelas", "Jumlah"]

# Ringkasan per split
split_df = (
    df["split"]
    .value_counts()
    .reset_index()
)

split_df.columns = ["Split", "Jumlah"]

# KPI
total_data = len(df)
total_kelas = df["kelas"].nunique()

imbalance_ratio = round(
    summary_df["Jumlah"].max() /
    summary_df["Jumlah"].min(),
    2
)

terbesar = summary_df.loc[
    summary_df["Jumlah"].idxmax()
]

terkecil = summary_df.loc[
    summary_df["Jumlah"].idxmin()
]

# SIDEBAR

st.sidebar.title("EcoSort Dashboard")

menu = st.sidebar.radio(
    "Navigasi",
    [
        "Overview",
        "Distribusi Dataset",
        "Galeri Sampah",
        "Insight Dataset",
        "Kesimpulan"
    ]
)

# OVERVIEW

if menu == "Overview":

    st.title("Dashboard Analisis Dataset EcoSort")

    st.markdown("""
    Dashboard ini menampilkan hasil preprocessing
    dataset klasifikasi sampah EcoSort.
    """)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Gambar",
        f"{total_data:,}"
    )

    col2.metric(
        "Jumlah Kelas",
        total_kelas
    )

    col3.metric(
        "Imbalance Ratio",
        imbalance_ratio
    )

    col4.metric(
        "Resolusi",
        "224×224"
    )

    st.divider()

    st.subheader(" Statistik Dataset")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Lebar Gambar",
        int(df["width"].mode()[0])
    )

    c2.metric(
        "Tinggi Gambar",
        int(df["height"].mode()[0])
    )

    c3.metric(
        "Format",
        df["format"].mode()[0]
    )

    st.divider()

    st.subheader("Status Dataset")

    st.progress(100)

    st.success("""
    Cleaning Dataset

    Resize 224x224

    Standarisasi Format

    Dataset Splitting

    Dataset siap digunakan untuk training model.
    """)

# DISTRIBUSI DATASET

elif menu == "Distribusi Dataset":

    st.title("Distribusi Dataset")

    tab1, tab2, tab3 = st.tabs([
        "Distribusi Kelas",
        "Proporsi Kelas",
        "Distribusi Split"
    ])

    with tab1:

        fig_class = px.bar(
            summary_df,
            x="Kelas",
            y="Jumlah",
            text="Jumlah",
            color="Kelas"
        )

        st.plotly_chart(
            fig_class,
            use_container_width=True
        )

    with tab2:

        fig_pie = px.pie(
            summary_df,
            names="Kelas",
            values="Jumlah",
            hole=0.6
        )

        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    with tab3:

        fig_split = px.bar(
            split_df,
            x="Split",
            y="Jumlah",
            text="Jumlah",
            color="Split"
        )

        st.plotly_chart(
            fig_split,
            use_container_width=True
        )

# GALERI GAMBAR

elif menu == "Galeri Sampah":

    st.title("Galeri Sampah")

    kategori = st.selectbox(
        "Pilih Kategori Sampah",
        [
            "Organik",
            "Anorganik",
            "B3"
        ]
    )

    gambar = {
        "Organik": "samples/organik.jpg",
        "Anorganik": "samples/anorganik.jpg",
        "B3": "samples/B3.jpg"
    }

    deskripsi = {
        "Organik":
        "Sampah yang berasal dari makhluk hidup dan dapat terurai secara alami.",

        "Anorganik":
        "Sampah yang sulit terurai seperti plastik, logam, cardboard, dan masih banyak lagi.",

        "B3":
        "Limbah bahan berbahaya dan beracun yang memerlukan penanganan khusus."
    }

    st.image(
        gambar[kategori],
        caption=f"Contoh Sampah {kategori}",
        use_container_width=True
    )

    st.info(deskripsi[kategori])

# INSIGHT

elif menu == "Insight Dataset":

    st.title("Insight Dataset")

    st.info(f"""
    ### Temuan Utama

    Total gambar:
    **{total_data:,}**

    Jumlah kelas:
    **{total_kelas}**

    Kelas terbanyak:
    **{terbesar['Kelas']}**
    ({terbesar['Jumlah']:,} gambar)

    Kelas tersedikit:
    **{terkecil['Kelas']}**
    ({terkecil['Jumlah']:,} gambar)

    Imbalance Ratio:
    **{imbalance_ratio}**

    Dataset memiliki distribusi yang cukup seimbang
    sehingga layak digunakan untuk proses pelatihan model.
    """)

    with st.expander("Rincian Data"):

        st.dataframe(
            df,
            use_container_width=True
        )

# KESIMPULAN

elif menu == "Kesimpulan":

    st.title("Kesimpulan")

    st.success(f"""
    Dataset EcoSort terdiri dari
    {total_kelas} kategori sampah
    dengan total {total_data:,} gambar.

    Seluruh gambar telah melalui
    proses preprocessing dan standarisasi.

    Dataset memiliki ukuran gambar
    224×224 piksel dengan format yang seragam.

    Distribusi data antar kelas cukup baik
    dengan nilai imbalance ratio sebesar
    {imbalance_ratio}.

    Dataset telah dibagi ke dalam
    Train, Validation, dan Test Set.

    Dataset siap digunakan untuk
    pengembangan model klasifikasi
    sampah dengan algorithma CNN.
    """)