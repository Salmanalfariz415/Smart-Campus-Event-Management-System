from flask import Flask
from flask_cors import CORS

def create_app():
    print("CREATE_APP START")

    app = Flask(__name__)
    CORS(
        app,
        origins=["http://localhost:63342", "http://127.0.0.1:63342", "*"],
        supports_credentials=True
    )

    from app.routes.auth_routes import auth_bp
    from app.routes.event_routes import event_bp
    print("REGISTERING AUTH BLUEPRINT")
    app.register_blueprint(auth_bp)#important
    app.register_blueprint(event_bp)

    print("URL MAP:", app.url_map)

    return app
