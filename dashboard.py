import streamlit as st
import pandas as pd
import plotly.express as px

# KONFIGURASI
st.set_page_config(
    page_title="Dashboard Preprocessing Dataset Sampah",
    page_icon="♻️",
    layout="wide"
)

st.title("♻️ Dashboard Preprocessing Dataset Sampah")

# LOAD CSV
@st.cache_data
def load_dataset_info():
    return pd.read_csv("dataset_info.csv")

df = load_dataset_info()

# OVERVIEW
st.header("📊 Dataset Overview")

total_images = len(df)

train_count = len(df[df["split"] == "train"])
val_count = len(df[df["split"] == "val"])
test_count = len(df[df["split"] == "test"])

total_classes = df["kelas"].nunique()

class_count = df["kelas"].value_counts()

imbalance_ratio = round(
    class_count.max() / class_count.min(),
    2
)

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric("Total Gambar", total_images)
col2.metric("Train", train_count)
col3.metric("Validation", val_count)
col4.metric("Test", test_count)
col5.metric("Jumlah Kelas", total_classes)
col6.metric("Imbalance Ratio", imbalance_ratio)

if imbalance_ratio < 1.5:
    st.success("✅ Dataset Balanced")
else:
    st.warning("⚠️ Dataset Imbalanced")

st.divider()

# DISTRIBUSI DATASET
st.header("📈 Distribusi Dataset")

split_df = (
    df["split"]
    .value_counts()
    .reset_index()
)

split_df.columns = ["Dataset", "Jumlah"]

fig_split = px.bar(
    split_df,
    x="Dataset",
    y="Jumlah",
    color="Dataset",
    text="Jumlah",
    title="Distribusi Train Validation Test"
)

st.plotly_chart(
    fig_split,
    use_container_width=True
)

# DISTRIBUSI KELAS
st.header("📊 Distribusi Kelas")

class_df = (
    df.groupby(["split", "kelas"])
    .size()
    .reset_index(name="Jumlah")
)

fig_class = px.bar(
    class_df,
    x="kelas",
    y="Jumlah",
    color="split",
    barmode="group",
    text="Jumlah",
    title="Distribusi Kelas pada Setiap Split"
)

st.plotly_chart(
    fig_class,
    use_container_width=True
)

# RESOLUSI GAMBAR
st.header("📏 Distribusi Resolusi")

colA, colB, colC = st.columns(3)

colA.metric(
    "Lebar Rata-rata",
    round(df["width"].mean(), 1)
)

colB.metric(
    "Tinggi Rata-rata",
    round(df["height"].mean(), 1)
)

colC.metric(
    "Resolusi Dominan",
    f"{df['width'].mode()[0]} x {df['height'].mode()[0]}"
)

col1, col2 = st.columns(2)

with col1:

    fig_width = px.histogram(
        df,
        x="width",
        nbins=30,
        title="Distribusi Lebar Gambar"
    )

    st.plotly_chart(
        fig_width,
        use_container_width=True
    )

with col2:

    fig_height = px.histogram(
        df,
        x="height",
        nbins=30,
        title="Distribusi Tinggi Gambar"
    )

    st.plotly_chart(
        fig_height,
        use_container_width=True
    )

# RINGKASAN DATA
st.subheader("📋 Ringkasan Jumlah Data")

summary = (
    df.groupby(["split", "kelas"])
    .size()
    .reset_index(name="Jumlah")
)

st.dataframe(
    summary,
    use_container_width=True
)

# SAMPLE IMAGE
st.header("🖼️ Sample Image")

sample_cols = st.columns(3)

kelas_list = [
    "Anorganik",
    "B3",
    "Organik"
]

for i, kelas in enumerate(kelas_list):

    image_path = f"samples/{kelas}.jpg"

    sample_cols[i].image(
        image_path,
        caption=kelas,
        use_container_width=True
    )

# FORMAT FILE
st.header("🗂️ Format File")

format_df = (
    df["format"]
    .value_counts()
    .reset_index()
)

format_df.columns = [
    "Format",
    "Jumlah"
]

fig_format = px.pie(
    format_df,
    names="Format",
    values="Jumlah",
    title="Distribusi Format File"
)

st.plotly_chart(
    fig_format,
    use_container_width=True
)

# METADATA
st.header("📋 Metadata Dataset")

st.dataframe(
    df,
    use_container_width=True
)