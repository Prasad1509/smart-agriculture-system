from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# ✅ REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    name = data['name']
    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔍 Check duplicate email
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        return jsonify({"message": "Email already exists"}), 400

    # 🔐 Hash password
    hashed_password = generate_password_hash(password)

    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, hashed_password))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "User registered successfully"})


# ✅ LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    email = data['email']
    password = data['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email=%s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    # 🔐 Check password
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login success", "user": user})
    else:
        return jsonify({"message": "Invalid credentials"}), 401