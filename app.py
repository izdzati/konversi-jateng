import streamlit as st
import pandas as pd
from config import sheet

# --- Ambil data dari Google Sheets ---
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- Styling CSS ---
st.markdown("""
    <style>
    .header-box {
        background-color: #d3d3d3;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
    }
    .result-box {
        background-color: #ffff99;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigasi ---
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Input Data Baru Konversi", "Konversi"])

# --- Halaman Input Data Baru ---
if page == "Input Data Baru Konversi":
    st.title("📥 Input Data Baru Konversi")

    # Form Input Manual
    st.subheader("✍️ Input Manual")
    with st.form("manual_form"):
        col1, col2 = st.columns(2)
        with col1:
            kode_relasi = st.text_input("Kode Relasi")
            jenis_tank = st.text_input("Jenis Tank")
            material = st.text_input("Material")
            metode = st.selectbox("Metode", ["Metode 1", "Metode 3"])
        with col2:
            nama_relasi = st.text_input("Nama Relasi")
            level_data = st.number_input("Level Data", step=0.001)
            kg = st.number_input("KG", step=0.001)
            liter = st.number_input("Liter", step=0.001)
            m3 = st.number_input("M3", step=0.001)

        submitted = st.form_submit_button("Tambah Data")
        if submitted:
            new_row = {
                "KODE RELASI": kode_relasi,
                "JENIS TANK": jenis_tank,
                "MATERIAL": material,
                "METODE": metode,
                "NAMA RELASI": nama_relasi,
                "LEVEL DATA": level_data,
                "KG": kg,
                "LITER": liter,
                "M3": m3
            }
            # Tambah data
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            # Bersihkan nilai yang tidak valid
            df_clean = df.replace([float('inf'), float('-inf')], None)
            df_clean = df_clean.fillna('')  # bisa juga fillna(0) kalau kamu mau ganti NaN ke 0

            # Update ke Google Sheets
            try:
              sheet.update([df_clean.columns.values.tolist()] + df_clean.values.tolist())
              st.success("Data berhasil ditambahkan!")
            except Exception as e:
              st.error(f"Gagal mengupdate ke Google Sheets: {e}")
              
    # Upload Excel / CSV
    st.subheader("📁 Upload Data Excel / CSV")
    uploaded_file = st.file_uploader("Pilih file Excel/CSV", type=["xlsx", "csv"])

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

    # Pastikan struktur data sesuai
    required_columns = ["KODE RELASI","JENIS TANK","MATERIAL","METODE","NAMA RELASI","LEVEL DATA", "KG", "LITER", "M3"]
    if all(col in df.columns for col in required_columns):
        st.write("📋 **Preview Data yang Diunggah:**")
        st.dataframe(df)  # Hanya menampilkan file yang di-upload

        if st.button("Tambah Data dari File"):
            df_clean = df.replace([float('inf'), float('-inf')], None).fillna("")
            for row in df_clean.itertuples(index=False):
                sheet.append_row(list(row))
            st.success("✅ Data dari file berhasil ditambahkan!")
    else:
        st.error("❌ Format kolom tidak sesuai! Harus ada: " + ", ".join(required_columns))

# --- Halaman Konversi ---
elif page == "Konversi":
    st.title("📊 Dashboard Konversi")

    # Pilih Nama Relasi
    relasi_unik = df["NAMA RELASI"].unique().tolist()
    selected_relasi = st.selectbox("Pilih Nama Relasi", relasi_unik)

    relasi_df = df[df["NAMA RELASI"] == selected_relasi]

    if not relasi_df.empty:
        kode_relasi = relasi_df["KODE RELASI"].iloc[0]
        jenis_tank = relasi_df["JENIS TANK"].iloc[0]
        material = relasi_df["MATERIAL"].iloc[0]
        metode_tersedia = relasi_df["METODE"].unique().tolist()

        st.markdown(f"**Nama Relasi :** {selected_relasi}")
        st.markdown(f"**Kode Relasi :** {kode_relasi}")
        st.markdown(f"**Jenis Tank :** {jenis_tank}")
        st.markdown(f"**Material :** {material}")

        metode_pilihan = st.selectbox("Pilih Metode", metode_tersedia)
        st.markdown(f"**Metode :** {metode_pilihan}")

        if metode_pilihan == "Metode 1":
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown('<div class="header-box">Level</div>', unsafe_allow_html=True)
                level_awal = st.number_input("Level Awal", min_value=0.0, step=0.1, key="m1_awal")
                level_akhir = st.number_input("Level Akhir", min_value=0.0, step=0.1, key="m1_akhir")
                level_hasil = abs(level_akhir - level_awal)

            df_awal = relasi_df[relasi_df["LEVEL DATA"] == level_awal]
            df_akhir = relasi_df[relasi_df["LEVEL DATA"] == level_akhir]

            with col2:
                st.markdown('<div class="header-box">Liter</div>', unsafe_allow_html=True)
                liter_awal = df_awal["LITER"].iloc[0] if not df_awal.empty else 0
                liter_akhir = df_akhir["LITER"].iloc[0] if not df_akhir.empty else 0
                liter_hasil = abs(liter_akhir - liter_awal)
                st.markdown(f"**Liter Awal:** {liter_awal}")
                st.markdown(f"**Liter Akhir:** {liter_akhir}")

            with col3:
                st.markdown('<div class="header-box">KG</div>', unsafe_allow_html=True)
                kg_awal = df_awal["KG"].iloc[0] if not df_awal.empty else 0
                kg_akhir = df_akhir["KG"].iloc[0] if not df_akhir.empty else 0
                kg_hasil = abs(kg_akhir - kg_awal)
                st.markdown(f"**KG Awal:** {kg_awal}")
                st.markdown(f"**KG Akhir:** {kg_akhir}")

            with col4:
                st.markdown('<div class="header-box">M³</div>', unsafe_allow_html=True)
                m3_awal = df_awal["M3"].iloc[0] if not df_awal.empty else 0
                m3_akhir = df_akhir["M3"].iloc[0] if not df_akhir.empty else 0
                m3_hasil = abs(m3_akhir - m3_awal)
                st.markdown(f"**M³ Awal:** {m3_awal}")
                st.markdown(f"**M³ Akhir:** {m3_akhir}")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f'<div class="result-box">Level Hasil: {level_hasil}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="result-box">Liter Hasil: {liter_hasil}</div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="result-box">KG Hasil: {kg_hasil}</div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="result-box">M³ Hasil: {m3_hasil}</div>', unsafe_allow_html=True)

        elif metode_pilihan == "Metode 3":
            st.subheader("🔢 Konversi Muatan - Metode 3")

            # Ambil parameter (LEVEL DATA) dari database
            parameter = relasi_df["LEVEL DATA"].iloc[0] if not relasi_df.empty and "LEVEL DATA" in relasi_df.columns else 0

            st.markdown(f"**Parameter (dari Level Data):** `{parameter}`")

            # Input Muatan KG dari user
            muatan_kg = st.number_input("Masukkan Muatan (KG)", min_value=0.0, step=0.01)

            # Hasil konversi = parameter x muatan
            hasil = parameter * muatan_kg

            # Tampilkan hasil
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="header-box">Parameter (Level Data)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-box">{parameter}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="header-box">Hasil Konversi (KG)</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-box">{hasil}</div>', unsafe_allow_html=True)