from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os

# ✅ Import routes
from routes.prediction_routes import prediction_bp
from routes.auth_routes import auth_bp
from utils.db import get_db_connection

# ✅ App init
app = Flask(__name__)
CORS(app)
app.secret_key = "secret123"   # 🔐 session ke liye required

# ✅ Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(prediction_bp)

# =====================================================
# 🔹 Load ML model (ONLY ONCE)
# =====================================================
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    '../ml_model/saved_model/crop_model.pkl'
)

model = pickle.load(open(MODEL_PATH, 'rb'))

# =====================================================
# 🔹 Home Route
# =====================================================
@app.route('/')
def home():
    return "Backend Running 🚀"

# =====================================================
# 🔹 Test DB Connection
# =====================================================
@app.route('/test-db')
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return "Database Connected ✅"
    except Exception as e:
        return f"DB Error: {str(e)}"

# =====================================================
# 🔹 ML Prediction API
# =====================================================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # ✅ Correct variables
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        rainfall = float(data['rainfall'])

        # ✅ Use already loaded model
        result = model.predict([[temperature, humidity, rainfall]])
        crop = result[0]

        return jsonify({
            "prediction": crop
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================================================
# 🔹 Run server
# =====================================================
if __name__ == '__main__':
    app.run(debug=True)