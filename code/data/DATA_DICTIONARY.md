# Data dictionary

Raw files are downloaded on first use to `code/data/raw/` by `fhe_heart/data.py` and are **not**
committed (`.gitignore`). Processed train/test CSVs go to `code/data/processed/<dataset>/` (also
not committed). See [research/ethics-data-note.md](../../research/ethics-data-note.md) for
licences and the IRB decision.

Split for both datasets: stratified, `test_size = 0.25`, `random_state = 42`; StandardScaler
fitted on the training rows only. The fitted scaler is saved inside
`fhe-ml-service/model/model_weights_<dataset>.json` so the client scales a raw form row exactly
as in training before encrypting it.

## UCI Heart Disease – Cleveland (`processed.cleveland.data`)

Source: Detrano et al. (1989), UCI Machine Learning Repository. 303 rows; 6 rows have `?` in
`ca` or `thal` and are dropped → **297 rows**, 13 features. Label: `num > 0` → 1 (disease),
`num = 0` → 0. Test split = 75 patients (PR2 Table 5).

| # | Column | Plain-language meaning (web form label) | Values |
|---|---|---|---|
| 1 | `age` | Age | years |
| 2 | `sex` | Sex | 1 = male, 0 = female |
| 3 | `cp` | Chest pain type | 1 typical angina, 2 atypical angina, 3 non-anginal pain, 4 asymptomatic |
| 4 | `trestbps` | Resting blood pressure | mm Hg on admission |
| 5 | `chol` | Serum cholesterol | mg/dl |
| 6 | `fbs` | Fasting blood sugar above 120 mg/dl | 1 = yes, 0 = no |
| 7 | `restecg` | Resting ECG | 0 normal, 1 ST-T wave abnormality, 2 left ventricular hypertrophy |
| 8 | `thalach` | Maximum heart rate reached | beats per minute |
| 9 | `exang` | Chest pain during exercise | 1 = yes, 0 = no |
| 10 | `oldpeak` | ST depression after exercise, relative to rest | mm |
| 11 | `slope` | Slope of the peak exercise ST segment | 1 up, 2 flat, 3 down |
| 12 | `ca` | Major vessels coloured by fluoroscopy | 0–3 |
| 13 | `thal` | Thallium stress test | 3 normal, 6 fixed defect, 7 reversible defect |
| – | `num` | Diagnosis (label) | 0 = no disease; 1–4 = disease (binarised) |

Note: the categorical columns are used as numbers (as in the PR2 pilot). One-hot encoding would
raise the feature count (and the number of ciphertexts in the per-feature layout); this is a
documented simplification, not an oversight.

## Edinburgh myocardial infarction (`edin.txt`)

Source: Kennedy et al. (1996). **1,253 rows, 9 binary features**, label `y` (1 = MI, 274 cases).
The public copy used here is the one distributed with Kim et al. (2018), the iDASH 2017 Track 3
winner (github.com/kimandrik/IDASH2017, licence CC BY-NC 3.0). In that copy the columns are
anonymised as `x1`–`x9`, so the web form can only show "Clinical item x1 … x9". The original
paper lists the clinical items; if the team needs real labels, map them from Kennedy et al. 1996
and record the source here.

Results for the two datasets are reported separately, never pooled (PR2 data statement).
