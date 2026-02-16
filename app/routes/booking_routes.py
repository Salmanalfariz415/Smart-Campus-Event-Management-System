from flask import request, jsonify, Blueprint
from app.db.sql_connection import get_sql_connection
import app.dao.booking_dao as booking_dao
import traceback
from flask_cors import cross_origin

booking_bp = Blueprint('booking', __name__, url_prefix='/booking')

@booking_bp.route('/create', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://localhost:63342", "http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5501", "http://localhost:5501"])
def create_booking():
    if request.method == 'OPTIONS':
        return '', 200
        
    connection = None
    try:
        connection = get_sql_connection()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['event_id', 'contact_name', 'contact_email']
        
        for field in required_fields:
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
        
        # Check available capacity
        capacity_query = """
        SELECT max_capacity, current_bookings, available_spots 
        FROM event_capacity WHERE event_id = %s
        """
        cursor = connection.cursor()
        cursor.execute(capacity_query, (data['event_id'],))
        capacity_result = cursor.fetchone()

        if capacity_result:
            max_capacity, current_bookings, available_spots = capacity_result
            attendees = data.get('attendees_count', 1)
            
            if available_spots < attendees:
                return {
                    'success': False,
                    'message': f'Not enough spots available. Only {available_spots} spots remaining.',
                    'available_spots': available_spots
                }

        # Update event capacity
        update_capacity_query = """
        UPDATE event_capacity 
        SET current_bookings = current_bookings + %s 
        WHERE event_id = %s
        """
        cursor.execute(update_capacity_query, (attendees, data['event_id']))
        
        result = booking_dao.create_booking(connection, data)
        
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
        print("=== BOOKING CREATION ERROR ===")
        print(str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

    finally:
        if connection:
            connection.close()

@booking_bp.route('/lookup/<booking_reference>', methods=['GET'])
@cross_origin(origins=["http://localhost:63342", "http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5501", "http://localhost:5501"])
def lookup_booking(booking_reference):
    connection = None
    try:
        connection = get_sql_connection()
        
        booking = booking_dao.get_booking_by_reference(connection, booking_reference)
        
        if not booking:
            return jsonify({"error": "Booking not found"}), 404
        
        return jsonify({
            "message": "Booking found",
            "booking": booking
        }), 200

    except Exception as e:
        print("=== BOOKING LOOKUP ERROR ===")
        print(str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

    finally:
        if connection:
            connection.close()

@booking_bp.route('/cancel', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://localhost:63342", "http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5501", "http://localhost:5501"])
def cancel_booking():
    if request.method == 'OPTIONS':
        return '', 200
        
    connection = None
    try:
        connection = get_sql_connection()
        data = request.get_json()
        
        booking_reference = data.get('booking_reference')
        if not booking_reference:
            return jsonify({"error": "Missing booking reference"}), 400
        
        result = booking_dao.cancel_booking(connection, booking_reference)
        
        if result['success']:
            return jsonify({"message": result['message']}), 200
        else:
            return jsonify({"error": result['message']}), 400

    except Exception as e:
        print("=== BOOKING CANCELLATION ERROR ===")
        print(str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

    finally:
        if connection:
            connection.close()

@booking_bp.route('/event/<int:event_id>', methods=['GET'])
@cross_origin(origins=["http://localhost:63342", "http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5501", "http://localhost:5501"])
def get_event_bookings(event_id):
    connection = None
    try:
        connection = get_sql_connection()
        
        bookings = booking_dao.get_event_bookings(connection, event_id)
        
        return jsonify({
            "message": "Bookings retrieved successfully",
            "bookings": bookings,
            "total_bookings": len(bookings)
        }), 200

    except Exception as e:
        print("=== EVENT BOOKINGS ERROR ===")
        print(str(e))
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

    finally:
        if connection:
            connection.close()