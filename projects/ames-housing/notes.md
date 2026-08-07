# Ames Housing — Project Notes

## Goal

Predict `SalePrice` for homes in Ames, Iowa, and compare interpretable linear models with nonlinear tree ensembles.

## Data

- **Source:** Ames Housing dataset (~2,930 homes, 82 variables)
- **Local path:** `data/raw/ames-housing/AmesHousing.csv`
- **Target:** `SalePrice` (right-skewed → modeled as `log1p(SalePrice)`)

## Approach

1. **EDA** — correlations, quality/size/neighborhood relationships, missingness, outliers  
2. **Preprocessing** — drop IDs; impute missing values; one-hot encode categoricals  
3. **Baseline OLS** — residual diagnostics showed heteroscedasticity and non-normal tails  
4. **Log target** — improved variance stability  
5. **VIF** — high multicollinearity → Ridge / Lasso / Elastic Net  
6. **Tree models** — Random Forest and XGBoost for nonlinear effects / interactions  

## Key results (test set)

| Model | Test RMSE (log) | Test R² | Dollar RMSE |
| ----- | --------------: | ------: | ----------: |
| Linear Regression | 0.165 | 0.854 | — |
| Ridge (α=1000) | 0.124 | 0.917 | $32,765 |
| Lasso (α=0.005) | 0.128 | 0.912 | — |
| Elastic Net | 0.127 | 0.912 | — |
| Random Forest | 0.123 | 0.919 | $27,228 |
| **XGBoost** | **0.107** | **0.938** | **$25,047** |

## What mattered most

Across Random Forest and XGBoost feature importance:

- **Overall Qual**
- Living / basement size (`Gr Liv Area`, `Total Bsmt SF`, `1st Flr SF`)
- Garage features (`Garage Cars`, `Garage Area`)
- Age / year built and related amenities

Ridge coefficients (interpretable linear view) pointed in the same direction: quality, size, and location drive price.

## Takeaways

- **Best predictor:** XGBoost (lowest error, highest R²)  
- **Best interpretable model:** Ridge  
- Log-transforming price and addressing multicollinearity with regularization were important steps before moving to ensembles  

## Limitations / next steps

- Ames-only data; may not generalize to other markets  
- Known large `Gr Liv Area` outliers were retained (could re-fit after removal)  
- No spatial or time-based validation beyond a random split  
- Possible extensions: engineered features (`TotalSF`, `HouseAge`), ordinal encodings for quality ratings  

## Skills demonstrated

EDA, missing-data handling, assumption checking, log transforms, VIF, regularized regression, Random Forest, XGBoost, model comparison, and coefficient / feature-importance interpretation.
