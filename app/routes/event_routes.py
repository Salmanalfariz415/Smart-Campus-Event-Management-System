from flask import request, jsonify, Blueprint
from app.db.sql_connection import get_sql_connection
import app.dao.event_dao as event_dao
import traceback
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os, uuid


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
        img = data.get('image')
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

@event_bp.route('/image_upload', methods=['POST', 'OPTIONS'])
@cross_origin(origins=["http://localhost:63342"])
def upload_image():
    UPLOAD_FOLDER = r"C:\Users\Salman AL Fariz\PyCharmMiscProject\app\static\uploads"

    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Secure + unique filename
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    image_url = f"/static/uploads/{filename}"

    return jsonify({
        "image_url": image_url
    }), 201

@event_bp.route('/add_card', methods=['GET', 'OPTIONS'])
@cross_origin(origins=["http://localhost:63342"])
def add_card():
    connection=None;
    try:
        connection = get_sql_connection()
        result=event_dao.eventcard(connection)
        return jsonify(result), 200
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        return jsonify({
            "error": "Event retrieval failed",
            "details": str(e)
        }), 500
    finally:
        if connection:
            connection.close()