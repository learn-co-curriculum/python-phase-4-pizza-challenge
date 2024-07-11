from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)


    restaurantPizza = db.relationship("RestaurantPizza", back_populates="restaurant")

    serialize_rules = ('-restaurantPizza.user')

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurantPizza= db.relationship("RestaurantPIzza", back_populates="Pizza") 

    serialize_rules = ('-restaurantPizza.user')

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    
    pizza = db.relationship("pizza", back_populates="restaurantPizza")
    restaurant = db.relationship("Restaurant", back_populates="restaurantPizza")

    serialize_rules = ('-pizza.restaurantPIzza', '-restaurant.restaurantPizza')



    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
