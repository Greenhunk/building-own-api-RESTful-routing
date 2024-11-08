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

@app.route("/search")
def search_cafe():
    query_location = request.args.get("loc")
    result = db.session.execute(db.select(Cafe).where(Cafe.location == query_location))
    cafe_loc = result.scalars().all()
    if cafe_loc:
        cafe_loc_list = []
        for cafe in cafe_loc:
            cafe_loc_list.append({
                'can_take_calls': cafe.can_take_calls,
                'coffee_price': cafe.coffee_price,
                'has_sockets': cafe.has_sockets,
                'has_toilet': cafe.has_toilet,
                'has_wifi': cafe.has_wifi,
                'id': cafe.id,
                'img_url': cafe.img_url,
                'location': cafe.location,
            })
        return jsonify(cafes=cafe_loc_list)
    else:
        return jsonify(error = {"Not Found": "Sorry, we don't have a cafe at that location"})

# HTTP POST - Create Record
@app.route("/add", methods= ["POST"])
def add_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods= ["PATCH"])
def cafe_price_update(cafe_id):
    new_price_coffee = request.args.get("new_price")
    result = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id))
    selected_cafe= result.scalar()
    if selected_cafe:
        selected_cafe.coffee_price = new_price_coffee
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(response={"Not found": "Invalid ID."})
# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods= ["DELETE"])
def del_cafe(cafe_id):
    api_key = request.args.get("api_key")
    result = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id))
    selected_cafe = result.scalar()
    if selected_cafe:
        if api_key == "TopSecretAPIKey":
            db.session.delete(selected_cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe."})
        else:
            return jsonify(response={"Error": "API key not valid"})
    else:
        return jsonify(response={"Not found": "Invalid ID."})





if __name__ == '__main__':
    app.run(debug=True)
