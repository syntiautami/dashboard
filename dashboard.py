import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("employee_data.csv", parse_dates=["Hire Date"], dayfirst=True)
    return data

df = load_data()

# Tambah kolom tahun hire
df["Hire Year"] = df["Hire Date"].dt.year

# Sidebar filter
st.sidebar.header("🔍 Filter Data")

# Filter department
departments = st.sidebar.multiselect(
    "Pilih Department",
    options=df["Department"].unique(),
    default=df["Department"].unique()
)

# Filter tahun hire
years = st.sidebar.multiselect(
    "Pilih Tahun Hire",
    options=sorted(df["Hire Year"].dropna().unique()),
    default=sorted(df["Hire Year"].dropna().unique())
)

# Filter salary
min_salary = int(df["Annual Salary (USD)"].min())
max_salary = int(df["Annual Salary (USD)"].max())
salary_range = st.sidebar.slider(
    "Pilih Rentang Salary (USD)",
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary)
)

# Terapkan filter
df = df[
    (df["Department"].isin(departments)) &
    (df["Hire Year"].isin(years)) &
    (df["Annual Salary (USD)"] >= salary_range[0]) &
    (df["Annual Salary (USD)"] <= salary_range[1])
]

st.title("📊 HR Dashboard")

# Baris 1
col1, col2, col3 = st.columns(3)
col1.metric("👥 Total Karyawan", f"{df.shape[0]}")
col2.metric("🏢 Jumlah Department", f"{df['Department'].nunique()}")
col3.metric("💰 Total Salary", f"${df['Annual Salary (USD)'].sum():,.0f}")

# Baris 2
col4, col5, col6 = st.columns(3)
col4.metric("📊 Rata-rata Salary", f"${df['Annual Salary (USD)'].mean():,.2f}")
if not df.empty:
    col5.metric("📅 Newest Hire Year", f"{df['Hire Date'].max().year}")
else:
    col5.metric("📅 Newest Hire Year", "-")
col6.metric("📂 Total Data Aktif", len(df))

# Bar chart horizontal: jumlah karyawan per department
st.subheader("🔹 Jumlah Karyawan per Department")
dept_count = df["Department"].value_counts().reset_index()
dept_count.columns = ["Department", "Jumlah Karyawan"]

fig_bar_horizontal = px.bar(
    dept_count,
    x="Jumlah Karyawan",
    y="Department",
    orientation="h",
    labels={"Jumlah Karyawan": "Jumlah Karyawan", "Department": "Department"},
    text="Jumlah Karyawan"
)
fig_bar_horizontal.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig_bar_horizontal)

# Bar chart: rata-rata salary per department
st.subheader("🔹 Rata-rata Salary per Department")
avg_salary_dept = df.groupby("Department")["Annual Salary (USD)"].mean().reset_index()
fig_avg_salary = px.bar(
    avg_salary_dept,
    x="Department",
    y="Annual Salary (USD)",
    labels={"Annual Salary (USD)": "Rata-rata Salary"},
    text_auto='.2s'
)
st.plotly_chart(fig_avg_salary)

# Pie chart: distribusi karyawan per department
st.subheader("🔹 Distribusi Karyawan per Department")
if not dept_count.empty:
    pie_fig = px.pie(
        dept_count,
        names="Department",
        values="Jumlah Karyawan",
        title="Distribusi Karyawan per Department",
        hole=0.3
    )
    st.plotly_chart(pie_fig)
else:
    st.write("Tidak ada data untuk pie chart.")

# Line chart: jumlah hire per bulan
st.subheader("🔹 Jumlah Hire per Bulan")
if not df.empty:
    df["Hire Month"] = df["Hire Date"].dt.to_period("M").astype(str)
    hire_per_bulan = df.groupby("Hire Month").size().reset_index(name="Jumlah")
    fig_line = px.line(
        hire_per_bulan,
        x="Hire Month",
        y="Jumlah",
        markers=True,
        title="Jumlah Hire per Bulan"
    )
    st.plotly_chart(fig_line)
else:
    st.write("Tidak ada data untuk line chart.")

# Data table lengkap
st.subheader("📋 Data Lengkap Karyawan")
st.dataframe(df)
