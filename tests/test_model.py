
import pytest
import pandas as pd
import joblib
import os

@pytest.fixture
def sample_data():
    # Sample raw data matching the Heart Disease dataset features
    return pd.DataFrame({
        'age': [63, 37],
        'sex': [1, 1],
        'cp': [3, 2],
        'trestbps': [145, 130],
        'chol': [233, 250],
        'fbs': [1, 0],
        'restecg': [0, 1],
        'thalach': [150, 187],
        'exang': [0, 0],
        'oldpeak': [2.3, 3.5],
        'slope': [0, 0],
        'ca': [0, 0],
        'thal': [1, 2]
    })

def test_data_processing(sample_data):
    # Test that there are no missing values in the mock data
    assert sample_data.isnull().sum().sum() == 0
    # Test correct number of columns (13 features)
    assert sample_data.shape[1] == 13

def test_model_inference(sample_data):
    # Check if the model file exists
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'heart_disease_pipeline.pkl')    
    assert os.path.exists(MODEL_PATH), f"Model file {MODEL_PATH} not found."
    
    # Load model and test prediction
    model = joblib.load(MODEL_PATH)
    predictions = model.predict(sample_data)
    
    # Assertions
    assert len(predictions) == 2
    assert all(p in [0, 1] for p in predictions), "Predictions must be binary (0 or 1)."
