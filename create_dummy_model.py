# create_dummy_model.py

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from pathlib import Path

# Ensure folder exists
Path("models").mkdir(exist_ok=True)

# Feature names expected by PredictionService
feature_names = ["age", "bmi", "glucose", "insulin", "hdl", "ldl"]

# Create dummy dataset with correct column names
X = pd.DataFrame(np.random.rand(20, 6), columns=feature_names)
y = np.random.rand(20)

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "models/model.pkl")

print("Dummy model saved with correct feature names.")
