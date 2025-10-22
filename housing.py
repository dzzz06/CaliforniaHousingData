import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- 页面配置 ---
st.set_page_config(page_title="California Housing App", layout="wide")

# --- 加载数据 ---
@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    return df

df = load_data()

# --- 页面标题 ---
st.title("California Housing Data(1990) by Zhan Ding")

# --- 侧边栏 ---
st.sidebar.header("Filters")

# 1️⃣ 多选框：按地区类型筛选
location_types = df["ocean_proximity"].unique()
selected_locations = st.sidebar.multiselect(
    "Select Location Type",
    options=location_types,
    default=location_types
)

# 2️⃣ 单选框：按收入水平筛选
income_filter = st.sidebar.radio(
    "Select Income Level",
    ("All", "Low (≤ 2.5)", "Medium (2.5–4.5)", "High (≥ 4.5)")
)

# --- 滑块: 房价范围 ---
min_price = int(df["median_house_value"].min())
max_price = int(df["median_house_value"].max())

price_range = st.slider(
    "Select Median House Value Range",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# --- 数据筛选逻辑 ---
filtered_df = df.copy()

# 按地区类型过滤
if selected_locations:
    filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(selected_locations)]

# 按收入水平过滤（使用 if 语句）
if income_filter == "Low (≤ 2.5)":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_filter == "Medium (2.5–4.5)":
    filtered_df = filtered_df[
        (filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)
    ]
elif income_filter == "High (≥ 4.5)":
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]
# 若为 "All" 则不过滤

# 按房价范围过滤
filtered_df = filtered_df[
    (filtered_df["median_house_value"] >= price_range[0]) &
    (filtered_df["median_house_value"] <= price_range[1])
]

# --- 输出统计信息 ---
st.write(f"### Showing {len(filtered_df)} houses based on selected filters")

# --- 地图展示 ---
st.map(filtered_df[["latitude", "longitude"]], use_container_width=True)

# --- 房价直方图 ---
st.write("### Median House Value Distribution (30 bins)")
fig, ax = plt.subplots()
ax.hist(filtered_df["median_house_value"], bins=30, edgecolor='black')
ax.set_xlabel("Median House Value")
ax.set_ylabel("Count")
st.pyplot(fig)