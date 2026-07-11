
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

# Set up standard API logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("HeartDiseaseAPI")

app = FastAPI(title="Heart Disease Prediction API with Monitoring")

# Custom Prometheus Metrics for Data Drift and Model Monitoring
PREDICTION_COUNTER = Counter("model_predictions_total", "Total predictions made", ["prediction_result"])
AGE_HISTOGRAM = Histogram("patient_age_distribution", "Distribution of patient ages")
CONFIDENCE_HISTOGRAM = Histogram("model_confidence_score", "Distribution of prediction confidence")

try:
    model = joblib.load("heart_disease_prediction_logistic_regression.pkl")
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise RuntimeError(f"Failed to load model: {e}")

class PatientData(BaseModel):
    age: float
    sex: int
    cp: int
    trestbps: float
    chol: float
    fbs: int
    restecg: int
    thalach: float
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

@app.post("/predict")
def predict(data: PatientData):
    logger.info(f"Received prediction request for age: {data.age}, chol: {data.chol}")
    try:
        input_data = pd.DataFrame([data.dict()])
        
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        confidence = np.max(probabilities)
        
        # Log to Prometheus
        PREDICTION_COUNTER.labels(prediction_result=str(prediction)).inc()
        AGE_HISTOGRAM.observe(data.age)
        CONFIDENCE_HISTOGRAM.observe(confidence)
        
        logger.info(f"Prediction: {prediction}, Confidence: {confidence:.2f}")
        
        return {
            "prediction": int(prediction),
            "confidence_score": float(confidence)
        }
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Heart Disease Prediction API is running."}

# Instrument the app to expose standard HTTP metrics
Instrumentator().instrument(app).expose(app)
