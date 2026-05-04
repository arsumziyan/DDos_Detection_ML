import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ─── 1. Load Dataset ───────────────────────────────────────────
# Place the CSV file in the same folder as this script
data = pd.read_csv('Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')

# ─── 2. Clean Column Names ─────────────────────────────────────
data.columns = data.columns.str.strip()

# ─── 3. Preprocessing ──────────────────────────────────────────
data.replace([np.inf, -np.inf], np.nan, inplace=True)
data.dropna(inplace=True)

# ─── 4. Label Encoding ─────────────────────────────────────────
data['Label'] = data['Label'].map({'BENIGN': 0, 'DDoS': 1})

# ─── 5. Feature Selection ──────────────────────────────────────
X = data.select_dtypes(include=[np.number]).drop(columns=['Label'])
y = data['Label']

# ─── 6. Train / Test Split ─────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Training set size: {X_train.shape}")
print(f"Testing set size:  {X_test.shape}")

# ─── 7. Train Random Forest ────────────────────────────────────
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# ─── 8. Evaluate ───────────────────────────────────────────────
y_pred = rf_model.predict(X_test)
print("\n--- Model Performance ---")
print(f"Accuracy Score: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['BENIGN', 'DDoS']))

# ─── 9. Confusion Matrix ───────────────────────────────────────
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['BENIGN', 'DDoS'],
            yticklabels=['BENIGN', 'DDoS'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('DDoS Detection Confusion Matrix')
plt.tight_layout()
plt.show()

# ─── 10. Feature Importance ────────────────────────────────────
importances = rf_model.feature_importances_
indices = np.argsort(importances)[-10:]
plt.figure(figsize=(10, 6))
plt.title('Top 10 Important Network Features')
plt.barh(range(len(indices)), importances[indices], align='center')
plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
plt.xlabel('Relative Importance')
plt.tight_layout()
plt.show()

# ─── 11. Manual Prediction Tests ───────────────────────────────
safe_example = X_test.iloc[0:1]
print(f"\nTest 1 (real sample): {'DDoS' if rf_model.predict(safe_example)[0] == 1 else 'Safe'}")

ddos_index = y_test[y_test == 1].index[0]
ddos_example = X_test.loc[[ddos_index]]
print(f"Test 2 (real DDoS):   {'DDoS' if rf_model.predict(ddos_example)[0] == 1 else 'Safe'}")

test_input = safe_example.copy()
test_input['Bwd Packet Length Std'] = 500.0
test_input['Flow Duration'] = 10
print(f"Test 3 (simulated):   {'DDoS' if rf_model.predict(test_input)[0] == 1 else 'Safe'}")