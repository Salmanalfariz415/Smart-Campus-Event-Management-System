from flask import request, jsonify, Blueprint
from app.db.sql_connection import get_sql_connection
from app.dao.auth_dao import register_user
import traceback
from flask_cors import cross_origin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
print("AUTH_ROUTES FILE LOADED")
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
        user_id = register_user(connection, username, password)

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
