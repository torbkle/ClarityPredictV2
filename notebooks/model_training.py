#%%

#%% md
# # ClarityPredict 2.0 – Model Training Notebook
# 
# Denne notebooken inneholder:
# - Lasting av datasett
# - EDA (utforskende dataanalyse)
# - Preprocessing (imputer + scaler)
# - Trening av tre modeller
# - Modell-sammenligning (MAE, RMSE, R²)
# - Lagring av beste modell
# 
# Dette er grunnlaget for rapportens tekniske kapittel.
# 
#%% md
# ## 1. Last inn datasettet
# 
#%%
import pandas as pd
import numpy as np
from pathlib import Path

df = pd.read_csv("../data/dataset.csv")
print("Loaded dataset with shape:", df.shape)
df.columns = df.columns.str.lower()
df.head()

#%% md
# ## 2. EDA – Utforskende dataanalyse
# 
# Vi ser på:
# - statistikk
# - manglende verdier
# - korrelasjoner
# 
#%%
print("\nBasic statistics:")
display(df.describe())

print("\nMissing values:")
display(df.isna().sum())

print("\nCorrelation matrix:")
display(df.corr())

#%% md
# ## 3. Preprocessing
# 
# Vi bruker:
# - Median-imputering
# - StandardScaler
# 
# Dette matcher produksjonskoden i PredictionService.
# 
#%%
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import pandas as pd

# Sørg for at df.columns allerede er gjort små:
df.columns = df.columns.str.lower()

features = ["age", "bmi", "glucose", "insulin", "hdl", "ldl"]

X = df[features]
y = df["target"]   # <-- endret fra "Target" til "target"

imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(X)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# Legg tilbake kolonnenavnene
X_scaled = pd.DataFrame(X_scaled, columns=features)

print("Imputer and scaler created.")


#%%
print(df.columns.tolist())

#%% md
# ## 4. Tren tre modeller
# 
# Modellene som trenes:
# - Linear Regression
# - RandomForestRegressor
# - XGBRegressor
# 
# Vi evaluerer med:
# - MAE
# - RMSE
# - R²
# 
#%%
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

models = {
    "LinearRegression": LinearRegression(),
    "RandomForestRegressor": RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),
    "XGBRegressor": XGBRegressor(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=42
    )
}

results = []

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_scaled, y)
    y_pred = model.predict(X_scaled)

    mae = mean_absolute_error(y, y_pred)
    rmse = mean_squared_error(y, y_pred) ** 0.5
    r2 = r2_score(y, y_pred)


    results.append({
        "model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    })

results_df = pd.DataFrame(results).sort_values(by="RMSE")
print("\nModel comparison:")
display(results_df)

#%% md
# ## 5. Velg beste modell
# 
# Vi velger modellen med lavest RMSE.
# 
#%%
best_row = results_df.iloc[0]
best_model_name = best_row["model"]
print(f"Selected best model: {best_model_name}")

final_model = models[best_model_name]

#%% md
# ## 6. Lagre modell og preprocessors
# 
# Disse filene brukes av Streamlit-appen:
# - model.pkl
# - scaler.pkl
# - imputer.pkl
# 
#%%
import joblib

BASE_DIR = Path.cwd().parents[0]
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)

joblib.dump(final_model, MODELS_DIR / "model.pkl")
joblib.dump(scaler, MODELS_DIR / "scaler.pkl")
joblib.dump(imputer, MODELS_DIR / "imputer.pkl")

print("\nSaved files:")
for f in MODELS_DIR.glob("*"):
    print("-", f)

#%% md
# ## Notebook ferdig
# 
# Modellen er trent, evaluert og lagret.
# Denne notebooken kan nå brukes direkte i rapporten.
# 
#%%
print(results_df.to_string())

#%%
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.show()

#%%
df.hist(figsize=(10,8))
plt.show()

#%%
plt.scatter(df["Glucose"], df["Insulin"])
plt.xlabel("Glucose")
plt.ylabel("Insulin")
plt.show()

#%%
from xgboost import plot_importance
plot_importance(final_model)
plt.show()


#%%
import shap

explainer = shap.TreeExplainer(final_model)
shap_values = explainer.shap_values(X_scaled)

shap.summary_plot(shap_values, X_scaled, feature_names=features)

#%%
shap.force_plot(explainer.expected_value, shap_values[0], X_test.iloc[0])

#%%

#%%
import matplotlib.pyplot as plt

models = ["Linear", "RandomForest", "XGBoost"]
rmse = [0.010381, 0.002777, 0.000502]

plt.bar(models, rmse)
plt.ylabel("RMSE")
plt.title("Model Comparison")
plt.show()

#%%
sample_list = [45, 27, 110, 80, 55, 120]
notebook_pred = final_model.predict([sample_list])
notebook_pred
