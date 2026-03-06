from flask import request, jsonify, Blueprint
import app.dao.booking_dao as booking_dao
import traceback
from flask_cors import cross_origin
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

CORS_ORIGINS = ["http://localhost:63342", "http://127.0.0.1:5500", "http://localhost:5500",
                "http://127.0.0.1:5501", "http://localhost:5501"]

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

def _get_user_id_from_token():
    """Extract user_id from Bearer JWT. Returns None if token is absent or invalid."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    try:
        token = auth_header.split(' ', 1)[1]
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.PyJWTError:
        return None


@booking_bp.route('/create', methods=['POST', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def create_booking():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()

        # Attach user_id from JWT if the request is authenticated
        user_id = _get_user_id_from_token()
        if user_id:
            data['user_id'] = user_id

        # Validate required fields
        for field in ['event_id', 'contact_name', 'contact_email']:
            if not data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Validate email format (basic)
        email = data.get('contact_email')
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format"}), 400

        # Validate attendees count
        attendees = data.get('attendees_count', 1)
        if not isinstance(attendees, int) or attendees < 1 or attendees > 10:
            return jsonify({"error": "Attendees count must be between 1 and 10"}), 400

        result = booking_dao.create_booking(data)

        if result['success']:
            return jsonify({
                "message": result['message'],
                "booking_reference": result['booking_reference'],
                "booking_id": result['booking_id']
            }), 201
        else:
            return jsonify({
                "error": result['message'],
                "available_spots": result.get('available_spots', 0)
            }), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@booking_bp.route('/lookup/<booking_reference>', methods=['GET'])
@cross_origin(origins=CORS_ORIGINS)
def lookup_booking(booking_reference):
    try:
        booking = booking_dao.get_booking_by_reference(booking_reference)
        if not booking:
            return jsonify({"error": "Booking not found"}), 404
        return jsonify({"message": "Booking found", "booking": booking}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@booking_bp.route('/cancel', methods=['POST', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def cancel_booking():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json()
        booking_reference = data.get('booking_reference')
        if not booking_reference:
            return jsonify({"error": "Missing booking reference"}), 400

        result = booking_dao.cancel_booking(booking_reference)

        if result['success']:
            return jsonify({"message": result['message']}), 200
        else:
            return jsonify({"error": result['message']}), 400

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@booking_bp.route('/event/<int:event_id>', methods=['GET'])
@cross_origin(origins=CORS_ORIGINS)
def get_event_bookings(event_id):
    try:
        bookings = booking_dao.get_event_bookings(event_id)
        return jsonify({
            "message": "Bookings retrieved successfully",
            "bookings": bookings,
            "total_bookings": len(bookings)
        }), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500