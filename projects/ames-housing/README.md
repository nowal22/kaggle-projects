# Ames Housing Price Prediction

Predict residential sale prices in Ames, Iowa using regularized linear models and tree-based ensembles.

| | |
|---|---|
| **Problem** | Regression (`SalePrice`) |
| **Best model** | XGBoost |
| **Test R² (log)** | 0.938 |
| **Test RMSE (log)** | 0.107 |
| **Dollar RMSE** | ~$25,047 |
| **Notebook** | [`../../notebooks/Ames_housing_regression.ipynb`](../../notebooks/Ames_housing_regression.ipynb) |
| **Write-up** | [`notes.md`](notes.md) |

## Quick start

1. Place the data at:
   ```text
   data/raw/ames-housing/AmesHousing.csv
   ```
2. Open and run the notebook top-to-bottom (start with the Imports cell).

## Models compared

Linear Regression → Ridge / Lasso / Elastic Net → Random Forest → **XGBoost**
