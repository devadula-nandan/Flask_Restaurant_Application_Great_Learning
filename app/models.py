from app import application
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Date

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:nandan123@localhost/FlaskRestaurant'
#application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)


class Customer(db.Model):
    __tablename__ = 'customer'
    cust_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    username = Column(String(255), unique=True)
    password = Column(String(255))
    level = Column(Integer)

    def __init__(self, cust_id, name, username, password, level):
        self.cust_id = cust_id
        self.name = name
        self.username = username
        self.password = password
        self.level = level


class Vendor(db.Model):
    __tablename__ = 'vendor'
    vendor_id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey("customer.cust_id"))
    restaurant_name = Column(String(255))

    def __init__(self, vendor_id, cust_id, restaurant_name):
        self.vendor_id = vendor_id
        self.cust_id = cust_id
        self.restaurant_name = restaurant_name


class Food(db.Model):
    __tablename__ = 'food'
    food_id = Column(Integer, primary_key=True)
    vendor_id = Column(Integer, ForeignKey("vendor.vendor_id"))
    dish_name = Column(String(255),unique=True)
    calories_per_gm = Column(Integer)
    available_quantity = Column(Integer)
    unit_price = Column(Integer)

    def __init__(self, food_id, vendor_id, dish_name, calories_per_gm, available_quantity, unit_price):
        self.food_id = food_id
        self.vendor_id = vendor_id
        self.dish_name = dish_name
        self.calories_per_gm = calories_per_gm
        self.available_quantity = available_quantity
        self.unit_price = unit_price


class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey("customer.cust_id"))
    total_amount = Column(Integer)
    date = Column(Date)

    def __init__(self, order_id, cust_id, total_amount, date):
        self.order_id = order_id
        self.cust_id = cust_id
        self.total_amount = total_amount
        self.date = date


class OrderItems(db.Model):
    __tablename__ = 'orderItems'
    item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    food_id = Column(Integer, ForeignKey("food.food_id"))
    quantity = Column(Integer)
    amount = Column(Integer)

    def __init__(self, item_id, order_id, food_id, quantity, amount):
        self.item_id = item_id
        self.order_id = order_id
        self.food_id = food_id
        self.quantity = quantity
        self.amount = amount


class Cart(db.Model):
    __tablename__ = 'cart'
    cart_item_id = Column(Integer, primary_key=True)
    cust_id = Column(Integer, ForeignKey('customer.cust_id'))
    food_id = Column(Integer, ForeignKey("food.food_id"))
    quantity = Column(Integer)
    amount = Column(Integer)

    def __init__(self, cart_item_id, cust_id, food_id, quantity, amount):
        self.cart_item_id = cart_item_id
        self.cust_id = cust_id
        self.food_id = food_id
        self.quantity = quantity
        self.amount = amount


db.create_all()
db.session.commit()
