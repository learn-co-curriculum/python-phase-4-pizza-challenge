#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
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
@app.route('/pizza')
def all_pizza():
    pizza = Pizza.query.all()
    pizza_list = []

    for user in pizza:
        pizza_list.append(pizza.to_dict())

    body = {
        "count": len(pizza_list),
        "pizza": pizza_list
    }

    return make_response(body, 200)


@app.route('/pizza/<int:id>')
@app.route('/pizza', methods=['GET', 'POST'])
def pizza():
    if request.method == 'GET':
        pizza = Pizza.query.all()
        pizza_list = []

        for user in pizza:
            pizza_list.append(pizza.to_dict())

        body = {
            "count": len(pizza_list),
            "pizza": pizza_list
        }

        return make_response(body, 200)
    
    elif request.method == 'POST':
        new_pizza = Pizza(
            name=request.form.get("name"),
            ingredients=request.form.get("ingredients")
        )

        db.session.add(new_pizza)
        db.session.commit()

        response = make_response(new_pizza.to_dict(), 201)

        return response


@app.route('/pizza/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def pizza_by_id(id):
    user = Pizza.query.filter_by(id=id).first()

    if pizza == None:
        body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(body, 404)

        return response
    
    else:
        if request.method == 'GET':
            pizza_dict = pizza.to_dict()

            response = make_response(pizza_dict, 200)

            return response

        elif request.method == 'PATCH':
            for attr in request.json:
                setattr(pizza, attr, request.json.get(attr))

            db.session.add(pizza)
            db.session.commit()

            pizza_dict = pizza.to_dict()

            response = make_response(pizza_dict, 200)

            return response
        
        elif request.method == 'DELETE':
            db.session.delete(pizza)
            db.session.commit()

            body = {
                "delete_successful": True,
                "message": "Pizza deleted."
            }

            response = make_response(body, 200)

            return response

def pizza_by_id(id):
    pizza =  Pizza.query.filter_by(id=id).first()

    if Pizza:
        body = Pizza.to_dict()
        status = 200
    else:
        body = {
            "message": f"Pizza id:{id} not found."
        }
        status = 404

    return make_response(body, status)



if __name__ == "__main__":
    app.run(port=5555, debug=True)
