import mysql.connector
import random
import string
from datetime import datetime

def generate_booking_reference():
    """Generate a unique booking reference like BK001234"""
    random_num = ''.join(random.choices(string.digits, k=6))
    return f"BK{random_num}"

def create_booking(connection, booking_data):
    """Create a new booking for an event"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Generate unique booking reference
        booking_ref = generate_booking_reference()
        
        # Check if booking reference already exists (very unlikely but safe)
        while True:
            check_query = "SELECT id FROM bookings WHERE booking_reference = %s"
            cursor.execute(check_query, (booking_ref,))
            if not cursor.fetchone():
                break
            booking_ref = generate_booking_reference()
        
        # Check available capacity
        capacity_query = """
        SELECT max_capacity, current_bookings, available_spots 
        FROM event_capacity WHERE event_id = %s
        """
        cursor.execute(capacity_query, (booking_data['event_id'],))
        capacity_result = cursor.fetchone()
        
        if capacity_result:
            max_capacity, current_bookings, available_spots = capacity_result
            attendees = booking_data.get('attendees_count', 1)
            
            if available_spots < attendees:
                return {
                    'success': False,
                    'message': f'Not enough spots available. Only {available_spots} spots remaining.',
                    'available_spots': available_spots
                }
        
        # Create the booking
        booking_query = """
        INSERT INTO bookings 
        (event_id, user_id, booking_reference, attendees_count, contact_name, 
         contact_email, contact_phone, special_requirements, payment_amount, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        booking_values = (
            booking_data['event_id'],
            booking_data.get('user_id'),  # None for guest bookings
            booking_ref,
            booking_data.get('attendees_count', 1),
            booking_data['contact_name'],
            booking_data['contact_email'],
            booking_data.get('contact_phone', ''),
            booking_data.get('special_requirements', ''),
            booking_data.get('payment_amount', 0.00),
            'confirmed'  # Auto-confirm for now
        )
        
        cursor.execute(booking_query, booking_values)
        booking_id = cursor.lastrowid
        
        # Update event capacity
        update_capacity_query = """
        UPDATE event_capacity 
        SET current_bookings = current_bookings + %s 
        WHERE event_id = %s
        """
        cursor.execute(update_capacity_query, (booking_data.get('attendees_count', 1), booking_data['event_id']))
        
        # Log the booking creation
        log_query = """
        INSERT INTO booking_logs (booking_id, action, new_status, notes)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(log_query, (booking_id, 'created', 'confirmed', 'Booking created successfully'))
        
        connection.commit()
        
        return {
            'success': True,
            'booking_id': booking_id,
            'booking_reference': booking_ref,
            'message': 'Booking confirmed successfully!'
        }
        
    except mysql.connector.Error as e:
        connection.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()

def get_booking_by_reference(connection, booking_reference):
    """Get booking details by reference number"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT b.id, b.event_id, b.booking_reference, b.attendees_count, 
               b.status, b.contact_name, b.contact_email, b.contact_phone,
               b.special_requirements, b.payment_amount, b.payment_status,
               b.booking_date, b.created_at,
               e.title as event_title, e.start_date, e.start_time, e.venue
        FROM bookings b
        JOIN events e ON b.event_id = e.id
        WHERE b.booking_reference = %s
        """
        
        cursor.execute(query, (booking_reference,))
        result = cursor.fetchone()
        
        if not result:
            return None
            
        booking_data = {
            'id': result[0],
            'event_id': result[1],
            'booking_reference': result[2],
            'attendees_count': result[3],
            'status': result[4],
            'contact_name': result[5],
            'contact_email': result[6],
            'contact_phone': result[7],
            'special_requirements': result[8],
            'payment_amount': float(result[9]) if result[9] else 0.00,
            'payment_status': result[10],
            'booking_date': result[11].strftime('%Y-%m-%d %H:%M:%S') if result[11] else '',
            'created_at': result[12].strftime('%Y-%m-%d %H:%M:%S') if result[12] else '',
            'event_details': {
                'title': result[13],
                'start_date': result[14].strftime('%Y-%m-%d') if result[14] else '',
                'start_time': str(result[15]) if result[15] else '',
                'venue': result[16]
            }
        }
        
        return booking_data
        
    except mysql.connector.Error as e:
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()

def cancel_booking(connection, booking_reference):
    """Cancel a booking by reference number"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        # Get current booking details
        get_query = "SELECT id, event_id, attendees_count, status FROM bookings WHERE booking_reference = %s"
        cursor.execute(get_query, (booking_reference,))
        result = cursor.fetchone()
        
        if not result:
            return {'success': False, 'message': 'Booking not found'}
            
        booking_id, event_id, attendees_count, current_status = result
        
        if current_status == 'cancelled':
            return {'success': False, 'message': 'Booking is already cancelled'}
        
        # Update booking status
        update_query = "UPDATE bookings SET status = 'cancelled', updated_at = NOW() WHERE booking_reference = %s"
        cursor.execute(update_query, (booking_reference,))
        
        # Update event capacity
        capacity_query = """
        UPDATE event_capacity 
        SET current_bookings = current_bookings - %s 
        WHERE event_id = %s
        """
        cursor.execute(capacity_query, (attendees_count, event_id))
        
        # Log the cancellation
        log_query = """
        INSERT INTO booking_logs (booking_id, action, old_status, new_status, notes)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(log_query, (booking_id, 'cancelled', current_status, 'cancelled', 'Booking cancelled by user'))
        
        connection.commit()
        
        return {'success': True, 'message': 'Booking cancelled successfully'}
        
    except mysql.connector.Error as e:
        connection.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()

def get_event_bookings(connection, event_id):
    """Get all bookings for a specific event"""
    cursor = None
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT booking_reference, contact_name, contact_email, attendees_count, 
               status, booking_date, payment_status
        FROM bookings 
        WHERE event_id = %s 
        ORDER BY booking_date DESC
        """
        
        cursor.execute(query, (event_id,))
        results = cursor.fetchall()
        
        bookings = []
        for result in results:
            bookings.append({
                'booking_reference': result[0],
                'contact_name': result[1],
                'contact_email': result[2],
                'attendees_count': result[3],
                'status': result[4],
                'booking_date': result[5].strftime('%Y-%m-%d %H:%M:%S') if result[5] else '',
                'payment_status': result[6]
            })
        
        return bookings
        
    except mysql.connector.Error as e:
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()