from flask import Flask
from flask_migrate import Migrate
from models import db
from api.cliente import api, ClienteListResource, ClienteResource

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:crudclient@127.0.0.1:5432/crud"

db.init_app(app)
api.init_app(app)

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)
