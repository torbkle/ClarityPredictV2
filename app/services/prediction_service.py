# prediction_service.py
# Core prediction and explainability logic for ClarityPredict 2.0

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, List

import joblib
import numpy as np
import pandas as pd
import shap

# Project root (two levels up from this file: app/services/ -> app/ -> project root)
BASE_DIR = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


# ---------------------------------------------------------
# Data structures
# ---------------------------------------------------------
@dataclass
class PredictionResult:
    input_df: pd.DataFrame
    prediction: float
    shap_values: Any


# ---------------------------------------------------------
# Prediction service
# ---------------------------------------------------------
class PredictionService:
    """
    Handles model loading, preprocessing, prediction,
    and SHAP-based explainability for ClarityPredict 2.0.
    """

    def __init__(
        self,
        model_path: str,
        expected_features: Optional[List[str]] = None,
        background_sample_size: int = 200,
        background_shap_sample: int = 50,
    ):
        # Resolve model path relative to project root
        self.model_path = BASE_DIR / model_path

        # Core components
        self.model = None
        self.scaler = None
        self.imputer = None
        self.explainer = None

        # Feature schema
        self.expected_features = expected_features

        # SHAP background settings
        self.background_sample_size = background_sample_size
        self.background_shap_sample = background_shap_sample
        self._background_data: Optional[np.ndarray] = None

        logger.info("Initializing PredictionService with model_path=%s", self.model_path)

        # Load components
        self._load_model()
        self._load_preprocessors()

        # Ensure expected_features is set BEFORE SHAP initialization
        self._set_expected_features()

        # Initialize SHAP components
        self._init_background_data()
        self._init_explainer()

    # ---------------------------------------------------------
    # MODEL LOADING
    # ---------------------------------------------------------
    def _load_model(self) -> None:
        if not self.model_path.exists():
            logger.error("Model file not found: %s", self.model_path)
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        logger.info("Loading model from %s", self.model_path)
        self.model = joblib.load(self.model_path)
        print("MODEL FEATURES:", getattr(self.model, "feature_names_in_", None))
        logger.info("Model loaded successfully: %s", type(self.model))

    def _load_preprocessors(self) -> None:
        """Load scaler and imputer saved during training."""
        scaler_path = BASE_DIR / "models/scaler.pkl"
        imputer_path = BASE_DIR / "models/imputer.pkl"

        if not scaler_path.exists() or not imputer_path.exists():
            raise FileNotFoundError(
                f"Preprocessor files not found. Expected: {scaler_path}, {imputer_path}"
            )

        self.scaler = joblib.load(scaler_path)
        self.imputer = joblib.load(imputer_path)

        logger.info("Scaler loaded: %s", type(self.scaler))
        logger.info("Imputer loaded: %s", type(self.imputer))

    # ---------------------------------------------------------
    # FEATURE HANDLING
    # ---------------------------------------------------------
    def _set_expected_features(self) -> None:
        """
        Ensures expected_features is set before SHAP initialization.
        Priority:
        1. Explicitly provided by user
        2. Inferred from model.feature_names_in_
        3. Hardcoded fallback (training schema)
        """
        if self.expected_features:
            logger.info("Using explicitly provided expected_features: %s", self.expected_features)
            return

        if hasattr(self.model, "feature_names_in_"):
            self.expected_features = list(self.model.feature_names_in_)
            logger.info("Inferred expected_features from model: %s", self.expected_features)
            return

        # FINAL fallback — must match training schema and UI
        self.expected_features = ["age", "bmi", "glucose", "insulin", "hdl", "ldl"]
        logger.warning(
            "Model has no feature_names_in_. Falling back to default expected_features: %s",
            self.expected_features,
        )

    # ---------------------------------------------------------
    # BACKGROUND DATA FOR SHAP
    # ---------------------------------------------------------
    def _init_background_data(self) -> None:
        if not self.expected_features:
            raise RuntimeError("expected_features must be set before initializing background data.")

        n_features = len(self.expected_features)
        logger.info(
            "Initializing synthetic background data: rows=%d, features=%d",
            self.background_sample_size,
            n_features,
        )

        rng = np.random.default_rng(seed=42)
        self._background_data = rng.random((self.background_sample_size, n_features))

    # ---------------------------------------------------------
    # SHAP EXPLAINER INITIALIZATION
    # ---------------------------------------------------------
    def _init_explainer(self) -> None:
        logger.info("Initializing SHAP explainer...")

        try:
            self.explainer = shap.TreeExplainer(self.model)
            logger.info("Using SHAP TreeExplainer.")
        except Exception as e:
            logger.warning("TreeExplainer failed (%s). Falling back to KernelExplainer.", e)

            if self._background_data is None:
                raise RuntimeError("No background data available for KernelExplainer.")

            background = shap.sample(self._background_data, self.background_shap_sample)
            self.explainer = shap.KernelExplainer(self.model.predict, background)
            logger.info("Using SHAP KernelExplainer with background shape=%s", background.shape)

    # ---------------------------------------------------------
    # INPUT PREPARATION
    # ---------------------------------------------------------
    def prepare_input(self, input_dict: Dict[str, Any]) -> pd.DataFrame:
        print("INPUT RECEIVED:", input_dict)
        print("EXPECTED FEATURES:", self.expected_features)
        logger.info("Preparing input data: %s", input_dict)

        # Create DataFrame from input
        df = pd.DataFrame([input_dict])

        # Ensure all expected features are present
        missing = [f for f in self.expected_features if f not in df.columns]
        if missing:
            raise ValueError(f"Missing required features: {missing}")

        # Ensure correct feature order
        df = df[self.expected_features]

        # Convert to numeric
        df = df.apply(pd.to_numeric, errors="coerce")

        # Impute missing values
        df_imputed = self.imputer.transform(df)

        # Scale values
        df_scaled = self.scaler.transform(df_imputed)

        return pd.DataFrame(df_scaled, columns=self.expected_features)

    # ---------------------------------------------------------
    # PREDICTION
    # ---------------------------------------------------------
    def predict(self, input_df: pd.DataFrame) -> float:
        logger.info("Running prediction on input shape %s", input_df.shape)
        pred = float(self.model.predict(input_df)[0])
        logger.info("Prediction result: %f", pred)
        return pred

    # ---------------------------------------------------------
    # SHAP EXPLANATION
    # ---------------------------------------------------------
    def explain(self, input_df: pd.DataFrame):
        if self.explainer is None:
            raise RuntimeError("SHAP explainer is not initialized.")

        logger.info("Computing SHAP values for input shape %s", input_df.shape)
        explanation = self.explainer(input_df)

        # Ensure we always return something UI‑vennlig
        # explanation.values -> numpy array of shape (n_samples, n_features)
        return explanation

    # ---------------------------------------------------------
    # FULL PIPELINE
    # ---------------------------------------------------------
    def run(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Running full prediction pipeline.")
        df = self.prepare_input(input_dict)
        prediction = self.predict(df)
        shap_explanation = self.explain(df)

        return {
            "input_df": df,
            "prediction": prediction,
            "shap_values": shap_explanation.values,  # array (1, n_features)
            "base_value": float(shap_explanation.base_values[0]),  # <-- THIS MUST EXIST
            "feature_names": self.expected_features,
        }



