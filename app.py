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

dataset_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')
df = pd.read_csv(dataset_path) if os.path.exists(dataset_path) else None

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

class RecommendationRequest(BaseModel):
    City: str
    BHK: int
    predicted_price_lakhs: float

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

@app.post("/recommendations")
def get_recommendations(req: RecommendationRequest):
    if df is None:
        return {"recommendations": []}
    
    # Filter by same city
    city_df = df[df['City'] == req.City]
    
    if city_df.empty:
        return {"recommendations": []}
        
    # Calculate price difference percentage
    city_df = city_df.copy()
    city_df['Price_Diff'] = abs(city_df['Price_Lakhs'] - req.predicted_price_lakhs) / req.predicted_price_lakhs
    
    # Calculate BHK difference
    city_df['BHK_Diff'] = abs(city_df['BHK'] - req.BHK)
    
    # Score: lower is better. Heavily penalize different BHKs and large price differences
    city_df['Score'] = city_df['Price_Diff'] + (city_df['BHK_Diff'] * 0.5)
    
    # Get top 4 similar properties
    top_recommendations = city_df.sort_values(by='Score').head(4)
    
    recs = []
    for _, row in top_recommendations.iterrows():
        recs.append({
            "City": row['City'],
            "Locality_Tier": row['Locality_Tier'],
            "Property_Type": row['Property_Type'],
            "BHK": int(row['BHK']),
            "Area_SqFt": int(row['Area_SqFt']),
            "Price_Lakhs": float(row['Price_Lakhs'])
        })
        
    return {"recommendations": recs}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
