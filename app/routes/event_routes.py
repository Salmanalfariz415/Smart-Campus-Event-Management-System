from flask import request, jsonify, Blueprint
from app.db.sql_connection import get_sql_connection
import app.dao.event_dao as event_dao
import traceback
from flask_cors import cross_origin


event_bp = Blueprint('event', __name__, url_prefix='/event')

@event_bp.route('/submit', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://localhost:63342"])
def submit():
    connection = None
    try:
        data = request.get_json()

        username = data.get('username')
        description = data.get('description')
        organization = data.get('organization')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        venue = data.get('venue')
        building = data.get('building')
        capacity = data.get('capacity')
        fee = data.get('fee')
        reg = data.get('reg')
        img = data.get('img')
        contact = data.get('contact')
        website = data.get('website')
        tag = data.get('tag')

        connection = get_sql_connection()

        event_id = event_dao.submitl(
            connection, username, description, organization,
            start_date, end_date, start_time, end_time,
            venue, building, capacity, fee, reg,
            img, contact, website, tag
        )

        return jsonify({
            "message": "Registration successful",
            "user_id": event_id
        }), 201

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        return jsonify({
            "error": "Event submission failed",
            "details": str(e)
        }), 500

    finally:
        if connection:
            connection.close()
