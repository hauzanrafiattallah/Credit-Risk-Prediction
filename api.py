from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

try:
    with open('model_prediksi.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Error: File model_prediksi.pkl tidak ditemukan!")

class CreditScoringInput(BaseModel):
    person_age: int
    person_income: float
    person_home_ownership: str
    person_emp_length: float
    loan_intent: str
    loan_grade: str
    loan_amnt: float
    loan_int_rate: float
    loan_percent_income: float
    cb_person_default_on_file: str
    cb_person_cred_hist_length: int

@app.get("/")
def home():
    return {"message": "Credit Risk API is Running!"}

@app.post("/predict")
def predict_credit(data: CreditScoringInput):
    try:
        data_dict = data.dict()
        df = pd.DataFrame([data_dict])
        
        prediction = model.predict(df)
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