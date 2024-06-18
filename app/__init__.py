from flask import Flask, send_from_directory
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)

    # Enable CORS for the specific origin
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .routes.model_routes import model_bp
    app.register_blueprint(model_bp, url_prefix='/api/models')

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                   'favicon.ico', mimetype='image/vnd.microsoft.icon')

    return app
