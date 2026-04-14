import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor

def build_and_train_model():
    print("Loading dataset...")
    data_path = os.path.join(os.path.dirname(__file__), 'dataset.csv')
    df = pd.parse_csv(data_path) if hasattr(pd, 'parse_csv') else pd.read_csv(data_path)
    
    X = df.drop(columns=['Price', 'Price_Lakhs'])
    y = df['Price_Lakhs']
    
    print("Splitting data into train/test...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    categorical_features = ['City', 'Locality_Tier', 'Property_Type', 'Furnishing_Status', 'Status']
    numerical_features = ['BHK', 'Area_SqFt', 'Bathrooms', 'Balcony', 'Age_of_Property']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
        ])
    
    print("Building XGBoost Pipeline...")
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=6,
            random_state=42,
            n_jobs=-1
        ))
    ])
    
    print("Training model (this might take a few seconds)...")
    model_pipeline.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model_pipeline.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    
    print("\n" + "="*30)
    print(" MODEL EVALUATION METRICS")
    print("="*30)
    print(f"R2 Score: {r2*100:.2f}%")
    print(f"MAE: Rs. {mae:.2f} Lakhs")
    print(f"RMSE: Rs. {rmse:.2f} Lakhs")
    print("="*30 + "\n")
    
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    joblib.dump(model_pipeline, model_path)
    print(f"Model saved successfully at: {model_path}")

if __name__ == "__main__":
    build_and_train_model()
