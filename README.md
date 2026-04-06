# Outbreak AI — Django Disease Outbreak Prediction System

## Quick Start (Python 3.10)

```bash
# 1. Install dependencies (NO TensorFlow required!)
pip install -r requirements.txt

# 2. First-time setup
python setup.py

# 3. Start server
python run.py
```

Open http://127.0.0.1:8000 — **Admin: `admin` / `admin123`**

---

## Why Scikit-learn instead of TensorFlow?

TensorFlow on Windows requires specific Microsoft Visual C++ Redistributables
and CUDA drivers. If these are missing or mismatched, TF throws a DLL load error.

The scikit-learn **Voting Ensemble (RandomForest + LogisticRegression + LinearSVC)**
used here:
- ✅ Works on any Python 3.10 Windows install with zero DLL issues
- ✅ Trains in ~10–30 seconds vs minutes for a CNN
- ✅ Handles imbalanced classes with `class_weight='balanced'`
- ✅ Produces probability estimates for confidence scores
- ✅ Achieves competitive accuracy on text classification tasks

---

## Workflow

1. **Admin uploads dataset** → `/admin-panel/upload/` → pick `Outbreak.csv`
2. **Admin trains model** → `/admin-panel/train/` → click "Start Training"
3. **View evaluation** → `/admin-panel/evaluation/`
4. **Users predict** → `/predict/`

## Bug Fix History

| # | File | Bug | Fix |
|---|------|-----|-----|
| 1 | `ml_engine.py` | TensorFlow DLL error on Windows | Replaced with scikit-learn ensemble |
| 2 | `ml_engine.py` | `stratify` fails with singleton classes | Auto-detect & disable stratify |
| 3 | `ml_engine.py` | Used `Date` column for TF-IDF | Smart column selection prefers `Description` |
| 4 | `ml_engine.py` | `environment.npy` never saved | Save/load `tfidf.pkl`, `scaler.pkl`, `clf.pkl` |
| 5 | `views.py` | `SameFileError` on upload | Check `abspath` before `shutil.copy` |
| 6 | `apps.py` | TF import crash on startup | Wrapped in `try/except`, checks for `clf.pkl` |
| 7 | `admin_upload.html` | Invalid `\|split` filter | Hardcoded column pill list |
| 8 | `requirements.txt` | TF/keras version conflicts | Removed TF; only scikit-learn needed |
