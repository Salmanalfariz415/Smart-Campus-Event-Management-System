from flask import request, jsonify, Blueprint
from app.db.sql_connection import get_sql_connection
import app.dao.auth_dao as auth_dao
import app.dao.booking_dao as booking_dao
import traceback
from flask_cors import cross_origin
import jwt
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

CORS_ORIGINS = ["http://localhost:63342", "http://127.0.0.1:5500", "http://localhost:5500",
                "http://127.0.0.1:5501", "http://localhost:5501"]

def _get_user_id_from_token():
    """Decode the Bearer JWT and return (user_id, user_type) or raise ValueError."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise ValueError('Missing or malformed Authorization header')
    token = auth_header.split(' ', 1)[1]
    payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
    return payload['user_id'], payload.get('user_type', 'user')

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

@auth_bp.route('/register_organizer', methods=['POST', 'OPTIONS'])
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
                          'email', 'phone', 'password']
        
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


# ── Profile endpoints ─────────────────────────────────────────────────────────

@auth_bp.route('/profile', methods=['GET', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def get_profile():
    """Return the authenticated user's profile data."""
    if request.method == 'OPTIONS':
        return '', 200
    connection = None
    try:
        user_id, user_type = _get_user_id_from_token()
        connection = get_sql_connection()
        user_data = auth_dao.get_user_details(connection, user_id)
        if not user_data:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"profile": user_data}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()


@auth_bp.route('/my-bookings', methods=['GET', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def get_my_bookings():
    """Return all bookings belonging to the authenticated user."""
    if request.method == 'OPTIONS':
        return '', 200
    connection = None
    try:
        user_id, _ = _get_user_id_from_token()
        connection = get_sql_connection()
        bookings = booking_dao.get_user_bookings(connection, user_id)
        return jsonify({"bookings": bookings}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()


@auth_bp.route('/profile/update', methods=['POST', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def update_profile():
    """Update organizer details for the authenticated organizer user."""
    if request.method == 'OPTIONS':
        return '', 200
    connection = None
    try:
        user_id, user_type = _get_user_id_from_token()
        if user_type != 'organizer':
            return jsonify({"error": "Only organizers can update organization info"}), 403

        data = request.get_json()
        connection = get_sql_connection()
        cursor = connection.cursor()
        update_query = """
        UPDATE organizers
        SET org_name = %s, org_type = %s, org_description = %s,
            contact_name = %s, contact_position = %s, phone = %s
        WHERE user_id = %s
        """
        cursor.execute(update_query, (
            data.get('org_name'),
            data.get('org_type'),
            data.get('org_description', ''),
            data.get('contact_name'),
            data.get('contact_position'),
            data.get('phone'),
            user_id
        ))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Profile updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()


@auth_bp.route('/change-password', methods=['POST', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def change_password():
    """Change the authenticated user's password."""
    if request.method == 'OPTIONS':
        return '', 200
    connection = None
    try:
        user_id, _ = _get_user_id_from_token()
        data = request.get_json()
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')

        if not current_password or not new_password:
            return jsonify({"error": "Both current and new password are required"}), 400
        if len(new_password) < 6:
            return jsonify({"error": "New password must be at least 6 characters"}), 400

        connection = get_sql_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT password_hash FROM users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "User not found"}), 404

        stored_hash = row[0]
        if not bcrypt.checkpw(current_password.encode('utf-8'), stored_hash.encode('utf-8')):
            return jsonify({"error": "Current password is incorrect"}), 401

        new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (new_hash, user_id))
        connection.commit()
        cursor.close()
        return jsonify({"message": "Password changed successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()
