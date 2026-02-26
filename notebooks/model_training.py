"""
ClarityPredict 2.0 – Model Training Script
------------------------------------------

This script trains three regression models on the biomarker dataset:
- Linear Regression
- Random Forest Regressor
- XGBoost Regressor

It performs:
1. Dataset loading
2. Preprocessing (median imputation + standard scaling)
3. Train/test split
4. Model training and evaluation (MAE, RMSE, R²)
5. Selection of the best model
6. Saving of model, scaler, and imputer for production use

The output files are stored in: models/
"""

import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor


# ---------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "dataset.csv"
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------
logger.info("Loading dataset from %s", DATA_PATH)
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.lower()

features = ["age", "bmi", "glucose", "insulin", "hdl", "ldl"]
target = "target"

X = df[features]
y = df[target]

logger.info("Dataset loaded with shape: %s", df.shape)


# ---------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------
logger.info("Applying preprocessing (median imputation + scaling)")

imputer = SimpleImputer(strategy="median")
scaler = StandardScaler()

X_imputed = imputer.fit_transform(X)
X_scaled = scaler.fit_transform(X_imputed)


# ---------------------------------------------------------
# Train/test split
# ---------------------------------------------------------
logger.info("Performing train/test split (80/20)")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)


# ---------------------------------------------------------
# Model definitions
# ---------------------------------------------------------
models = {
    "LinearRegression": LinearRegression(),
    "RandomForestRegressor": RandomForestRegressor(
        n_estimators=300, random_state=42, n_jobs=-1
    ),
    "XGBRegressor": XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42,
    ),
}

results = []


# ---------------------------------------------------------
# Train and evaluate models
# ---------------------------------------------------------
logger.info("Training and evaluating models...")

for name, model in models.items():
    logger.info("Training %s", name)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)

    results.append({
        "model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    })

results_df = pd.DataFrame(results).sort_values(by="RMSE")
logger.info("Model comparison:\n%s", results_df)


# ---------------------------------------------------------
# Select best model
# ---------------------------------------------------------
best_model_name = results_df.iloc[0]["model"]
best_model = models[best_model_name]

logger.info("Selected best model: %s", best_model_name)


# ---------------------------------------------------------
# Save model and preprocessors
# ---------------------------------------------------------
logger.info("Saving model and preprocessors to %s", MODELS_DIR)

joblib.dump(best_model, MODELS_DIR / "model.pkl")
joblib.dump(scaler, MODELS_DIR / "scaler.pkl")
joblib.dump(imputer, MODELS_DIR / "imputer.pkl")

logger.info("Training complete. Files saved:")
for f in MODELS_DIR.glob("*"):
    logger.info(" - %s", f)
