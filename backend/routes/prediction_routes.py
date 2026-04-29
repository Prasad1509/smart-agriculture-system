from flask import Blueprint, request, jsonify
from utils.db import get_db_connection

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/predict-db', methods=['GET','POST'])
def predict_db():
    try:
        data = request.json

        temp = float(data['temperature'])
        humidity = float(data['humidity'])
        rainfall = float(data['rainfall'])
        user_id = int(data['user_id'])

        # Simple logic
        if rainfall > 80:
            crop = "Rice"
        elif temp > 30:
            crop = "Maize"
        else:
            crop = "Wheat"

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO predictions (user_id, temperature, humidity, rainfall, predicted_crop)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, temp, humidity, rainfall, crop))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"predicted_crop": crop})

    except Exception as e:
        return jsonify({"error": str(e)}), 500