from flask import Flask
from flask_cors import CORS

def create_app():
    print("CREATE_APP START")

    app = Flask(__name__)

    from flask_cors import CORS
    CORS(
        app,
        origins=[
            "http://localhost:63342",
            "http://127.0.0.1:63342",
            "http://127.0.0.1:5500",
            "http://localhost:5500",
            "http://127.0.0.1:5501",
            "http://localhost:5501"
        ]
    )

    from app.routes.auth_routes import auth_bp
    from app.routes.event_routes import event_bp
    from app.routes.booking_routes import booking_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(booking_bp)

    print("URL MAP:", app.url_map)

    return app

