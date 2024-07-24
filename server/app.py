#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict(rules=('-restaurant_pizzas',)) for restaurant in restaurants])

class RestaurantDetail(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)
        if restaurant:
            return restaurant.to_dict()
        return {'error': 'Restaurant not found'}, 404

    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return {}, 204
        return {'error': 'Restaurant not found'}, 404

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict(rules=('-restaurant_pizzas',)) for pizza in pizzas])

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        try:
            restaurant_pizza = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id']
            )
            db.session.add(restaurant_pizza)
            db.session.commit()
            return restaurant_pizza.to_dict(), 201
        except ValueError as e:
            return {'errors': [str(e)]}, 400
        except Exception as e:
            return {'errors': [str(e)]}, 500

api.add_resource(Restaurants, '/restaurants')
api.add_resource(RestaurantDetail, '/restaurants/<int:id>')
api.add_resource(Pizzas, '/pizzas')
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == "__main__":
    app.run(port=5555, debug=True)