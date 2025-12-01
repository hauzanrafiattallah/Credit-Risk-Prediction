# app.py
import streamlit as st
import requests

# Set konfigurasi halaman
st.set_page_config(page_title="Credit Risk Prediction", page_icon="💰")

st.title("💰 Aplikasi Prediksi Risiko Kredit")
st.write("Isi formulir di bawah ini untuk memprediksi apakah pinjaman akan disetujui atau berisiko macet.")

# --- Form Input User ---
with st.form("credit_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Pemohon")
        person_age = st.number_input("Usia (Tahun)", min_value=18, max_value=100, value=25)
        person_income = st.number_input("Pendapatan Tahunan ($)", min_value=0, value=80000)
        person_emp_length = st.number_input("Lama Bekerja (Tahun)", min_value=0.0, value=5.0)
        
        # Dropdown untuk Home Ownership
        home_ownership_options = ["RENT", "OWN", "MORTGAGE", "OTHER"]
        person_home_ownership = st.selectbox("Status Kepemilikan Rumah", home_ownership_options)
        
        # Dropdown untuk Default History
        default_options = ["Y", "N"]
        cb_person_default_on_file = st.selectbox("Pernah Gagal Bayar Sebelumnya? (Y/N)", default_options)
        cb_person_cred_hist_length = st.number_input("Panjang Riwayat Kredit (Tahun)", min_value=0, value=4)

    with col2:
        st.subheader("Data Pinjaman")
        loan_amnt = st.number_input("Jumlah Pinjaman ($)", min_value=0, value=15000)
        
        # Dropdown untuk Loan Intent
        intent_options = ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"]
        loan_intent = st.selectbox("Tujuan Pinjaman", intent_options)
        
        # Dropdown untuk Loan Grade
        grade_options = ["A", "B", "C", "D", "E", "F", "G"]
        loan_grade = st.selectbox("Grade Pinjaman", grade_options)
        
        loan_int_rate = st.number_input("Suku Bunga (%)", min_value=0.0, value=11.5)
        loan_percent_income = st.number_input("Persentase Pinjaman thd Pendapatan (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.25, step=0.01)

    # Tombol Submit
    submitted = st.form_submit_button("Prediksi Risiko")

# --- Logika Pengiriman Data ---
if submitted:
    # 1. Siapkan payload data (harus sama persis dengan kunci di api.py)
    payload = {
        "person_age": int(person_age),
        "person_income": float(person_income),
        "person_home_ownership": person_home_ownership,
        "person_emp_length": float(person_emp_length),
        "loan_intent": loan_intent,
        "loan_grade": loan_grade,
        "loan_amnt": float(loan_amnt),
        "loan_int_rate": float(loan_int_rate),
        "loan_percent_income": float(loan_percent_income),
        "cb_person_default_on_file": cb_person_default_on_file,
        "cb_person_cred_hist_length": int(cb_person_cred_hist_length)
    }

    # 2. Kirim ke API FastAPI
    # Ganti URL jika sudah deploy global (misal: https://nama-app.onrender.com/predict)
    api_url = "http://127.0.0.1:8000/predict" 
    
    with st.spinner("Sedang memproses data..."):
        try:
            response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                status = result['prediction_status']
                
                # Tampilkan Hasil
                if result['prediction_code'] == 0:
                    st.success(f"✅ Hasil: {status}")
                    st.balloons()
                else:
                    st.error(f"⚠️ Hasil: {status}")
                    st.write("Pinjaman ini memiliki risiko tinggi untuk gagal bayar.")
            else:
                st.error(f"Error dari server: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("Gagal terhubung ke server API. Pastikan uvicorn sedang berjalan!")