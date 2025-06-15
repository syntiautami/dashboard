import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("employee_data.csv", parse_dates=["Hire Date"], dayfirst=True)
    return data

df = load_data()

# Filter (opsional bisa dihilangkan kalau mau full data)
st.sidebar.header("🔍 Filter Data")
departments = st.sidebar.multiselect("Pilih Department", options=df["Department"].unique(), default=df["Department"].unique())
df = df[df["Department"].isin(departments)]

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
st.subheader("🔹 Jumlah Karyawan per Jabatan")
designation_count = df["Designation"].value_counts()

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(designation_count.index, designation_count.values, color="skyblue", edgecolor="black")
ax.set_xlabel("Designation")
ax.set_ylabel("Jumlah Karyawan")
ax.set_title("Jumlah Karyawan per Jabatan")
plt.xticks(rotation=45, ha='right')  # Biar nama jabatan nggak tabrakan
st.pyplot(fig)

chart = alt.Chart(designation_count).mark_bar().encode(
    x=alt.X("Designation", sort="-y"),
    y="Count",
    tooltip=["Designation", "Count"]
).properties(width=700)

st.altair_chart(chart, use_container_width=True)


# Bar chart: rata-rata salary per department
st.subheader("🔹 Rata-rata Salary per Department")
avg_salary_dept = df.groupby("Department")["Annual Salary (USD)"].mean()
st.bar_chart(avg_salary_dept)

# Bar chart: jumlah karyawan per jabatan
st.subheader("🔹 Jumlah Karyawan per Department")

# Hitung jumlah karyawan per dept
dept_count = df["Department"].value_counts()

# Bikin bar chart
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(dept_count.index, dept_count.values, color="skyblue", edgecolor="black")
ax.set_xlabel("Department")
ax.set_ylabel("Jumlah Karyawan")
ax.set_title("Jumlah Karyawan per Department")
plt.xticks(rotation=45, ha='right')  # Biar label dept miring dikit biar muat

st.pyplot(fig)


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
