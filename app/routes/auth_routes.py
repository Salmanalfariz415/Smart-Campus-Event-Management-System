from flask import request, jsonify, Blueprint
from app.db.sql_connection import get_sql_connection
import app.dao.auth_dao as auth_dao
import traceback
from flask_cors import cross_origin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://localhost:63342"])
def register():
    if request.method == 'OPTIONS':
        return '', 200

    connection = None
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        connection = get_sql_connection()
        user_id = auth_dao.register_user(connection,username,password)

        return jsonify({
            "message": "Registration successful",
            "user_id": user_id
        }), 201

    except Exception as e:
        print("=== ERROR ===")
        print(str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

    finally:
        if connection:
            connection.close()

@auth_bp.route('/login',methods=['POST'])
def login():
    connection = None
    try:
        connection = get_sql_connection()
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        result=auth_dao.login_user(connection, username, password)
        if result =="Incorrect username or password":
            return jsonify({"message": "Incorrect username or password"}), 401
        #this is to make sure the message "Login Successful" doesnt get when error
        return jsonify({
            "message": "Login successful",
            "result": result
        }), 200

    finally:
        if connection:
            connection.close()

