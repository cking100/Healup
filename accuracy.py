import os
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

print("\n" + "="*70)
print("🤖 MODEL EVALUATION ACROSS MULTIPLE DATASETS")
print("="*70)

# -----------------------------
# Configuration
# -----------------------------
DATA_DIR = "Data"  # folder containing your datasets
VALID_EXTENSIONS = [".csv"]
MIN_CLASSES = 2     # at least 2 unique disease classes required

# -----------------------------
# Convert non-numeric columns to numeric safely
# -----------------------------
def convert_to_numeric(df):
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].str.strip().str.lower().replace({'yes':1, 'no':0})
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

# -----------------------------
# Function to safely load and detect disease column
# -----------------------------
def load_dataset_with_target(path):
    df = pd.read_csv(path)
    if df.empty:
        return None, None, "❌ Empty dataset"

    # Try to find the target/disease column
    target_col = None
    for col in df.columns:
        if col.lower() in ["disease", "prognosis", "target", "diagnosis", "label"]:
            target_col = col
            break

    # If not found, assume last column is disease
    if not target_col:
        target_col = df.columns[-1]

    y = df[target_col]
    X = df.drop(columns=[target_col])

    # Convert non-numeric features to numeric
    X = convert_to_numeric(X)

    # Check if disease column is valid
    if y.nunique() < MIN_CLASSES:
        return None, None, f"⚠️ Only {y.nunique()} class found in '{target_col}' column"

    return X, y, f"✅ Found disease column: '{target_col}'"

# -----------------------------
# Evaluate one dataset
# -----------------------------
def evaluate_dataset(path):
    X, y, msg = load_dataset_with_target(path)
    print(f"\n📂 {os.path.basename(path)} → {msg}")

    if X is None or y is None:
        return None

    # Encode & Scale
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Split & Train
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return acc

# -----------------------------
# Main loop through datasets
# -----------------------------
def main():
    dataset_files = [
        os.path.join(DATA_DIR, f)
        for f in os.listdir(DATA_DIR)
        if os.path.splitext(f)[1].lower() in VALID_EXTENSIONS
    ]

    if not dataset_files:
        print("❌ No CSV datasets found in the Data/ folder.")
        return

    accuracies = []
    for file in dataset_files:
        acc = evaluate_dataset(file)
        if acc is not None:
            accuracies.append((os.path.basename(file), acc))

    print("\n" + "="*70)
    print("📊 EVALUATION SUMMARY")
    print("="*70)

    if not accuracies:
        print("❌ No valid datasets to evaluate.")
        return

    for name, acc in accuracies:
        print(f"✅ {name}: {acc*100:.2f}%")

    overall_acc = np.mean([a for _, a in accuracies])
    print("\n🏆 OVERALL AVERAGE ACCURACY: {:.2f}%".format(overall_acc * 100))

    print("="*70)

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    main()
