"""Pipeline World Bank: ekstraksi, cleansing, Decision Tree, dan ekspor HTML.

Jalankan file ini berurutan seperti cell Jupyter untuk menghasilkan:
- data_mentah.csv
- hasil_ml.html
"""

import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

API_URL = "http://api.worldbank.org/v2/country/all/indicator/IT.NET.USER.ZS?format=json&per_page=2000"
RAW_CSV = "data_mentah.csv"
REPORT_HTML = "hasil_ml.html"


# Langkah 1: Ekstraksi API dan Ekspor CSV
response = requests.get(API_URL, timeout=30)
response.raise_for_status()
json_data = response.json()

# Data World Bank berada pada indeks ke-1; indeks ke-0 berisi metadata pagination.
data_records = json_data[1]
df_raw = pd.DataFrame(data_records)
df_raw.to_csv(RAW_CSV, index=False)


# Langkah 2: Data Cleansing (Data Analyst)
# Catatan: langkah pertama menyimpan CSV, sehingga file yang dibaca adalah data_mentah.csv.
df = pd.read_csv(RAW_CSV)
total_baris_mentah = len(df)

df["value"] = pd.to_numeric(df["value"], errors="coerce")
missing_values = df["value"].isna().sum()

df_clean = df.dropna(subset=["value"]).copy()
total_baris_bersih = len(df_clean)
total_baris_dihapus = total_baris_mentah - total_baris_bersih

print(f"Total missing values pada kolom value: {missing_values}")
print(f"Total baris data mentah: {total_baris_mentah}")
print(f"Total baris data bersih: {total_baris_bersih}")

if total_baris_bersih <= 1000:
    raise ValueError("Jumlah data bersih harus di atas 1000 data.")


# Langkah 3: Machine Learning (Decision Tree)
mean_value = df_clean["value"].mean()
df_clean["Status_Digital"] = (df_clean["value"] > mean_value).astype(int)
df_clean["date"] = pd.to_numeric(df_clean["date"], errors="coerce").astype(int)

X = df_clean[["date", "value"]]
y = df_clean["Status_Digital"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)
akurasi = model.score(X_test, y_test)
print(f"Akurasi Decision Tree: {akurasi:.2%}")


# Langkah 4: Ekspor ke Frontend (Jembatan HTML)
html_report = f"""<!doctype html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      color: #0f172a;
      background: #ffffff;
    }}
    .report {{
      padding: 24px;
      border-radius: 16px;
      background: linear-gradient(135deg, #eff6ff, #f8fafc);
      border: 1px solid #dbeafe;
    }}
    h2 {{ margin-top: 0; }}
    p {{ font-size: 16px; line-height: 1.6; }}
    strong {{ color: #1d4ed8; }}
  </style>
</head>
<body>
  <section class="report">
    <h2>Laporan Prediksi Kesiapan Digital</h2>
    <p><strong>Sumber API:</strong> {API_URL}</p>
    <p><strong>Jumlah data bersih:</strong> {total_baris_bersih}</p>
    <p><strong>Jumlah data yang dihapus:</strong> {total_baris_dihapus}</p>
    <p><strong>Akurasi Decision Tree:</strong> {akurasi:.2%}</p>
  </section>
</body>
</html>
"""

with open(REPORT_HTML, "w", encoding="utf-8") as file:
    file.write(html_report)

print(f"Laporan HTML berhasil disimpan ke {REPORT_HTML}")
