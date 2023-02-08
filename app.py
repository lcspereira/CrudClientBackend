from flask import Flask
from flask_migrate import Migrate
from models import db
from api.cliente import ClienteListResource, ClienteResource
from api.item import ItemListResource, ItemResource, ItemListByClienteResource
from api import api
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("CRUD_DB_URL")

db.init_app(app)
api.init_app(app)


migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
