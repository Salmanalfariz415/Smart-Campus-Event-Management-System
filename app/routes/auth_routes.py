from flask import request, jsonify, Blueprint
from app.db.sql_connection import get_sql_connection
import app.dao.auth_dao as auth_dao
import traceback
from flask_cors import cross_origin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://localhost:63342", "http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5501", "http://localhost:5501"])
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

@auth_bp.route('/register-organizer', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://localhost:63342", "http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5501", "http://localhost:5501"])
def register_organizer():
    if request.method == 'OPTIONS':
        return '', 200
        
    connection = None
    try:
        connection = get_sql_connection()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['org_name', 'org_type', 'contact_name', 'contact_position', 
                          'email', 'phone', 'username', 'password']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Check password confirmation
        if data.get('password') != data.get('confirm_password'):
            return jsonify({"error": "Passwords do not match"}), 400
            
        result = auth_dao.register_organizer(connection, data)
        
        return jsonify({
            "message": "Organizer registration successful",
            "user_id": result['user_id'],
            "organizer_id": result['organizer_id']
        }), 201

    except Exception as e:
        print("=== ORGANIZER REGISTRATION ERROR ===")
        print(str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

    finally:
        if connection:
            connection.close()