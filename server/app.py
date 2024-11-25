from flask import Flask, request
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
    restaurants = Restaurant.query.all()
    return [restaurant.to_dict() for restaurant in restaurants], 200

@app.route("/restaurants/<int:id>", methods=["GET", "DELETE"])
def handle_restaurant(id):
    """Get or delete a restaurant by ID"""
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return {"error": "Restaurant not found"}, 404

    if request.method == "GET":
        return {
            **restaurant.to_dict(),
            "restaurant_pizzas": [rp.to_dict() for rp in restaurant.restaurant_pizzas]
        }, 200

    # DELETE
    db.session.delete(restaurant)
    db.session.commit()
    return "", 204

# Pizza Routes
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    """Get all pizzas"""
    pizzas = Pizza.query.all()
    return [pizza.to_dict() for pizza in pizzas], 200

@app.route("/pizzas/<int:id>", methods=["GET", "DELETE"])
def handle_pizza(id):
    """Get or delete a pizza by ID"""
    pizza = db.session.get(Pizza, id)
    if not pizza:
        return {"error": "Pizza not found"}, 404

    if request.method == "GET":
        return pizza.to_dict(), 200

    # DELETE
    db.session.delete(pizza)
    db.session.commit()
    return "", 204

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
        return restaurant_pizza.to_dict(), 201
    except ValueError:
        return {"errors": ["validation errors"]}, 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)





