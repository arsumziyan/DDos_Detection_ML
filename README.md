# 🛡️ DDoS Attack Detection System

A machine learning project that detects Distributed Denial-of-Service (DDoS) attacks in real-time network traffic using a **Random Forest classifier** trained on the ISCX-CIC benchmark dataset.

---

## 📊 Results

| Metric | Score |
|---|---|
| Accuracy | ~99% |
| Precision (DDoS) | ~1.00 |
| Recall (DDoS) | ~1.00 |
| F1 Score | ~1.00 |

The model achieves near-perfect classification on the held-out test set, with virtually zero false positives and false negatives.

---

## 📁 Dataset

**ISCX-CIC Friday DDoS Dataset (CIC-DDoS2019)**

- File used: `Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`
- Contains real packet capture data labeled as `BENIGN` or `DDoS`
- Download: [Kaggle — CIC-DDoS2019](https://www.kaggle.com/datasets/aymenabb/ddos-evaluation-dataset-cic-ddos2019)

> **Note:** The dataset file is not included in this repo due to its large size. Download it from Kaggle and place it in your working directory or Google Drive before running the notebook.

---

## 🧠 How It Works — ML Pipeline

```
Raw CSV  →  Clean Data  →  Encode Labels  →  Feature Selection  →  Train/Test Split  →  Train RF  →  Evaluate
```

1. **Data Ingestion** — Load the `.pcap_ISCX.csv` file
2. **Data Cleaning** — Strip column whitespace, replace `±Inf` with NaN, drop nulls
3. **Label Encoding** — `BENIGN → 0`, `DDoS → 1`
4. **Feature Selection** — All numeric columns as features; `Label` as target
5. **Train/Test Split** — 80% train, 20% test (`random_state=42`)
6. **Model Training** — `RandomForestClassifier(n_estimators=100, n_jobs=-1)`
7. **Evaluation** — Accuracy score, classification report, confusion matrix heatmap

---

## 🏆 Top Network Features (by Importance)

| Feature | Relative Importance |
|---|---|
| Bwd Packet Length Std | 0.92 |
| Flow Duration | 0.78 |
| Fwd Packet Length Max | 0.65 |
| Avg Bwd Segment Size | 0.55 |
| Packet Length Variance | 0.44 |
| Flow Bytes/s | 0.36 |
| Init_Win_bytes_forward | 0.28 |

---

## 🚀 Getting Started

### Option A — Google Colab (Recommended)

1. Open the notebook in Google Colab
2. Upload the dataset CSV to your Google Drive
3. Update the file path in the notebook:
   ```python
   data = pd.read_csv('/content/drive/MyDrive/your-folder/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')
   ```
4. Run all cells

### Option B — Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ddos-detection-ml.git
cd ddos-detection-ml

# 2. Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn

# 3. Place the dataset CSV in the project folder and update the path in the script

# 4. Run the script
python ddos_detector.py
```

---

## 🧪 Manual Testing

The notebook includes three prediction tests:

```python
# Test 1 — Predict on a real BENIGN sample from the test set
safe_example = X_test.iloc[0:1]
# → Output: "Safe"

# Test 2 — Predict on a real DDoS sample from the test set
ddos_example = X_test.loc[[ddos_index]]
# → Output: "DDoS"

# Test 3 — Manually simulate an attack scenario
test_input['Bwd Packet Length Std'] = 500.0
test_input['Flow Duration'] = 10
# → Output: "DDoS"  (model correctly flags the simulated flood)
```

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **ML Library:** scikit-learn
- **Data:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Environment:** Google Colab

---

## 📂 Project Structure

```
ddos-detection-ml/
├── README.md
├── ddos_detector.py              # Standalone training & prediction script
├── notebook/
│   └── ddos_detection.ipynb     # Full Google Colab notebook
└── portfolio/
    ├── ddos-detection-portfolio.html
    └── ddos-detection-portfolio.css
```

---

## ⚠️ Limitations & Notes

- The ISCX-CIC dataset is a well-known benchmark, and tree-based models tend to achieve high accuracy on it due to strong feature separability between traffic classes. Real-world performance on unseen network environments may vary.
- The model is trained on a single day's traffic capture — broader generalization would require training on multiple attack types and time windows.
- No feature scaling is applied (Random Forests don't require it).

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

*Built with Python & scikit-learn — DDoS Detection ML Project*
