<p align="center">
  <img src="assets/icons/logo.png" alt="ClarityPredict Logo" width="160">
</p>

<h1 align="center">ClarityPredict</h1>
<p align="center">
  A transparent, clinically oriented machine‑learning platform for biomarker‑based risk prediction.
</p>

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" />
  <img src="https://img.shields.io/badge/Streamlit-1.32-red.svg" />
  <img src="https://img.shields.io/badge/SHAP-Explainable%20AI-green.svg" />
  <img src="https://img.shields.io/badge/XGBoost-Model-orange.svg" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  <img src="https://img.shields.io/badge/Last%20Updated-2026--02--25-lightgrey.svg" />
  <img src="https://img.shields.io/badge/Version-2.0.0-blueviolet.svg" />
</p>

---

##  Overview

ClarityPredict is a modular, explainable machine‑learning application built with Streamlit.  
The platform provides:

- **Biomarker exploration**
- **Interactive data visualization**
- **Explainable predictions using SHAP**
- **A clean, clinical UI built from reusable components**

The system is designed for transparency, reproducibility, and clinical relevance — making it suitable for academic work, prototyping, and decision‑support research.

---

##  Core Features

- **Prediction Engine**  
  Tree‑based regression model with full preprocessing pipeline (imputation + scaling)

- **Explainability**  
  SHAP summary plots, bar charts, and waterfall plots for transparent interpretation

- **Data Exploration**  
  Interactive visualizations of biomarker distributions and relationships

- **Modular Architecture**  
  Clean separation between UI, services, models, and data

- **Professional UI/UX**  
  Custom styling, consistent components, and a distraction‑free clinical layout

---

##  Project Structure

ClarityPredictV2/
│
├── app/
│   ├── components/      # Header, footer, metric cards, UI elements
│   ├── layout/          # Global CSS, branding, styling
│   ├── pages/           # Streamlit multipage views (Home, Explore, Prediction, About)
│   ├── services/        # PredictionService, SHAP logic, model loading
│   ├── utils/           # Formatting helpers, validators
│   └── main.py          # Streamlit entry point
│
├── models/              # Trained model + preprocessors
│   ├── model.pkl
│   ├── scaler.pkl
│   ├── imputer.pkl
│
├── data/
│   └── dataset.csv      # Training dataset
│
├── notebooks/
│   └── training_pipeline.ipynb
│
├── assets/
│   └── icons/           # Branding and UI icons
│
└── README.md


This structure ensures maintainability, clarity, and scalability.

---

##  Machine‑Learning Pipeline

ClarityPredict uses a reproducible and transparent ML workflow:

### **1. Dataset**
Biomarker dataset with six numerical features:  
`Age, BMI, Glucose, Insulin, HDL, LDL`

### **2. Preprocessing**
- Median imputation  
- Standard scaling  
- Fixed feature ordering  

### **3. Model Training**
- XGBoost Regressor  
- Hyperparameter tuning  
- Evaluation and selection  

### **4. Model Artifacts**
- `model.pkl`  
- `scaler.pkl`  
- `imputer.pkl`  

### **5. PredictionService**
- Loads model and preprocessors  
- Validates and prepares input  
- Generates prediction  
- Computes SHAP explanations  

### **6. Streamlit UI**
- Prediction page  
- Explore page  
- SHAP visualization  
- Interactive plots  

---

##  Explainability (SHAP)

ClarityPredict uses **SHAP (SHapley Additive exPlanations)** to provide transparent and clinically meaningful model interpretation.

The platform includes:

- **Summary plots** — global feature behavior  
- **Bar charts** — ranked feature contributions  
- **Waterfall plots** — detailed breakdown of a single prediction  
- **Local explanations** — how each biomarker influences the output  

This ensures every prediction is interpretable and grounded in measurable biomarker contributions.

---

##  Model Card

### **Model Type**
XGBoost Regressor (tree‑based)

### **Intended Use**
- Educational and research purposes  
- Biomarker‑based risk estimation  
- Demonstration of explainable ML pipelines  

### **Not Intended For**
- Clinical diagnosis  
- Treatment decisions  
- Real‑world patient risk assessment  

### **Training Data**
- 6 biomarker features  
- Cleaned and standardized dataset  
- Numerical inputs only  

### **Strengths**
- Fast inference  
- Strong performance on tabular data  
- High interpretability with SHAP  

### **Limitations**
- Limited to the training dataset distribution  
- Not validated for clinical deployment  
- Sensitive to out‑of‑range inputs  

---

##  How to Run

From the project root:

bash
streamlit run app/main.py
The application will open automatically in your browser.

---

## Technologies Used

- Python 3
- Streamlit
- Pandas / NumPy
- scikit‑learn
- XGBoost
- SHAP
- Matplotlib / Seaborn
- Custom CSS for branding

---

## Future Work

- Add model comparison tools
- Expand biomarker dataset
- Integrate uncertainty estimation
- Add user authentication
- Deploy as a cloud‑hosted application

---

# License

This project is for educational and demonstration purposes only.

---
<p align="center">
<b>ClarityPredict — Transparent. Explainable. Insightful.</b>
</p>
