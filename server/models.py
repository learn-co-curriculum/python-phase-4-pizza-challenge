from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import relationship, validates
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
    restaurant_pizzas = relationship("RestaurantPizza", back_populates="restaurant")
    pizzas = association_proxy('restaurant_pizzas', 'pizza')
    serialize_rules = ("-restaurant_pizzas.restaurant",)


    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = relationship("RestaurantPizza", back_populates="pizza")
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')


    # add serialization rules
    serialize_rules = ("-restaurant_pizzas.pizza",)


    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    restaurant_id = db.Column(db.Integer, ForeignKey('restaurants.id'))
    pizza_id = db.Column(db.Integer, ForeignKey('pizzas.id'))


    restaurant = relationship("Restaurant", back_populates="restaurant_pizzas")
    pizza = relationship("Pizza", back_populates="restaurant_pizzas")


    serialize_rules = ("-restaurant.restaurant_pizzas", "-pizza.restaurant_pizzas")

    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("validation errors")
        return price

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
    