import pandas as pd
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "intent_model.pkl")

# Create folder if not exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv("intent_dataset.csv")

X = df["text"]
y = df["intent"]

# Vectorizer + Model
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vec, y)

# Save (model + vectorizer)
with open(MODEL_PATH, "wb") as f:
    pickle.dump((model, vectorizer), f)

print("✅ Model trained & saved at:", MODEL_PATH)
