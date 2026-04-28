from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os

# 🔗 Import DB
from utils.db import get_db_connection

# 🔗 Import routes
from routes.auth_routes import auth_bp

# ✅ App init
app = Flask(__name__)
CORS(app)

# ✅ Register blueprint
app.register_blueprint(auth_bp)

# ✅ Load ML model (safe path)
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    '../ml_model/saved_model/crop_model.pkl'
)

model = pickle.load(open(MODEL_PATH, 'rb'))

# ✅ Home route
@app.route('/')
def home():
    return "Backend Running 🚀"

# ✅ Test DB connection
@app.route('/test-db')
def test_db():
    try:
        conn = get_db_connection()
        conn.close()
        return "Database Connected ✅"
    except Exception as e:
        return f"DB Error: {str(e)}"

# ✅ Prediction API
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