import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# ✅ Load dataset
data = pd.read_csv('../dataset/crop_data.csv')

# ✅ Features & Label
X = data[['temperature', 'humidity', 'rainfall']]
y = data['crop']

# ✅ Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# ✅ Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# ✅ Save model
pickle.dump(model, open('../saved_model/crop_model.pkl', 'wb'))

print("Model trained & saved successfully")