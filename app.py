from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = joblib.load(model_path)

class HouseFeatures(BaseModel):
    City: str
    Locality_Tier: str
    Property_Type: str
    Furnishing_Status: str
    Status: str
    BHK: int
    Area_SqFt: int
    Bathrooms: int
    Balcony: int
    Age_of_Property: int

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/predict")
def predict_price(features: HouseFeatures):
    input_data = pd.DataFrame([features.dict()])
    
    prediction_lakhs = model.predict(input_data)[0]
    
    if prediction_lakhs >= 100:
        price_str = f"₹ {prediction_lakhs/100:.2f} Crores"
    else:
        price_str = f"₹ {prediction_lakhs:.2f} Lakhs"
        
    return {"estimated_price": price_str, "raw_lakhs": round(float(prediction_lakhs), 2)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
