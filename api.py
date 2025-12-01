# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd

# Inisialisasi Aplikasi
app = FastAPI()

# --- 1. Load Model ---
# Pastikan nama file model sesuai dengan yang ada di folder Anda
try:
    with open('model_prediksi.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Error: File model_prediksi.pkl tidak ditemukan!")

# --- 2. Definisikan Schema Input (Sesuai Atribut Credit Risk) ---
class CreditScoringInput(BaseModel):
    person_age: int
    person_income: float
    person_home_ownership: str  # Contoh: RENT, OWN, MORTGAGE
    person_emp_length: float
    loan_intent: str            # Contoh: PERSONAL, EDUCATION
    loan_grade: str             # Contoh: A, B, C, D
    loan_amnt: float
    loan_int_rate: float
    loan_percent_income: float
    cb_person_default_on_file: str # Y atau N
    cb_person_cred_hist_length: int

@app.get("/")
def home():
    return {"message": "Credit Risk API is Running!"}

# --- 3. Endpoint Prediksi ---
@app.post("/predict")
def predict_credit(data: CreditScoringInput):
    try:
        # Ubah data dari format JSON (Pydantic) ke Dictionary
        data_dict = data.dict()
        
        # Ubah ke pandas DataFrame (Sesuai format training model Anda)
        # Ini penting agar nama kolom persis sama dengan saat training
        df = pd.DataFrame([data_dict])
        
        # Lakukan prediksi
        # Hasil biasanya berupa array, misal [0] atau [1]
        prediction = model.predict(df)
        
        # (Opsional) Jika model punya predict_proba untuk melihat probabilitas
        # probability = model.predict_proba(df).max() 
        
        # Kembalikan hasil ke user
        # Asumsi: 0 = Tidak Default (Aman), 1 = Default (Macet)
        result = int(prediction[0])
        
        if result == 0:
            status = "Disetujui (Risiko Rendah)"
        else:
            status = "Ditolak (Risiko Tinggi)"
            
        return {
            "prediction_code": result,
            "prediction_status": status
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))