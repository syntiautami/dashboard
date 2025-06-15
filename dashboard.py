import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("employee_data.csv", parse_dates=["Hire Date"], dayfirst=True)
    return data

df = load_data()

# Filter sidebar
st.sidebar.header("🔍 Filter Data")

# Filter department
departments = st.sidebar.multiselect(
    "Pilih Department", 
    options=df["Department"].unique(), 
    default=df["Department"].unique()
)

# Filter salary
min_salary = int(df["Annual Salary (USD)"].min())
max_salary = int(df["Annual Salary (USD)"].max())
salary_range = st.sidebar.slider(
    "Pilih Rentang Salary (USD)", 
    min_salary, 
    max_salary, 
    (min_salary, max_salary)
)

# Apply filters
df = df[
    (df["Department"].isin(departments)) &
    (df["Annual Salary (USD)"] >= salary_range[0]) &
    (df["Annual Salary (USD)"] <= salary_range[1])
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
