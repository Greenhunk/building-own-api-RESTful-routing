import random

import flask.json
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe = {
        'can_take_calls': random_cafe.can_take_calls,
        'coffee_price': random_cafe.coffee_price,
        'has_sockets': random_cafe.has_sockets,
        'has_toilet': random_cafe.has_toilet,
        'has_wifi': random_cafe.has_wifi,
        'id': random_cafe.id,
        'img_url': random_cafe.img_url,
        'location': random_cafe.location,




    })
@app.route("/all")
def get_all_cafe():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    all_cafes_list = []
    for cafe in all_cafes:
        all_cafes_list.append({
            'can_take_calls': cafe.can_take_calls,
            'coffee_price': cafe.coffee_price,
            'has_sockets': cafe.has_sockets,
            'has_toilet': cafe.has_toilet,
            'has_wifi': cafe.has_wifi,
            'id': cafe.id,
            'img_url': cafe.img_url,
            'location': cafe.location,

        })
    return jsonify(cafes=all_cafes_list)


# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
