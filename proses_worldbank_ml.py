"""Pipeline World Bank internet users -> CSV -> cleansing -> Decision Tree -> HTML.

Cara pakai:
1. pip install -r requirements.txt
2. python proses_worldbank_ml.py
3. buka index.html di browser

Catatan tugas:
- Data utama diambil dari API World Bank, bukan HTML scraping.
- File mentah yang diekspor adalah data_mentah.csv.
- File laporan frontend yang dibuat otomatis adalah hasil_ml.html.
"""

from __future__ import annotations

from html import escape
from pathlib import Path
import math

import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

API_URL = "http://api.worldbank.org/v2/country/all/indicator/IT.NET.USER.ZS?format=json&per_page=2000"
HTTPS_API_URL = API_URL.replace("http://", "https://", 1)
RAW_CSV_PATH = Path("data_mentah.csv")
REPORT_HTML_PATH = Path("hasil_ml.html")


def buat_data_cadangan() -> pd.DataFrame:
    """Buat data cadangan agar notebook tetap bisa didemokan saat API diblokir jaringan."""
    countries = [
        ("ID", "IDN", "Indonesia"),
        ("MY", "MYS", "Malaysia"),
        ("SG", "SGP", "Singapore"),
        ("TH", "THA", "Thailand"),
        ("VN", "VNM", "Vietnam"),
        ("PH", "PHL", "Philippines"),
        ("US", "USA", "United States"),
        ("JP", "JPN", "Japan"),
        ("KR", "KOR", "Korea, Rep."),
        ("CN", "CHN", "China"),
        ("IN", "IND", "India"),
        ("AU", "AUS", "Australia"),
        ("BR", "BRA", "Brazil"),
        ("ZA", "ZAF", "South Africa"),
        ("DE", "DEU", "Germany"),
        ("FR", "FRA", "France"),
        ("GB", "GBR", "United Kingdom"),
        ("CA", "CAN", "Canada"),
        ("MX", "MEX", "Mexico"),
        ("NG", "NGA", "Nigeria"),
        ("EG", "EGY", "Egypt, Arab Rep."),
        ("SA", "SAU", "Saudi Arabia"),
        ("TR", "TUR", "Turkiye"),
        ("AR", "ARG", "Argentina"),
        ("RU", "RUS", "Russian Federation"),
    ]
    years = range(1960, 2025)
    records = []

    for country_index, (country_id, iso3, country_name) in enumerate(countries):
        base = 4 + (country_index % 9) * 2.4
        growth = 0.095 + (country_index % 5) * 0.008
        midpoint = 2001 + (country_index % 7)

        for year in years:
            value = 100 / (1 + math.exp(-growth * (year - midpoint))) - base
            value = max(0, min(99.5, value + (country_index % 4) * 1.7))
            records.append(
                {
                    "indicator": {"id": "IT.NET.USER.ZS", "value": "Individuals using the Internet (% of population)"},
                    "country": {"id": country_id, "value": country_name},
                    "countryiso3code": iso3,
                    "date": str(year),
                    "value": round(value, 4) if year >= 1980 else None,
                    "unit": "",
                    "obs_status": "",
                    "decimal": 1,
                    "data_mode": "fallback_demo",
                }
            )

    return pd.DataFrame(records)


def ambil_data_world_bank() -> tuple[pd.DataFrame, str]:
    """Ambil data JSON dari World Bank API dan ubah indeks ke-1 menjadi DataFrame."""
    last_error: Exception | None = None

    for url in (API_URL, HTTPS_API_URL):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            json_data = response.json()

            if not isinstance(json_data, list) or len(json_data) < 2:
                raise ValueError("Format respons API World Bank tidak sesuai: indeks ke-1 tidak ditemukan.")

            data_records = json_data[1]
            if not data_records:
                raise ValueError("Respons API World Bank tidak berisi data indikator.")

            df_api = pd.DataFrame(data_records)
            df_api["data_mode"] = "world_bank_api"
            return df_api, "World Bank API"
        except (requests.RequestException, ValueError) as error:
            last_error = error

    print(f"Peringatan: API World Bank tidak bisa diakses ({last_error}). Menggunakan data cadangan demo.")
    return buat_data_cadangan(), "Data cadangan demo saat API diblokir"


def ekspor_data_mentah(df_raw: pd.DataFrame) -> None:
    """Simpan DataFrame mentah ke CSV."""
    df_raw.to_csv(RAW_CSV_PATH, index=False)


def bersihkan_data() -> tuple[pd.DataFrame, int, int, int, int]:
    """Baca CSV mentah, ubah value ke numerik, hitung missing, dan drop missing value."""
    df = pd.read_csv(RAW_CSV_PATH)
    total_baris_mentah = len(df)

    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    missing_values = int(df["value"].isna().sum())

    df_clean = df.dropna(subset=["value"]).copy()
    total_baris_bersih = len(df_clean)
    total_baris_dihapus = total_baris_mentah - total_baris_bersih

    if total_baris_bersih <= 1000:
        raise ValueError(
            f"Jumlah data bersih harus di atas 1000 data, tetapi hanya ada {total_baris_bersih}."
        )

    return df_clean, total_baris_mentah, total_baris_bersih, total_baris_dihapus, missing_values


def latih_model_decision_tree(df_clean: pd.DataFrame) -> tuple[pd.DataFrame, float, float]:
    """Buat target Status_Digital, latih Decision Tree, dan kembalikan akurasi."""
    rata_rata_value = float(df_clean["value"].mean())
    df_model = df_clean.copy()
    df_model["Status_Digital"] = (df_model["value"] > rata_rata_value).astype(int)
    df_model["date"] = pd.to_numeric(df_model["date"], errors="coerce")
    df_model = df_model.dropna(subset=["date", "value", "Status_Digital"]).copy()
    df_model["date"] = df_model["date"].astype(int)

    X = df_model[["date", "value"]]
    y = df_model["Status_Digital"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    akurasi = float(model.score(X_test, y_test))

    return df_model, rata_rata_value, akurasi


def buat_laporan_html(
    sumber_data: str,
    total_baris_mentah: int,
    total_baris_bersih: int,
    total_baris_dihapus: int,
    missing_values: int,
    rata_rata_value: float,
    akurasi: float,
) -> None:
    """Buat string HTML laporan dan simpan ke hasil_ml.html menggunakan open() bawaan Python."""
    html_report = f"""<!doctype html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, sans-serif; color: #0f172a; background: #ffffff; }}
    .report {{ padding: 24px; background: linear-gradient(135deg, #eff6ff, #f8fafc); }}
    h2 {{ margin: 0 0 16px; color: #1e3a8a; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }}
    .metric {{ padding: 16px; border: 1px solid #dbeafe; border-radius: 14px; background: #ffffff; }}
    .label {{ margin: 0 0 8px; color: #64748b; font-size: 13px; font-weight: 700; text-transform: uppercase; }}
    .value {{ margin: 0; color: #0f172a; font-size: 24px; font-weight: 800; }}
    .source {{ margin: 18px 0 0; color: #334155; line-height: 1.6; word-break: break-word; }}
  </style>
</head>
<body>
  <section class="report">
    <h2>Laporan Prediksi Kesiapan Digital</h2>
    <div class="grid">
      <article class="metric"><p class="label">Data Mentah</p><p class="value">{total_baris_mentah}</p></article>
      <article class="metric"><p class="label">Data Bersih</p><p class="value">{total_baris_bersih}</p></article>
      <article class="metric"><p class="label">Data Dihapus</p><p class="value">{total_baris_dihapus}</p></article>
      <article class="metric"><p class="label">Missing Value</p><p class="value">{missing_values}</p></article>
      <article class="metric"><p class="label">Mean Value</p><p class="value">{rata_rata_value:.2f}</p></article>
      <article class="metric"><p class="label">Akurasi</p><p class="value">{akurasi:.2%}</p></article>
    </div>
    <p class="source"><strong>Sumber data aktif:</strong> {escape(sumber_data)}</p>
    <p class="source"><strong>Sumber API utama:</strong> {escape(API_URL)}</p>
  </section>
</body>
</html>
"""

    with open(REPORT_HTML_PATH, "w", encoding="utf-8") as file:
        file.write(html_report)


def main() -> None:
    df_raw, sumber_data = ambil_data_world_bank()
    ekspor_data_mentah(df_raw)

    df_clean, total_baris_mentah, total_baris_bersih, total_baris_dihapus, missing_values = bersihkan_data()
    _df_model, rata_rata_value, akurasi = latih_model_decision_tree(df_clean)

    buat_laporan_html(
        sumber_data=sumber_data,
        total_baris_mentah=total_baris_mentah,
        total_baris_bersih=total_baris_bersih,
        total_baris_dihapus=total_baris_dihapus,
        missing_values=missing_values,
        rata_rata_value=rata_rata_value,
        akurasi=akurasi,
    )

    print(f"Sumber data aktif: {sumber_data}")
    print(f"Total missing values pada kolom value: {missing_values}")
    print(f"Total baris data mentah: {total_baris_mentah}")
    print(f"Total baris data bersih: {total_baris_bersih}")
    print(f"Total baris data yang dihapus: {total_baris_dihapus}")
    print(f"Akurasi Decision Tree: {akurasi:.2%}")
    print(f"File CSV berhasil dibuat: {RAW_CSV_PATH}")
    print(f"File HTML berhasil dibuat: {REPORT_HTML_PATH}")


if __name__ == "__main__":
    main()
