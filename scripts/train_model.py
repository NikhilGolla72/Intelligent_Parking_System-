import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("data/parking_data.csv")

le = LabelEncoder()
df["Vehicle Type"] = le.fit_transform(df["Vehicle Type"])
df["Weather"] = le.fit_transform(df["Weather"])
df["Traffic"] = le.fit_transform(df["Traffic"])
df["Location"] = le.fit_transform(df["Location"])

X = df.drop(columns=["Vehicle Number", "Parking Time"])
y = df["Parking Time"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

with open("models/parking_model.pkl", "wb") as f:
    pickle.dump(rf_model, f)
