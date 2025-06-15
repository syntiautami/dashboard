import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv("employee_data.csv", parse_dates=["Hire Date"], dayfirst=True)
    return data

df = load_data()

# Judul dashboard
st.title("📊 HR Dashboard Perusahaan PyA")

# Sidebar filter
st.sidebar.header("🔍 Filter Data")
departments = st.sidebar.multiselect(
    "Pilih Department", options=df["Department"].unique(), default=df["Department"].unique())
designations = st.sidebar.multiselect(
    "Pilih Designation", options=df["Designation"].unique(), default=df["Designation"].unique())
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

# Berbagai visualisasi

st.subheader("🔹 Bar Chart: Jumlah Karyawan per Department")
dept_count = filtered_df["Department"].value_counts()
st.bar_chart(dept_count)

st.subheader("🔹 Pie Chart: Proporsi Karyawan per Department")
fig1, ax1 = plt.subplots()
ax1.pie(dept_count, labels=dept_count.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

st.subheader("🔹 Line Chart: Jumlah Hire per Bulan")
df_hire = filtered_df.copy()
df_hire["Bulan"] = df_hire["Hire Date"].dt.to_period("M").astype(str)
hire_per_bulan = df_hire.groupby("Bulan").size()
st.line_chart(hire_per_bulan)

st.subheader("🔹 Scatter Plot: Salary vs Hire Date")
fig2, ax2 = plt.subplots()
ax2.scatter(filtered_df["Hire Date"], filtered_df["Annual Salary (USD)"])
ax2.set_xlabel("Hire Date")
ax2.set_ylabel("Annual Salary (USD)")
st.pyplot(fig2)

st.subheader("🔹 Boxplot: Distribusi Salary per Department")
fig3, ax3 = plt.subplots(figsize=(10,5))
sns.boxplot(x="Department", y="Annual Salary (USD)", data=filtered_df, ax=ax3)
st.pyplot(fig3)

# Analisis Salary Class
st.subheader("🧠 Analisis Salary Class (Low / Medium / High)")
def classify_salary(salary):
    if salary < 50000:
        return "Low"
    elif salary < 65000:
        return "Medium"
    else:
        return "High"

filtered_df["Salary Class"] = filtered_df["Annual Salary (USD)"].apply(classify_salary)
st.dataframe(filtered_df[["Employee ID", "Full Name", "Annual Salary (USD)", "Salary Class"]])

# Bonus: ML sederhana
st.subheader("🤖 Prediksi Salary Class Berdasarkan Department")
# Encode department
le = LabelEncoder()
filtered_df["Dept_Code"] = le.fit_transform(filtered_df["Department"])
filtered_df["Salary_Class_Num"] = filtered_df["Salary Class"].map({"Low":0, "Medium":1, "High":2})

# ML model
X = filtered_df[["Dept_Code"]]
y = filtered_df["Salary_Class_Num"]
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

dept_input = st.selectbox("Pilih Department untuk Prediksi", filtered_df["Department"].unique())
dept_code = le.transform([dept_input])[0]
pred = model.predict([[dept_code]])
class_map = {0:"Low", 1:"Medium", 2:"High"}
st.write(f"Prediksi salary class untuk {dept_input}: {class_map[pred[0]]}")
