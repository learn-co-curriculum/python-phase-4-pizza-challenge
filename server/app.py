from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

# Initialize Flask App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Extensions
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def index():
    """Root endpoint"""
    return "<h1>Code Challenge</h1>"

# Restaurant Routes
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    """Get all restaurants"""
    return jsonify([restaurant.to_dict() for restaurant in Restaurant.query.all()])

@app.route("/restaurants/<int:id>", methods=["GET", "DELETE"])
def handle_restaurant(id):
    """Get or delete a restaurant by ID"""
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    if request.method == "GET":
        return jsonify({
            **restaurant.to_dict(),
            "restaurant_pizzas": [rp.to_dict() for rp in restaurant.restaurant_pizzas]
        })

    # DELETE
    db.session.delete(restaurant)
    db.session.commit()
    return "", 204

# Pizza Routes
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    """Get all pizzas"""
    return jsonify([pizza.to_dict() for pizza in Pizza.query.all()])

# RestaurantPizza Routes
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    """Create a new RestaurantPizza"""
    data = request.get_json()

    try:
        restaurant_pizza = RestaurantPizza(
            price=data["price"],
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"]
        )
        db.session.add(restaurant_pizza)
        db.session.commit()
        return jsonify(restaurant_pizza.to_dict()), 201
    except ValueError:
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)



