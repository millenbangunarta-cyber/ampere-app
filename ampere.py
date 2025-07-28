# Mengimpor library yang diperlukan
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import timezone
import os
import io

# Fungsi untuk mencatat data motor dan ampere, serta membuat grafik
def catat_data(nama_motor, ampere_motor):
    # Gunakan zona waktu Kalimantan Timur (WITA)
    tz = timezone('Asia/Makassar')
    waktu_input = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    
    # Validasi arus
    if ampere_motor > 100:
        status_ampere = "Warning: Arus terlalu tinggi!"
    else:
        status_ampere = "Arus normal."
    
    # Simpan data ke DataFrame
    data = pd.DataFrame([[waktu_input, nama_motor, ampere_motor, status_ampere]],
                        columns=["Waktu", "Nama Motor", "Arus (Ampere)", "Status"])

    # Simpan ke file CSV
    if os.path.exists("data_motor.csv"):
        data.to_csv("data_motor.csv", mode='a', header=False, index=False)
    else:
        data.to_csv("data_motor.csv", index=False)

    # Membuat grafik arus
    fig, ax = plt.subplots()
    df = pd.read_csv("data_motor.csv")
    
    # Filter grafik berdasarkan nama motor yang sama
    df = df[df["Nama Motor"] == nama_motor]
    
    ax.plot(pd.to_datetime(df["Waktu"]), df["Arus (Ampere)"], marker='o', color='orange', label="Arus (Ampere)")
    ax.set_xlabel("Waktu")
    ax.set_ylabel("Ampere (A)")
    ax.set_title(f"Tren Arus Motor: {nama_motor}")
    ax.legend()

    # Simpan grafik ke BytesIO
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    
    return f"Data berhasil disimpan!\nWaktu: {waktu_input}\nMotor: {nama_motor}\nArus: {ampere_motor} A\nStatus: {status_ampere}", buf

# --- Streamlit App ---

# Tambahkan styling background
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)),
            url("https://raw.githubusercontent.com/millenbangunarta-cyber/bearing-app/main/IMG_1714.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    label {
        color: white !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- INISIALISASI SESSION STATE ---
if "nama_motor" not in st.session_state:
    st.session_state.nama_motor = ""
if "ampere_motor" not in st.session_state:
    st.session_state.ampere_motor = 0.0  # <- Pastikan ini float
if "submit_result" not in st.session_state:
    st.session_state.submit_result = None
if "submit_chart" not in st.session_state:
    st.session_state.submit_chart = None

# Judul Aplikasi
st.markdown("<h1 style='color: white;'>⚡ Pencatatan Arus Motor</h1>", unsafe_allow_html=True)

# Input pengguna
nama_motor = st.text_input('🔧 Nama Motor', value=st.session_state.nama_motor, key="nama_motor")
ampere_motor = st.number_input(
    '⚡ Arus Motor (Ampere)',
    min_value=0.0,
    max_value=500.0,
    value=float(st.session_state.ampere_motor),  # <- Pastikan ini float juga
    step=0.1,
    key="ampere_motor"
)

# Fungsi ketika tombol submit ditekan
def submit_callback():
    if st.session_state.nama_motor.strip() == "":
        st.session_state.submit_result = "warning"
        st.session_state.submit_chart = None
    else:
        result, chart = catat_data(
            st.session_state.nama_motor,
            st.session_state.ampere_motor
        )
        st.session_state.submit_result = result
        st.session_state.submit_chart = chart

        # Reset input
        st.session_state.nama_motor = ""
        st.session_state.ampere_motor = 0.0

# Tombol submit
st.button("Submit", on_click=submit_callback)

# Tampilkan hasil jika ada
if st.session_state.submit_result:
    if st.session_state.submit_result == "warning":
        st.warning("Nama motor tidak boleh kosong.")
    else:
        st.success(st.session_state.submit_result)
        if st.session_state.submit_chart:
            st.image(st.session_state.submit_chart)

# Tombol download CSV
if os.path.exists("data_motor.csv"):
    with open("data_motor.csv", "rb") as file:
        st.download_button(label="📥 Unduh Data CSV", data=file, file_name="data_motor.csv")

# Footer
st.markdown(
    """
    <hr style="margin-top: 50px; margin-bottom: 10px;">
    <div style="text-align: center; color: gray; font-size: small;">
        &copy; 2025 Aplikasi Pencatatan Arus Motor - Made with ❤️ by millen as a planner BEP
    </div>
    """,
    unsafe_allow_html=True
)
