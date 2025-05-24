import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from analysis import (
    plot_residuals, add_feature_engineering, select_top_features,
    plot_mae_by_bin, plot_mae_by_type,
    plot_model_metrics_bar, plot_boxplot_surface
)
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# Leximi dhe pastrimi i dataset-it (datapreprocessing)
df = pd.read_csv("dataset.csv", encoding="utf-8")
df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df.drop(columns=["Url", "Emri"], inplace=True)

def clean_price(price):
    if isinstance(price, str):
        price = price.lower().replace("çmimi sipas kërkesës", "")
        price = price.replace(",", "").replace("€", "").replace("lek", "").strip()
        return pd.to_numeric(price, errors='coerce')
    return price

df["Cmimi"] = df["Cmimi"].apply(clean_price)
df = df[df["Cmimi"].notna() & (df["Cmimi"] > 1000) & (df["Cmimi"] < 1_000_000)]

def simplify_lloji(value):
    if isinstance(value, str):
        value = value.lower()
        if "apartament" in value:
            return "Apartament"
        elif "vilë" in value or "shtepi" in value:
            return "Vile"
        elif "tokë" in value:
            return "Toke"
        elif "magazinë" in value or "komercial" in value:
            return "Komercial"
    return "Tjeter"

df["Lloji"] = df["Lloji"].apply(simplify_lloji)
df["Cmimi_per_m2"] = df["Cmimi"] / df["Siperfaqe Totale"]
df["Vendndodhja"] = df["Qyteti"].fillna("") + " - " + df["Zona"].fillna("")
df.drop(columns=["Zona", "Qyteti"], inplace=True)
df.dropna(subset=["Siperfaqe Totale", "Siperfaqe e Brendshme", "Dhoma Gjumi"], inplace=True)

# Veçoritë për modelim
features = [
    "Siperfaqe Totale", "Siperfaqe e Brendshme", "Dhoma Gjumi", "Kati",
    "Statusi", "Lloji", "Mobiluar", "Shikime", "Hipoteka", "Gjendja",
    "Qera", "Cmimi_per_m2", "Vendndodhja"
]

X = df[features]
y = df["Cmimi"]

cat_cols = X.select_dtypes(include="object").columns.tolist()
num_cols = X.select_dtypes(include=["float64", "int64"]).columns.tolist()

preprocessor = ColumnTransformer([
    ("num", Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ]), num_cols),
    ("cat", Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]), cat_cols)
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelet
xgb_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", XGBRegressor(n_estimators=200, learning_rate=0.1, max_depth=7, random_state=42))
])

rf_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42))
])

xgb_pipeline.fit(X_train, y_train)
rf_pipeline.fit(X_train, y_train)

xgb_preds = xgb_pipeline.predict(X_test)
rf_preds = rf_pipeline.predict(X_test)

xgb_preds_train = xgb_pipeline.predict(X_train)
rf_preds_train = rf_pipeline.predict(X_train)

# Metrica
xgb_r2 = r2_score(y_test, xgb_preds)
xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_preds))
xgb_mae = mean_absolute_error(y_test, xgb_preds)

xgb_r2_train = r2_score(y_train, xgb_preds_train)
xgb_rmse_train = np.sqrt(mean_squared_error(y_train, xgb_preds_train))
xgb_mae_train = mean_absolute_error(y_train, xgb_preds_train)

rf_r2 = r2_score(y_test, rf_preds)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
rf_mae = mean_absolute_error(y_test, rf_preds)

rf_r2_train = r2_score(y_train, rf_preds_train)
rf_rmse_train = np.sqrt(mean_squared_error(y_train, rf_preds_train))
rf_mae_train = mean_absolute_error(y_train, rf_preds_train)

print("\nModel Comparison")
print("------------------------------")
print("XGBoost")
print(f" Train  | R²: {xgb_r2_train:.4f} | RMSE: €{xgb_rmse_train:,.2f} | MAE: €{xgb_mae_train:,.2f}")
print(f" Test   | R²: {xgb_r2:.4f}       | RMSE: €{xgb_rmse:,.2f}       | MAE: €{xgb_mae:,.2f}")
print("\nRandom Forest")
print(f" Train  | R²: {rf_r2_train:.4f} | RMSE: €{rf_rmse_train:,.2f} | MAE: €{rf_mae_train:,.2f}")
print(f" Test   | R²: {rf_r2:.4f}       | RMSE: €{rf_rmse:,.2f}       | MAE: €{rf_mae:,.2f}")

# Vizualizime plot
plot_residuals(X_test, y_test, rf_preds)
df = add_feature_engineering(df)
X_processed = preprocessor.fit_transform(X)
feature_names = num_cols + list(preprocessor.named_transformers_["cat"]["encoder"].get_feature_names_out(cat_cols))
select_top_features(X_processed, y, feature_names)

X_test_copy = X_test.copy()
X_test_copy["Cmimi_Real"] = y_test.values
X_test_copy["Parashikim"] = rf_preds

X_test_copy.to_csv("rezultatet.csv", index=False)

plot_mae_by_bin(X_test_copy.assign(Lloji=X_test["Lloji"], ABP_Bin=df.loc[X_test.index, "ABP_Bin"]))
plot_mae_by_type(X_test_copy.assign(Lloji=X_test["Lloji"]))
plot_model_metrics_bar(xgb_rmse, xgb_mae, rf_rmse, rf_mae)
plot_boxplot_surface(df)
