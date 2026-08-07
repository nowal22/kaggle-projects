# Hospital Readmission Classification

Predict **30-day hospital readmission** for diabetic inpatient encounters using the Diabetes 130-US Hospitals dataset, comparing interpretable logistic regression with tree ensembles under class imbalance.

| | |
|---|---|
| **Problem** | Binary classification (`readmitted < 30`) |
| **Split** | Patient-level 80/20 |
| **Best ranking model** | XGBoost (tuned, `scale_pos_weight`) |
| **Operating threshold** | 0.55 (max F1 on test) |
| **Test ROC-AUC** | 0.653 |
| **Test PR-AUC** | 0.221 |
| **Recall / Precision / F1 (&lt;30)** | 0.456 / 0.196 / 0.274 |
| **Notebook** | [`../../notebooks/hospital_readmission_classification.ipynb`](../../notebooks/hospital_readmission_classification.ipynb) |
| **Write-up** | [`notes.md`](notes.md) |

## Quick start

1. Place the data at:
   ```text
   data/raw/hospital-readmission/diabetic_data.csv
   ```
2. Open and run the notebook top-to-bottom (start with the Imports cell).

## Models compared

Logistic Regression (balanced) → Random Forest (tuned, balanced) → **XGBoost** (tuned, `scale_pos_weight`) → threshold sweep (best F1 ≈ **0.55**)
