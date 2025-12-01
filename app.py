import streamlit as st
import pandas as pd
import pickle

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

st.set_page_config(page_title="Aplikasi Prediksi Risiko Kredit", page_icon="💰")
st.title("💰 Aplikasi Prediksi Risiko Kredit")
st.write("Isi formulir di bawah ini untuk memprediksi apakah pinjaman akan disetujui atau berisiko macet.")

with st.form("form_kredit"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Pemohon")
        age = st.number_input("Usia (Tahun)", 18, 100, 22)
        income = st.number_input("Pendapatan Tahunan ($)", 0, 10000000, 25000)
        emp_len = st.number_input("Lama Bekerja (Tahun)", 0.0, 60.0, 1.0)
        home = st.selectbox("Status Kepemilikan Rumah", ["RENT", "OWN", "MORTGAGE", "OTHER"])
        default = st.selectbox("Pernah Gagal Bayar Sebelumnya? (Y/N)", ["Y", "N"])
        hist_len = st.number_input("Panjang Riwayat Kredit (Tahun)", 0, 60, 3)
        
    with col2:
        st.subheader("Data Pinjaman")
        amnt = st.number_input("Jumlah Pinjaman ($)", 0, 1000000, 15000)
        intent = st.selectbox("Tujuan Pinjaman", ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"])
        grade = st.selectbox("Grade Pinjaman", ["A", "B", "C", "D", "E", "F", "G"], index=3)
        rate = st.number_input("Suku Bunga (%)", 0.0, 100.0, 16.50)
        percent = st.number_input("Persentase Pinjaman thd Pendapatan (0.0 - 1.0)", 0.0, 1.0, 0.60)

    submitted = st.form_submit_button("Prediksi Risiko")

if submitted and model is not None:
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

    try:
        prediction = model.predict(input_data)
        hasil = int(prediction[0])
        
        if hasil == 0:
            st.success("✅ Hasil: Disetujui (Risiko Rendah)")
            st.write("Pinjaman ini aman untuk disetujui.")
            st.balloons()
        else:
            st.error("⚠️ Hasil: Ditolak (Risiko Tinggi)")
            st.write("Pinjaman ini memiliki risiko tinggi untuk gagal bayar.")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses data: {e}")