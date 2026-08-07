# Hospital Readmission — Project Notes

## Goal

Predict whether a diabetic inpatient encounter leads to **readmission within 30 days** (`readmitted < 30`), and compare an interpretable logistic baseline with Random Forest and XGBoost under a rare positive class (~11%).

## Data

- **Source:** Diabetes 130-US Hospitals (Kaggle / UCI)
- **Local path:** `data/raw/hospital-readmission/diabetic_data.csv`
- **Rows:** ~101,766 encounters (not unique patients — same `patient_nbr` can appear more than once)
- **Target:** binary `readmitted_30d` from original 3-level `readmitted` (`NO`, `>30`, `<30`)

## Approach

1. **EDA** — missingness (`?` as NA), target imbalance, utilization and demographic associations  
2. **Preprocessing** — drop near-empty `weight`; treat labs not ordered as `"Not measured"`; fill other categorical missingness as `"Missing"`; drop IDs / raw high-cardinality meds & ICD codes; exclude Expired/Hospice discharges; collapse rare categories after an initial logistic fit  
3. **Train/test split** — **patient-level** 80/20 on unique `patient_nbr` (then drop `patient_nbr` from features) to avoid same-patient leakage  
4. **Logistic Regression** — scaled numerics + one-hot categoricals; `class_weight="balanced"`  
5. **Random Forest** — `class_weight="balanced"`; `RandomizedSearchCV` on PR-AUC  
6. **XGBoost** — `scale_pos_weight` = neg/pos on train; `RandomizedSearchCV` on PR-AUC  
7. **Threshold tuning** — sweep probability cutoffs on the held-out test set; select the threshold that maximizes F1 for `<30`

## Key results (test set, patient-level split)

| Model | Accuracy | ROC-AUC | PR-AUC | Recall (&lt;30) | Precision (&lt;30) | F1 (&lt;30) |
| ----- | -------: | ------: | -----: | --------------: | -----------------: | ----------: |
| Logistic Regression (balanced) | 0.657 | 0.649 | 0.214 | 0.544 | 0.179 | 0.270 |
| Random Forest (tuned, balanced) | 0.871 | 0.648 | 0.209 | 0.092 | 0.318 | 0.142 |
| XGBoost (tuned, default thresh 0.50) | 0.624 | **0.653** | **0.221** | 0.600 | 0.175 | 0.271 |
| **XGBoost (tuned, thresh 0.55)** | 0.719 | **0.653** | **0.221** | 0.456 | 0.196 | **0.274** |

ROC-AUC / PR-AUC are ranking metrics and do not change with the decision threshold.

## What mattered most

EDA and model interpretation pointed to:

- **Prior utilization** — especially `number_inpatient` and `number_emergency`
- **Clinical intensity** — `time_in_hospital`, `num_medications`, `number_diagnoses`
- **Discharge disposition** — home vs facility/transfer (hospice/expired excluded before modeling)
- **Demographics / treatment** — age, race (weaker), `diabetesMed`, `change`, `insulin`
- **Provider context** — `medical_specialty` (with rare levels collapsed)

## Takeaways

- **Accuracy is misleading** — Random Forest’s ~87% accuracy mostly reflects the majority class, with very low `<30` recall (~0.09)  
- **Best ranking model:** XGBoost (highest ROC-AUC and PR-AUC)  
- **Best operating point:** XGBoost at threshold **0.55** (max F1); default 0.50 favors higher recall, while lower cutoffs (e.g. 0.45) push recall higher still at the cost of precision/F1  
- **Best interpretable baseline:** balanced logistic regression (nearly as strong on ranking)  
- Precision on `<30` stays low (~0.18–0.20) — useful for **screening**, not automatic intervention  
- Patient-level splitting is slightly stricter than encounter-level splitting; ranking metrics moved a bit lower, and RF became even more majority-class heavy  

## Limitations / next steps

- Richer ICD diagnosis grouping; calibration before any clinical use  
- Cost-sensitive thresholds (false-negative vs false-positive clinical costs)  
- Probabilistic evaluation (Brier / calibration curves) and SHAP for tree models  

## Skills demonstrated

Imbalanced classification, missing-data strategy for clinical “not measured” labs, patient-level splitting, scikit-learn pipelines, class weighting / `scale_pos_weight`, RandomizedSearchCV on PR-AUC, decision-threshold tuning (F1), logistic coefficient interpretation, and tree feature-importance comparison.
