import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("employee_data.csv", parse_dates=["Hire Date"], dayfirst=True)
    return data

df = load_data()

#kolom baru untuk hire year
df["Hire Year"] = df["Hire Date"].dt.year

# Filter sidebar
st.sidebar.header("🔍 Filter Data")

# Filter department
departments = st.sidebar.multiselect(
    "Pilih Department", 
    options=df["Department"].unique(), 
    default=df["Department"].unique()
)

#Filter hire year
hire_years = st.sidebar.multiselect(
    "Pilih Hire Year", 
    options=df["Hire Year"].unique(), 
    default=df["Hire Year"].unique()
)

# Filter salary
# Slider untuk salary (boleh dipakai bareng atau ganti dengan input_number)
salary_min = int(df["Annual Salary (USD)"].min())
salary_max = int(df["Annual Salary (USD)"].max())

st.sidebar.write("Masukkan Rentang Salary (USD):")
min_salary_input = st.sidebar.number_input("Minimum Salary", min_value=salary_min, max_value=salary_max, value=salary_min, step=1000)
max_salary_input = st.sidebar.number_input("Maximum Salary", min_value=salary_min, max_value=salary_max, value=salary_max, step=1000)


# Apply filters
df = df[
    (df["Department"].isin(departments)) &
    (df["Annual Salary (USD)"] >= min_salary_input) &
    (df["Annual Salary (USD)"] <= max_salary_input) &
    (df["Hire Year"].isin(years))
]

# Scorecard
st.title("📊 HR Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Karyawan", f"{df.shape[0]}")
col2.metric("Jumlah Department", f"{df['Department'].nunique()}")
col3.metric("Total Salary", f"${df['Annual Salary (USD)'].sum():,.0f}")

col4, col5 = st.columns(2)
col4.metric("Rata-rata Salary", f"${df['Annual Salary (USD)'].mean():,.2f}")
col5.metric("Newest Hire Year", f"{df['Hire Date'].max().year}")

# Bar chart: jumlah karyawan per department
st.subheader("🔹 Jumlah Karyawan per Department")
dept_count = df["Department"].value_counts()
st.bar_chart(dept_count)

# Bar chart: rata-rata salary per department
st.subheader("🔹 Rata-rata Salary per Department")
avg_salary_dept = df.groupby("Department")["Annual Salary (USD)"].mean()
st.bar_chart(avg_salary_dept)

# Bar chart: jumlah karyawan per jabatan
st.subheader("🔹 Jumlah Karyawan per Jabatan")
designation_count = df["Designation"].value_counts()
st.bar_chart(designation_count)

# Pie chart: distribusi karyawan per department
st.subheader("🔹 Distribusi Karyawan per Department")
fig1, ax1 = plt.subplots()
ax1.pie(dept_count, labels=dept_count.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# Line chart: jumlah hire per bulan
st.subheader("🔹 Jumlah Hire per Bulan")
df["Hire Month"] = df["Hire Date"].dt.to_period("M").astype(str)
hire_per_bulan = df.groupby("Hire Month").size().sort_index()
st.line_chart(hire_per_bulan)

# Data table lengkap
st.subheader("📋 Data Lengkap Karyawan")
st.dataframe(df)
