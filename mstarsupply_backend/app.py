from flask import Flask
from flask_cors import CORS

from mstarsupply_backend.database import configure_db
from product.routes import bp_product

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite+pysqlite:///:memory:"
    app.config["SQLALCHEMY_ECHO"] = True

    # CORS
    CORS(app)

    # DB
    configure_db(app)

    #BLUEPRINTS
    app.register_blueprint(bp_product)

    return app
