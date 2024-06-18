from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from .routes.model_routes import model_bp
    app.register_blueprint(model_bp, url_prefix='/api/models')

    return app
