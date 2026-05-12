# CLO4-IDS-ML-Solution
### AI-Powered Intrusion Detection System | Information Security Assignment 1

---

## Project Overview
A Machine Learning-based Network Intrusion Detection System (NIDS) that classifies network traffic as **Normal** or **Malicious** using the NSL-KDD benchmark dataset.

## Objective
Design, develop, and evaluate a proof-of-concept ML model to augment an existing NIDS, demonstrating that ML can outperform rule-based detection for modern network threats.

## Dataset
**NSL-KDD** — Improved version of the KDD Cup 1999 dataset, containing:
- 41 network traffic features (packet stats, protocol info, flag counts)
- Labels: normal traffic + 4 attack categories (DoS, Probe, R2L, U2R)
- Training: ~125,000 samples | Test: ~22,000 samples

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/mrehanmajeed/CLO4-IDS-ML-Solution
cd CLO4-IDS-ML-Solution
```

### 2. Install Dependencies
```bash
pip install pandas numpy scikit-learn matplotlib seaborn jupyter
```

### 3. Run the Notebook
```bash
jupyter notebook IDS_ML_Solution.ipynb
```
> The notebook will automatically download the NSL-KDD dataset on first run. It will also save the trained model as `ids_dt_model.pkl`.

### 4. Run the Interactive Dashboard (Streamlit)
To visualize the ML model in action with a beautiful frontend, run the Streamlit dashboard:
```bash
streamlit run app.py
```
> **Note:** The dashboard will allow you to enter live IP addresses or hostnames. It simulates the extraction of the 41 NSL-KDD networking features to demonstrate real-time predictive capabilities.

## Models Implemented
| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| Random Forest | ~76.74% | ~96.71% | ~61.22% | ~74.98% |
| Decision Tree | ~79.36% | ~96.70% | ~65.99% | ~78.44% |

## Results Summary
- **Decision Tree** selected as primary model for superior precision and explainability
- High Recall ensures minimal missed attacks (low False Negatives)
- Feature Importance analysis identifies top network traffic indicators of attacks
- Confusion matrix and classification reports included for full evaluation

## Repository Structure
```
CLO4-IDS-ML-Solution/
├── IDS_ML_Solution.ipynb   # Complete ML pipeline
├── README.md
├── KDDTrain+.txt           # Auto-downloaded on first run
├── KDDTest+.txt            # Auto-downloaded on first run
└── *.png                   # Generated plots
```

## References
- Tavallaee, M. et al. (2009). A detailed analysis of the KDD CUP 99 data set. IEEE CISDA.
- NSL-KDD Dataset: https://github.com/defcom17/NSL_KDD
- Scikit-learn documentation: https://scikit-learn.org
