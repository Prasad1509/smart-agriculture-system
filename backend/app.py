from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os

# ✅ Correct imports
from routes.prediction_routes import prediction_bp
from routes.auth_routes import auth_bp
from utils.db import get_db_connection

app = Flask(__name__)
CORS(app)

# ✅ Register routes
app.register_blueprint(auth_bp)
app.register_blueprint(prediction_bp)

# ✅ Load ML model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    '../ml_model/saved_model/crop_model.pkl'
)

model = pickle.load(open(MODEL_PATH, 'rb'))

# ✅ Home
@app.route('/')
def home():
    return "Backend Running 🚀"

# ✅ Test DB
@app.route('/test-db')
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return "Database Connected ✅"
    except Exception as e:
        return f"DB Error: {str(e)}"

# ✅ ML Prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        temp = float(data['temperature'])
        hum = float(data['humidity'])
        rain = float(data['rainfall'])

        result = model.predict([[temp, hum, rain]])

        return jsonify({
            "prediction": result[0]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Run server
if __name__ == '__main__':
    app.run(debug=True)