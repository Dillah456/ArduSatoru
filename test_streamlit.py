import streamlit as st
import pandas as pd

# Konfigurasi halaman
st.set_page_config(
    page_title="Website Streamlit",
    page_icon="📘",
    layout="wide"
)

# Sidebar
st.sidebar.title("📂 Menu")
menu = st.sidebar.radio(
    "Pilih Halaman",
    ["Home", "Input Data", "Lihat Data"]
)

# State untuk menyimpan data
if "data" not in st.session_state:
    st.session_state.data = []

# ======================
# HALAMAN HOME
# ======================
if menu == "Home":
    st.title("🏠 Selamat Datang")
    st.write("""
    Ini adalah contoh website sederhana berbasis **Streamlit + Python**.
    
    Cocok untuk:
    - Dashboard
    - Sistem Catatan
    - Prototipe cepat
    - Aplikasi internal
    """)

# ======================
# HALAMAN INPUT DATA
# ======================
elif menu == "Input Data":
    st.title("✍️ Input Data")

    with st.form("form_input"):
        judul = st.text_input("Judul")
        kategori = st.selectbox(
            "Kategori",
            ["Fleeting Note", "Literature Note", "Permanent Note"]
        )
        isi = st.text_area("Isi Catatan")
        submit = st.form_submit_button("Simpan")

        if submit:
            st.session_state.data.append({
                "Judul": judul,
                "Kategori": kategori,
                "Isi": isi
            })
            st.success("Data berhasil disimpan!")

# ======================
# HALAMAN LIHAT DATA
# ======================
elif menu == "Lihat Data":
    st.title("📊 Data Tersimpan")

    if st.session_state.data:
        df = pd.DataFrame(st.session_state.data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada data.")
