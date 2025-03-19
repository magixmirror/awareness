import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Load dataset
df = pd.read_csv("./rainfall_area-wt_India_1901-2015.csv")

# Define new scarcity classification thresholds
def classify_scarcity(annual_rainfall):
    if annual_rainfall < 1000:
        return "Severe Scarcity"
    elif 1000 <= annual_rainfall < 1150:
        return "Moderate Scarcity"
    else:
        return "No Scarcity"

# Apply classification
df["Scarcity_Level"] = df["ANNUAL"].apply(classify_scarcity)

# Select features (monthly + seasonal rainfall)
features = df.columns[2:-2]  # Exclude REGION, YEAR, and ANNUAL
X = df[features]
y = df["Scarcity_Level"]

# Encode target labels
y_encoded = LabelEncoder().fit_transform(y)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

# Compute class weights
class_weights = compute_class_weight(class_weight="balanced", classes=np.unique(y_train), y=y_train)
class_weight_dict = {i: class_weights[i] for i in range(len(class_weights))}

# Train Random Forest model with class weighting
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight=class_weight_dict)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=["Moderate Scarcity", "No Scarcity", "Severe Scarcity"])
conf_matrix = confusion_matrix(y_test, y_pred)

# Print results
print("Model Accuracy:", accuracy)
print("Classification Report:\n", report)
print("Confusion Matrix:\n", conf_matrix)

# Save the model
joblib.dump(model, "water_scarcity_model.pkl")


