import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, f_regression
import seaborn as sns
import os

def plot_residuals(X_test, y_test, preds):
    os.makedirs("grafiket", exist_ok=True)
    residuals = y_test - preds
    plt.figure(figsize=(8, 5))
    plt.scatter(X_test["Siperfaqe Totale"], residuals, alpha=0.4)
    plt.axhline(y=0, color='red', linestyle='--')
    plt.title("Gabimet (Residuals) vs Siperfaqe Totale")
    plt.xlabel("Siperfaqe Totale (m²)")
    plt.ylabel("Gabimi (Çmimi Real - i Parashikuar)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("grafiket/residuals_vs_siperfaqe.png")
    plt.close()

def add_feature_engineering(df):
    df["Viti_Ndertimit"] = pd.to_numeric(df.get("Viti_Ndertimit", np.nan), errors="coerce")
    df["Mosha"] = 2024 - df["Viti_Ndertimit"]
    df["ABP_Bin"] = pd.cut(df["Siperfaqe Totale"], bins=[0, 50, 100, 150, 200, 500, np.inf],
                           labels=["<50m²", "50-100", "100-150", "150-200", "200-500", "500+"])
    return df

def select_top_features(X_processed, y, feature_names):
    selector = SelectKBest(score_func=f_regression, k=10)
    selector.fit(X_processed, y)
    top_features = np.array(feature_names)[selector.get_support()]
    print("Top 10 veçori më të rëndësishme sipas ANOVA F-score:")
    for feat in top_features:
        print(f"{feat}")

def plot_mae_by_bin(df):
    plt.figure(figsize=(8, 5))
    mae_per_bin = df.groupby("ABP_Bin", observed=False)["Cmimi_Real"].mean() - \
              df.groupby("ABP_Bin", observed=False)["Parashikim"].mean()
    mae_per_bin = mae_per_bin.abs()
    mae_per_bin.plot(kind="bar", color="orange")
    plt.ylabel("Gabimi Mesatar Absolut (MAE)")
    plt.title("Gabimi MAE sipas Kategorive të Sipërfaqes Totale")
    plt.tight_layout()
    plt.savefig("grafiket/mae_by_abp_bin.png")
    plt.close()

def plot_mae_by_type(df):
    plt.figure(figsize=(8, 5))
    mae_per_type = df.groupby("Lloji", observed=False)["Cmimi_Real"].mean() - \
               df.groupby("Lloji", observed=False)["Parashikim"].mean()
    mae_per_type = mae_per_type.abs()
    mae_per_type.plot(kind="bar", color="orange")
    plt.ylabel("Gabimi Mesatar Absolut (MAE)")
    plt.title("Gabimi MAE sipas Llojit të Pronës")
    plt.tight_layout()
    plt.savefig("grafiket/mae_by_type.png")
    plt.close()

def plot_model_metrics_bar(xgb_rmse, xgb_mae, rf_rmse, rf_mae):
    labels = ['Random Forest', 'XGBoost']
    rmse = [rf_rmse, xgb_rmse]
    mae = [rf_mae, xgb_mae]
    x = np.arange(len(labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - width/2, rmse, width, label='Test RMSE (€)', color='skyblue')
    ax.bar(x + width/2, mae, width, label='Test MAE (€)', color='orange')
    ax.set_ylabel('Vlera në Euro (€)')
    ax.set_title('Krahasimi i RMSE dhe MAE në test për modelet')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    plt.tight_layout()
    os.makedirs("grafiket", exist_ok=True)
    plt.savefig("grafiket/krahasimi_modeleve.png")
    plt.close()

def plot_boxplot_surface(df):
    os.makedirs("grafiket", exist_ok=True)
    fig, axs = plt.subplots(3, 2, figsize=(14, 10))
    sns.boxplot(ax=axs[0, 0], x=df['Siperfaqe Totale'], color='lightblue')
    axs[0, 0].set_title("Boxplot - Siperfaqe Totale")
    sns.boxplot(ax=axs[0, 1], x=df['Siperfaqe e Brendshme'], color='lightblue')
    axs[0, 1].set_title("Boxplot - Siperfaqe e Brendshme")
    sns.boxplot(ax=axs[1, 0], x=df['Dhoma Gjumi'], color='lightblue')
    axs[1, 0].set_title("Boxplot - Dhoma Gjumi")
    sns.boxplot(ax=axs[1, 1], x=df['Shikime'], color='lightblue')
    axs[1, 1].set_title("Boxplot - Shikime")
    sns.boxplot(ax=axs[2, 0], x=df['Cmimi'], color='lightblue')
    axs[2, 0].set_title("Boxplot - Cmimi")
    axs[0, 0].set_xlabel("Siperfaqe Totale")
    axs[0, 1].set_xlabel("Siperfaqe e Brendshme")
    axs[1, 0].set_xlabel("Dhoma Gjumi")
    axs[1, 1].set_xlabel("Shikime")
    axs[2, 0].set_xlabel("Cmimi")
    fig.delaxes(axs[2, 1])
    plt.tight_layout()
    plt.savefig("grafiket/boxplots_all.png")
    plt.close()

