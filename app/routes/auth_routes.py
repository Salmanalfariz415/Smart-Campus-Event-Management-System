from flask import request, jsonify, Blueprint
import app.dao.auth_dao as auth_dao
import app.dao.booking_dao as booking_dao
import traceback
from flask_cors import cross_origin
import jwt
import os
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
@cross_origin(origins=CORS_ORIGINS)
def register():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        result = auth_dao.register_user(data.get('username'), data.get('password'))
        return jsonify({
            "message": "Registration successful",
            "user_id": result["user_id"],
            "token": result["token"]
        }), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400


@auth_bp.route('/login', methods=['POST'])
@cross_origin(origins=CORS_ORIGINS)
def login():
    try:
        data = request.get_json()
        result = auth_dao.login_user(data.get('username'), data.get('password'))
        if result == "Incorrect username or password":
            return jsonify({"message": "Incorrect username or password"}), 401
        return jsonify({"message": "Login successful", "result": result}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/register_organizer', methods=['POST', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def register_organizer():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        required_fields = ['org_name', 'org_type', 'contact_name', 'contact_position',
                           'email', 'phone', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400
        if data.get('password') != data.get('confirm_password'):
            return jsonify({"error": "Passwords do not match"}), 400

        result = auth_dao.register_organizer(data)
        return jsonify({
            "message": "Organizer registration successful",
            "user_id": result['user_id'],
            "organizer_id": result['organizer_id'],
            "token": result['token']
        }), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ── Profile endpoints ─────────────────────────────────────────────────────────

@auth_bp.route('/profile', methods=['GET', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def get_profile():
    """Return the authenticated user's profile data."""
    if request.method == 'OPTIONS':
        return '', 200
    try:
        user_id, _ = _get_user_id_from_token()
        user_data = auth_dao.get_user_details(user_id)
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
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/my-bookings', methods=['GET', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def get_my_bookings():
    """Return all bookings belonging to the authenticated user."""
    if request.method == 'OPTIONS':
        return '', 200
    try:
        user_id, _ = _get_user_id_from_token()
        bookings = booking_dao.get_user_bookings(user_id)
        return jsonify({"bookings": bookings}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/profile/update', methods=['POST', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def update_profile():
    """Update organizer details for the authenticated organizer user."""
    if request.method == 'OPTIONS':
        return '', 200
    try:
        user_id, user_type = _get_user_id_from_token()
        if user_type != 'organizer':
            return jsonify({"error": "Only organizers can update organization info"}), 403
        data = request.get_json()
        auth_dao.update_organizer(user_id, data)
        return jsonify({"message": "Profile updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/change-password', methods=['POST', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def change_password():
    """Change the authenticated user's password."""
    if request.method == 'OPTIONS':
        return '', 200
    try:
        user_id, _ = _get_user_id_from_token()
        data = request.get_json()
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')

        if not current_password or not new_password:
            return jsonify({"error": "Both current and new password are required"}), 400
        if len(new_password) < 6:
            return jsonify({"error": "New password must be at least 6 characters"}), 400

        ok = auth_dao.change_password(user_id, current_password, new_password)
        if not ok:
            return jsonify({"error": "Current password is incorrect"}), 401
        return jsonify({"message": "Password changed successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
