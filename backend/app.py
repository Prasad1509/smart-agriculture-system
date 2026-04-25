from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

# ✅ Model load
model = pickle.load(open('../ml_model/saved_model/crop_model.pkl', 'rb'))

# ✅ Home route
@app.route('/')
def home():
    return "Backend Running"

# ✅ Prediction API
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    temp = float(data['temperature'])
    hum = float(data['humidity'])
    rain = float(data['rainfall'])

    result = model.predict([[temp, hum, rain]])

    return jsonify({
        "prediction": result[0]
    })

# ✅ Run server
if __name__ == '__main__':
    app.run(debug=True)