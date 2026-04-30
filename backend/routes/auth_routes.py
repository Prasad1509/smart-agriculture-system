from flask import Blueprint, request, jsonify, session
from utils.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# =====================================================
# 🔹 REGISTER API
# =====================================================
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        name = data['name']
        email = data['email']
        password = data['password']

        # 🔐 Hash password
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
        """, (name, email, hashed_password))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =====================================================
# 🔹 LOGIN API
# =====================================================
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        email = data['email']
        password = data['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # ❌ direct password check remove
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        # ✅ Check hashed password
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]   # 🔐 session save

            return jsonify({
                "message": "Login successful",
                "user_id": user[0]
            })
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500