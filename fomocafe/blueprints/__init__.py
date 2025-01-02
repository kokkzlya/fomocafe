from flask import Flask
from fomocafe.blueprints.api import bp as api_bp

def register_blueprints(app: Flask):
    app.register_blueprint(api_bp, url_prefix="/api")
