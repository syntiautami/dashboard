import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    # Ganti dengan path file kamu
    data = pd.read_csv("employee_data.csv", parse_dates=["Hire Date"], dayfirst=True)
    return data

df = load_data()

# Judul dashboard
st.title("📊 HR Dashboard Perusahaan PyA <3")

# Filter
st.sidebar.header("🔍 Filter Data")
departments = st.sidebar.multiselect("Pilih Department", options=df["Department"].unique(), default=df["Department"].unique())
designations = st.sidebar.multiselect("Pilih Designation", options=df["Designation"].unique(), default=df["Designation"].unique())
hire_date = st.sidebar.date_input(
    "Pilih Rentang Hire Date", 
    [df["Hire Date"].min(), df["Hire Date"].max()]
)
salary_range = st.sidebar.slider(
    "Rentang Salary (USD)",
    int(df["Annual Salary (USD)"].min()),
    int(df["Annual Salary (USD)"].max()),
    (int(df["Annual Salary (USD)"].min()), int(df["Annual Salary (USD)"].max()))
)

# Filter data
filtered_df = df[
    (df["Department"].isin(departments)) &
    (df["Designation"].isin(designations)) &
    (df["Hire Date"] >= pd.to_datetime(hire_date[0])) &
    (df["Hire Date"] <= pd.to_datetime(hire_date[1])) &
    (df["Annual Salary (USD)"] >= salary_range[0]) &
    (df["Annual Salary (USD)"] <= salary_range[1])
]

# Tampilkan data
st.subheader("📋 Data Karyawan (Setelah Filter)")
st.dataframe(filtered_df)

# Statistik
st.subheader("📈 Statistik")
st.write(f"Total Karyawan: {filtered_df.shape[0]}")
st.write(f"Rata-rata Gaji: ${filtered_df['Annual Salary (USD)'].mean():,.2f}")
st.write(f"Gaji Tertinggi: ${filtered_df['Annual Salary (USD)'].max():,.2f}")
st.write(f"Gaji Terendah: ${filtered_df['Annual Salary (USD)'].min():,.2f}")

# Visualisasi
st.subheader("🔹 Jumlah Karyawan per Department")
dept_count = filtered_df["Department"].value_counts()
st.bar_chart(dept_count)

st.subheader("🔹 Rata-rata Salary per Department")
avg_salary_dept = filtered_df.groupby("Department")["Annual Salary (USD)"].mean()
st.bar_chart(avg_salary_dept)

# Line chart: jumlah hire per bulan
st.subheader("🔹 Jumlah Hire per Bulan")
df_hire = filtered_df.copy()
df_hire["Bulan"] = df_hire["Hire Date"].dt.to_period("M").astype(str)
hire_per_bulan = df_hire.groupby("Bulan").size()
st.line_chart(hire_per_bulan)

# Analisis sederhana: klasifikasi salary
st.subheader("🧠 Klasifikasi Salary (Low / Medium / High)")
def classify_salary(salary):
    if salary < 50000:
        return "Low"
    elif salary < 65000:
        return "Medium"
    else:
        return "High"

filtered_df["Salary Class"] = filtered_df["Annual Salary (USD)"].apply(classify_salary)
st.dataframe(filtered_df[["Employee ID", "Full Name", "Annual Salary (USD)", "Salary Class"]])
