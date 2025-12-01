import streamlit as st
import pandas as pd
import pickle

# --- 1. Load Model Langsung di Sini ---
@st.cache_resource
def load_model():
    try:
        with open('model_prediksi.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("File 'model_prediksi.pkl' tidak ditemukan. Pastikan file ada di folder yang sama.")
        return None

model = load_model()

# --- 2. Tampilan (UI) ---
st.set_page_config(page_title="Credit Risk App (Simple)", page_icon="💰")
st.title("💰 Cek Kelayakan Pinjaman (Versi Simpel)")
st.write("Aplikasi ini berjalan tanpa API terpisah, mirip project Green Cure.")

# Form Input
with st.form("form_kredit"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Diri")
        age = st.number_input("Usia", 18, 100, 25)
        income = st.number_input("Pendapatan Tahunan ($)", 0, 10000000, 80000)
        emp_len = st.number_input("Lama Kerja (Tahun)", 0.0, 60.0, 5.0)
        home = st.selectbox("Kepemilikan Rumah", ["RENT", "OWN", "MORTGAGE", "OTHER"])
        default = st.selectbox("Pernah Gagal Bayar?", ["Y", "N"])
        hist_len = st.number_input("Lama Histori Kredit", 0, 60, 4)
        
    with col2:
        st.subheader("Data Pinjaman")
        amnt = st.number_input("Jumlah Pinjaman ($)", 0, 1000000, 15000)
        intent = st.selectbox("Tujuan", ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"])
        grade = st.selectbox("Grade Pinjaman", ["A", "B", "C", "D", "E", "F", "G"])
        rate = st.number_input("Bunga (%)", 0.0, 100.0, 11.5)
        percent = st.number_input("Persen Income (0.0 - 1.0)", 0.0, 1.0, 0.25)

    submitted = st.form_submit_button("Cek Prediksi")

# --- 3. Logika Prediksi (Langsung di file ini) ---
if submitted and model is not None:
    # Siapkan DataFrame (sama persis seperti saat training)
    input_data = pd.DataFrame([{
        "person_age": int(age),
        "person_income": float(income),
        "person_home_ownership": home,
        "person_emp_length": float(emp_len),
        "loan_intent": intent,
        "loan_grade": grade,
        "loan_amnt": float(amnt),
        "loan_int_rate": float(rate),
        "loan_percent_income": float(percent),
        "cb_person_default_on_file": default,
        "cb_person_cred_hist_length": int(hist_len)
    }])

    # Prediksi langsung pakai variabel 'model'
    try:
        prediction = model.predict(input_data)
        hasil = int(prediction[0])
        
        # Tampilkan Hasil
        if hasil == 0:
            st.success("✅ **Disetujui!** Risiko Rendah (Aman)")
            st.balloons()
        else:
            st.error("⚠️ **Ditolak!** Risiko Tinggi (Berpotensi Macet)")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")