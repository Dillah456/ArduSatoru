import streamlit as st
import pandas as pd
import requests

# Konfigurasi halaman
st.set_page_config(
    page_title="Expert System - Rekomendasi Tempat Wisata",
    page_icon="🗺️",
    layout="wide"
)

# URL API
API_URL = "https://x8ki-letl-twmt.n7.xano.io/api:LmVdZTtF/alya"

# Fungsi untuk fetch data dari API
@st.cache_data
def fetch_data_from_api():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Gagal terhubung ke API: {e}")
        return []

# Fungsi untuk filter rekomendasi
def filter_recommendations(data, budget, kecamatan):
    """
    Filter tempat wisata berdasarkan:
    1. Budget user harus berada dalam range Cost_Start dan Cost_Max
    2. Kecamatan sesuai dengan input user (jika ada)
    """
    recommendations = []
    
    for place in data:
        # Check cost range
        cost_start = place.get("Cost_Start", 0)
        cost_max = place.get("Cost_Max", float('inf'))
        
        if cost_start <= budget <= cost_max:
            # Check kecamatan if specified
            if kecamatan:
                place_kecamatan = place.get("Domisili", {}).get("kecamatan", "").lower()
                if kecamatan.lower() in place_kecamatan or place_kecamatan in kecamatan.lower():
                    recommendations.append(place)
            else:
                recommendations.append(place)
    
    return recommendations

# Sidebar
st.sidebar.title("🧠 Expert System Wisata")
menu = st.sidebar.radio(
    "Pilih Menu",
    ["Home", "Input Kriteria", "Lihat Semua Data"]
)

# ======================
# HALAMAN HOME
# ======================
if menu == "Home":
    st.title("🏠 Selamat Datang di Expert System Rekomendasi Wisata")
    st.write("""
    Sistem ini membantu Anda menemukan tempat wisata yang sesuai dengan budget dan preferensi Anda.
    
    **Fitur:**
    - 🎯 Filter berdasarkan Budget (Cost)
    - 📍 Filter berdasarkan Kecamatan
    - 📊 Dapatkan rekomendasi tempat wisata terbaik
    - 💰 Info lengkap tentang range harga setiap tempat
    
    **Cara Menggunakan:**
    1. Buka menu "Input Kriteria"
    2. Masukkan budget Anda
    3. Pilih kecamatan (opsional)
    4. Sistem akan menampilkan rekomendasi tempat wisata
    """)

# ======================
# HALAMAN INPUT KRITERIA
# ======================
elif menu == "Input Kriteria":
    st.title("🎯 Input Kriteria Pencarian")
    
    # Fetch data
    data = fetch_data_from_api()
    
    if data:
        # Get unique kecamatan
        kecamatan_list = set()
        for place in data:
            kec = place.get("Domisili", {}).get("kecamatan")
            if kec:
                kecamatan_list.add(kec)
        kecamatan_list = sorted(list(kecamatan_list))
        
        # Input form
        col1, col2 = st.columns(2)
        
        with col1:
            budget = st.number_input(
                "💰 Budget Anda (dalam Rupiah)",
                min_value=0,
                value=100000,
                step=10000,
                help="Masukkan budget yang Anda miliki"
            )
        
        with col2:
            kecamatan = st.selectbox(
                "📍 Pilih Kecamatan (Opsional)",
                ["Semua Kecamatan"] + kecamatan_list,
                help="Pilih kecamatan yang Anda inginkan atau semua"
            )
            if kecamatan == "Semua Kecamatan":
                kecamatan = ""
        
        # Button untuk cari rekomendasi
        if st.button("🔍 Cari Rekomendasi", use_container_width=True, type="primary"):
            recommendations = filter_recommendations(data, budget, kecamatan)
            
            st.subheader("📋 Hasil Rekomendasi")
            
            if recommendations:
                st.success(f"✅ Ditemukan {len(recommendations)} tempat wisata yang sesuai dengan kriteria Anda!")
                
                # Tampilkan dalam bentuk cards
                for idx, place in enumerate(recommendations, 1):
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"### {idx}. {place.get('nama_tempat', 'N/A')}")
                            
                            # Info lokasi
                            domisili = place.get('Domisili', {})
                            st.write(f"**Lokasi:** {domisili.get('kecamatan', 'N/A')}, {domisili.get('kabupaten_kota', 'N/A')}")
                            st.write(f"**Provinsi:** {domisili.get('provinsi', 'N/A')}")
                        
                        with col2:
                            st.metric("ID", place.get('id', 'N/A'))
                        
                        # Info cost
                        cost_start = place.get('Cost_Start', 0)
                        cost_max = place.get('Cost_Max', 0)
                        st.write(f"💵 **Range Harga:** Rp {cost_start:,} - Rp {cost_max:,}")
                        st.write(f"✨ **Status:** Sesuai dengan budget Anda")
            else:
                st.warning("❌ Maaf, tidak ada tempat wisata yang sesuai dengan kriteria Anda. Coba ubah budget atau kecamatan Anda.")
                
                # Saran
                st.info("💡 **Saran:** Coba tingkatkan budget atau ubah kecamatan untuk hasil yang lebih banyak.")
    else:
        st.error("Gagal memuat data dari API")

# ======================
# HALAMAN LIHAT SEMUA DATA
# ======================
elif menu == "Lihat Semua Data":
    st.title("📊 Semua Data Tempat Wisata")
    
    data = fetch_data_from_api()
    
    if data:
        # Prepare dataframe
        df_data = []
        for place in data:
            df_data.append({
                "ID": place.get('id'),
                "Nama Tempat": place.get('nama_tempat'),
                "Kecamatan": place.get('Domisili', {}).get('kecamatan'),
                "Kabupaten/Kota": place.get('Domisili', {}).get('kabupaten_kota'),
                "Provinsi": place.get('Domisili', {}).get('provinsi'),
                "Cost Min (Rp)": place.get('Cost_Start'),
                "Cost Max (Rp)": place.get('Cost_Max'),
                "Dibuat": place.get('created_at')
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Summary
        st.subheader("📈 Statistik")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Tempat", len(data))
        
        with col2:
            avg_cost_start = df["Cost Min (Rp)"].mean()
            st.metric("Rata-rata Cost Min", f"Rp {avg_cost_start:,.0f}")
        
        with col3:
            avg_cost_max = df["Cost Max (Rp)"].mean()
            st.metric("Rata-rata Cost Max", f"Rp {avg_cost_max:,.0f}")
    else:
        st.error("Gagal memuat data dari API")
