from flask import request, jsonify, Blueprint, render_template
import app.dao.event_dao as event_dao
import traceback
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from app.supabase_client import supabase

import os, uuid

CORS_ORIGINS = ["http://localhost:63342", "http://127.0.0.1:5500", "http://localhost:5500",
                "http://127.0.0.1:5501", "http://localhost:5501"]

event_bp = Blueprint('event', __name__, url_prefix='/event')

@event_bp.route('/events', methods=['GET'])
def events_page():
    """Serve the events HTML page"""
    return render_template('events.html')

@event_bp.route('/submit', methods=['POST', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def submit():
    try:
        data = request.get_json()

        event_id = event_dao.submitl(
            data.get('username'),
            data.get('event_type'),
            data.get('event_sub_type'),
            data.get('description'),
            data.get('organization'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('start_time'),
            data.get('end_time'),
            data.get('venue'),
            data.get('building'),
            data.get('capacity'),
            data.get('fee'),
            data.get('reg'),
            data.get('image'),
            data.get('contact'),
            data.get('website'),
            data.get('tag'),
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

@event_bp.route('/image_upload', methods=['POST', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        ext = os.path.splitext(file.filename)[1]
        filename = f"events/{uuid.uuid4()}{ext}"

        file_bytes = file.read()

        response = supabase.storage.from_("event-images").upload(
            filename,
            file_bytes,
            {"content-type": file.content_type}
        )

        public_url = supabase.storage.from_("event-images").get_public_url(filename)

        return jsonify({"image_url": public_url}), 201

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return jsonify({"error": str(e)}), 500


@event_bp.route('/add_card', methods=['GET', 'OPTIONS'])
@cross_origin(origins=CORS_ORIGINS)
def add_card():
    try:
        result = event_dao.eventcard()
        return jsonify(result), 200
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        return jsonify({
            "error": "Event retrieval failed",
            "details": str(e)
        }), 500