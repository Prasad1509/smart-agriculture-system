from flask import Blueprint, request, jsonify
from utils.db import get_db_connection

prediction_bp = Blueprint('prediction', __name__)

# =====================================================
# 🔹 1. PREDICT + SAVE DATA (POST API)
# =====================================================
@prediction_bp.route('/predict-db', methods=['POST'])
def predict_db():
    conn = None
    cursor = None

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        # Validate fields
        required_fields = ['temperature', 'humidity', 'rainfall', 'user_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Convert values
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        rainfall = float(data['rainfall'])
        user_id = int(data['user_id'])

        # Prediction logic
        if rainfall > 80:
            crop = "Rice"
        elif temperature > 30:
            crop = "Maize"
        else:
            crop = "Wheat"

        print("Data:", data)
        print("Predicted Crop:", crop)

        # DB insert
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO predictions (user_id, temperature, humidity, rainfall, predicted_crop)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, temperature, humidity, rainfall, crop))

        conn.commit()

        return jsonify({
            "message": "Prediction saved successfully",
            "predicted_crop": crop
        })

    except ValueError:
        return jsonify({"error": "Invalid data type"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# =====================================================
# 🔹 2. GET HISTORY DATA (NEW API)
# =====================================================
@prediction_bp.route('/predictions/<int:user_id>', methods=['GET'])
def get_predictions(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM predictions WHERE user_id = %s
        """, (user_id,))

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500