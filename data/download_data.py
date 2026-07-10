import os
import pandas as pd
import requests

def download_and_label_data():
    # Official URL for the Cleveland dataset file
    DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    
    # Define the official 14 feature names as specified in the UCI documentation
    COLUMNS = [
        "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", 
        "thalach", "exang", "oldpeak", "slope", "ca", "thal", "num"
    ]
    
    os.makedirs('data', exist_ok=True)
    raw_path = os.path.join('data', 'raw_heart_disease.csv')
    
    print(f"Downloading dataset from UCI (ID 45)...")
    
    # Read the headerless CSV directly from the URL and apply the column names
    try:
        df = pd.read_csv(DATA_URL, names=COLUMNS, na_values="?")
        
        # Save it locally as a clean, labeled CSV file
        df.to_csv(raw_path, index=False)
        print(f"Success! Labeled raw data saved to {raw_path}")
        print(f"Dataset shape: {df.shape}")
        
    except Exception as e:
        print(f"Error downloading or processing data: {e}")

if __name__ == "__main__":
    download_and_label_data()