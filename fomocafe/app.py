from flask import Flask
from flask_cors import CORS

from fomocafe import db
from fomocafe.blueprints import register_blueprints

app = Flask(__name__)
app.config.from_object("fomocafe.config.Config")
db.init_app(app)
register_blueprints(app)
CORS(app)

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"])
