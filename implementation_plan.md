# Indian House Price Prediction - B.Tech Major Project

This project aims to build a comprehensive end-to-end Machine Learning solution for predicting House Prices in India. Since it's a B.Tech Major Project, it is designed to achieve high accuracy and be presented with a professional, visually stunning web application. 

The project will be split into three core phases:

## Phase 1: Synthetic Dataset Generation (`dataset_generator.py`)
We will algorithmically generate a large, realistic Indian Real Estate dataset (approx. 50,000 rows) anchored in **actual real estate base rates for 2025/2026**. 
- **Features generated:** 
  - `City` and corresponding true-to-market base rates: 
    - **Mumbai** (~₹14,000/sqft base, higher for premium localities)
    - **Bengaluru** (~₹9,500/sqft)
    - **Delhi-NCR** (~₹9,167/sqft)
    - **Hyderabad** (~₹7,000/sqft)
    - **Pune** (~₹5,000/sqft)
  - `Locality` / `Area Tier` (Premium, Mid-segment, Affordable) - applies multipliers (e.g., Premium adds 40-60% to base price).
  - `BHK` (1 to 5), `Area_SqFt` (scaled rationally based on BHK).
  - `Bathrooms`, `Balcony`, `Furnishing_Status`, `Property_Type` (Apartment, Villa), `Status`.
- **Target Variable:** `Price` (calculated intelligently by multiplying Base Rate × SqFt × Locality Premium × Amenities Multiplier, adding Gaussian noise to simulate varied market conditions).

## Phase 2: High-Accuracy Machine Learning Pipeline (`model_pipeline.py`)
To achieve high accuracy, we won't just stop at basic Linear Regression. 
- **Preprocessing:** One-Hot Encoding for categorical features, Robust Scaling for numerical features to handle any outliers.
- **Model Selection:** We will train and compare Advanced Ensemble Models:
  - Random Forest Regressor
  - XGBoost Regressor (Highly recommended for tabular data)
  - LightGBM Regressor
- **Evaluation:** Using R² Score, MAE, and RMSE.
- **Export:** The best performing model pipeline will be saved as `model.pkl` along with feature columns.

## Phase 3: Stunning Web Application UI (`app.py` & `/static`)
To impress your examiners and reviewers, we will build a modern Web Dashboard:
- **Backend:** Fast API built with Flask or FastAPI.
- **Frontend:** A beautiful, responsive web interface built with HTML, CSS, and JS. It will feature modern aesthetics:
  - Premium Dark Mode / Glassmorphism UI.
  - Smooth micro-animations.
  - Interactive prediction forms.

---

## User Review Required

> [!NOTE]
> Please review this plan! 
> 
> A B.Tech major project implies you need a complete submission. This plan includes generating data, training an accurate model, and creating a modern Web UI to showcase it to your examiners.

## Proposed Changes

### Machine Learning Core
#### [NEW] [dataset_generator.py](file:///d:/house price prediction/dataset_generator.py)
Script to generate the Indian real estate dataset using pandas and numpy.
#### [NEW] [model_pipeline.py](file:///d:/house price prediction/model_pipeline.py)
Script to read `dataset.csv`, build the preprocessing steps, train XGBoost/RandomForest, evaluate accuracy, and save models.

### Web Application
#### [NEW] [app.py](file:///d:/house price prediction/app.py)
FastAPI backend to serve the web application and expose prediction endpoints.
#### [NEW] [index.html](file:///d:/house price prediction/static/index.html)
The stunning frontend UI for user interactions.
#### [NEW] [style.css](file:///d:/house price prediction/static/style.css)
The CSS styling with premium aesthetics (dark mode, glassmorphism).

## Open Questions

1. **Dataset Size:** I will generate **50,000 rows**. Is this size acceptable?
2. **Frameworks:** I planned to use `FastAPI` (Python) and a custom frontend. Do you prefer another framework like Flask or Streamlit?
3. **Accuracy Goals:** Do you have any specific accuracy goals in mind (e.g. >90%)?

## Verification Plan
1. Generate the dataset and inspect `dataset.csv`.
2. Run model training script and verify accuracy logs (aiming for >90% R2).
3. Launch the web server locally and test predictions via the web UI.
