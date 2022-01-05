from flask import request, jsonify, session
from flask_restful import Resource
from app import *
from app.models import db, Customer, Vendor, Food, Orders, OrderItems, Cart
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
import uuid
from datetime import datetime

# uuid function (for change here to change everywhere functionality)
def generateId():
    return int(str(uuid.uuid4().int)[:5])

# function to make dictionaries out of queried table
def getOrders(_orders):
    orders = []
    for _order in _orders:
        order = dict()
        order['order_id'] = _order.order_id
        order['cust_id'] = _order.cust_id
        order['total_amount'] = _order.total_amount
        order['date'] = _order.date
        orders.append(order)
    return orders

# fields
class Add_CustomerRequest(Schema):
    name = fields.Str()
    username = fields.Str()
    password = fields.Str()
    level = fields.Int()


class LoginRequest(Schema):
    username = fields.Str()
    password = fields.Str()


class Add_VendorRequest(Schema):
    cust_id = fields.Int()
    restaurant_name = fields.Str()


class Add_Food_ItemRequest(Schema):
    vendor_id = fields.Int()
    dish_name = fields.Str()
    calories_per_gm = fields.Int()
    available_quantity = fields.Int()
    unit_price = fields.Int()


class Add_To_CartRequest(Schema):
    food_id = fields.Int()
    quantity = fields.Int()


class APIResponse(Schema):
    message = fields.Str(default="Success")


class VendorsResponse(Schema):
    message = fields.Str(default="Success")
    vendors = fields.List(fields.Dict())


class OrdersResponse(Schema):
    message = fields.Str(default="Success")
    orders = fields.List(fields.Dict())


# 1a
class Add_Customer(MethodResource, Resource):
    @doc(description='Add Customer', tags=['Add Customer API'])
    @use_kwargs(Add_CustomerRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            name, username, password, level = kwargs['name'], kwargs[
                'username'], kwargs['password'], kwargs['level']
            if not name or not username or not password or level is None:
                return APIResponse().dump(dict(message='Incomplete customer information provided')), 400
            if level == 0:
                customer = Customer(
                    cust_id=generateId(),
                    name=name,
                    username=username,
                    password=password,
                    level=level
                )
                db.session.add(customer)
                db.session.commit()
                return APIResponse().dump(dict(message='New customer added'))
            else:
                return APIResponse().dump(dict(message='Initial sign up should be of customer, try level = 0')), 201
        except Exception as e:
            return APIResponse().dump(dict(message=f'Unable to add customer{str(e)}')), 400


api.add_resource(Add_Customer, '/add_customer')
docs.register(Add_Customer)


# 1b
class Login(MethodResource, Resource):
    @doc(description='Login', tags=['Login API'])
    @use_kwargs(LoginRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            username, password = kwargs['username'], kwargs['password']
            if not username or not password:
                return APIResponse().dump(dict(message='Incomplete credentials provided')), 400
            customer = Customer.query.filter_by(
                username=username, password=password).first()
            if customer:
                session['cust_id'] = customer.cust_id
                return APIResponse().dump(dict(message='Login successful')), 200
            return APIResponse().dump(dict(message='Customer does not exist')), 401
        except Exception as e:
            return APIResponse().dump(dict(message=f'Login unsuccessful {str(e)}')), 400


api.add_resource(Login, '/login')
docs.register(Login)


# 1c
class Logout(MethodResource, Resource):
    @doc(description='Logout API', tags=['Logout API'])
    @marshal_with(APIResponse)
    def delete(self):
        try:
            if session['cust_id']:
                session['cust_id'] = None
                return APIResponse().dump(dict(message='Logged out successfully')), 200
            else:
                return APIResponse().dump(dict(message='Not logged in')), 401
        except Exception as e:
            return APIResponse().dump(dict(message=f'Logout unsuccessful {str(e)}')), 400


api.add_resource(Logout, '/logout')
docs.register(Logout)


# 2a
class Add_Vendor(MethodResource, Resource):
    @doc(description='Add Vendor API', tags=['Add Vendor API'])
    @use_kwargs(Add_VendorRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            cust_id, restaurant_name = kwargs['cust_id'], kwargs['restaurant_name']
            if not cust_id or not restaurant_name:
                return APIResponse().dump(dict(message='Incomplete vendor information provided')), 400
            customer = Customer.query.filter_by(
                cust_id=cust_id, level=0).first()
            if customer:
                customer.level = 1
                vendor = Vendor(
                    vendor_id=generateId(),
                    cust_id=cust_id,
                    restaurant_name=restaurant_name
                )
                db.session.add(vendor)
                db.session.commit()
                return APIResponse().dump(dict(message='New vendor added')), 201
            return APIResponse().dump(dict(message='Not allowed to add vendor / Already a vendor')), 401
        except Exception as e:
            return APIResponse().dump(dict(message=f'Unable to add vendor {str(e)}')), 400


api.add_resource(Add_Vendor, '/add_vendor')
docs.register(Add_Vendor)


# 2b
class Get_All_Vendors(MethodResource, Resource):
    @doc(description='Get All Vendors API', tags=['Get All Vendors API'])
    @marshal_with(VendorsResponse)
    def get(self):
        try:
            if session['cust_id']:
                vendors = Vendor.query.all()
                _vendors = []
                for vendor in vendors:
                    _vendor = dict()
                    _vendor['vendor_id'] = vendor.vendor_id
                    _vendor['restaurant_name'] = vendor.restaurant_name
                    foodItems = Food.query.filter_by(
                        vendor_id=vendor.vendor_id)
                    _foodItems = []
                    for foodItem in foodItems:
                        _foodItem = dict()
                        _foodItem['food_id'] = foodItem.food_id
                        _foodItem['dish_name'] = foodItem.dish_name
                        _foodItem['calories_per_gm'] = foodItem.calories_per_gm
                        _foodItem['available_quantity'] = foodItem.available_quantity
                        _foodItem['unit_price'] = foodItem.unit_price
                        _foodItems.append(_foodItem)
                    _vendor['food_items'] = _foodItems
                    _vendors.append(_vendor)
                return VendorsResponse().dump(dict(message='Vendors fetched successfully', vendors=_vendors)), 200
            return VendorsResponse().dump(dict(message='Not logged in', vendors=[])), 401
        except Exception as e:
            return VendorsResponse().dump(dict(message=f'Unable to fetch vendors {str(e)}', vendors=[])), 400


api.add_resource(Get_All_Vendors, '/get_all_vendors')
docs.register(Get_All_Vendors)


# 3a
class Add_Food_Item(MethodResource, Resource):
    @doc(description='Add Food Item API', tags=['Add Food Item API'])
    @use_kwargs(Add_Food_ItemRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            vendor_id, dish_name, calories_per_gm, available_quantity, unit_price = kwargs['vendor_id'], kwargs[
                'dish_name'], kwargs['calories_per_gm'], kwargs['available_quantity'], kwargs['unit_price']
            if not vendor_id or not dish_name or not calories_per_gm or not available_quantity or not unit_price:
                return APIResponse().dump(dict(message='Incomplete food item information provided')), 400
            if session['cust_id']:
                vendor = Vendor.query.filter_by(vendor_id=vendor_id).first()
                if vendor:
                    food_item_already_listed = Food.query.filter_by(vendor_id=vendor_id,dish_name=dish_name,unit_price=unit_price,calories_per_gm=calories_per_gm).first()
                    if food_item_already_listed:
                        food_item_already_listed.available_quantity += available_quantity
                        db.session.commit()
                        return APIResponse().dump(dict(message=f'Food item already exists, the stock is increased by {available_quantity} and the updated stock is {food_item_already_listed.available_quantity}')), 201
                    foodItem = Food(
                        food_id=generateId(),
                        vendor_id=vendor_id,
                        dish_name=dish_name,
                        calories_per_gm=calories_per_gm,
                        available_quantity=available_quantity,
                        unit_price=unit_price
                    )
                    db.session.add(foodItem)
                    db.session.commit()
                    return APIResponse().dump(dict(message='New food item added')), 201
                else:
                    return APIResponse().dump(dict(message='Only logged in vendors can add new food items')), 403
            else:
                return APIResponse().dump(dict(message='Not logged in')), 401
        except Exception as e:
            return APIResponse().dump(dict(message=f'Unable to add food item {str(e)}')), 400


api.add_resource(Add_Food_Item, '/add_food_item')
docs.register(Add_Food_Item)


# cart api
class Add_To_Cart(MethodResource, Resource):
    @doc(description='Add To Cart API', tags=['Add To Cart API'])
    @use_kwargs(Add_To_CartRequest, location=('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            food_id, quantity = kwargs['food_id'], kwargs['quantity']
            if not food_id or not quantity:
                return APIResponse().dump(dict(message='Incomplete cart item information provided')), 400
            food_item = Food.query.filter_by(food_id=food_id).first()
            if session['cust_id'] and food_item:
                customer = Customer.query.filter_by(
                    cust_id=session['cust_id'], level=0).first()
                if not customer:
                    return APIResponse().dump(dict(message='Not allowed to add to cart, only customers are allowed')), 403
                if quantity > food_item.available_quantity:
                    return APIResponse().dump(dict(message='Quantity unavailable')), 400
                alreadyInCart = Cart.query.filter_by(cust_id=session['cust_id'], food_id=food_id).first()
                if alreadyInCart:
                    if alreadyInCart.quantity + quantity > food_item.available_quantity:
                        return APIResponse().dump(dict(message=f'quantity exceeds stock {food_item.available_quantity - alreadyInCart.quantity} remaining')), 400
                    alreadyInCart.quantity += quantity
                else:
                    cart_item = Cart(
                    cart_item_id=generateId(),
                    food_id=food_id,
                    cust_id=session['cust_id'],
                    quantity=quantity,
                    amount=quantity * food_item.unit_price
                )
                    db.session.add(cart_item)
                db.session.commit()
                return APIResponse().dump(dict(message='Item added to cart')), 201
            return APIResponse().dump(dict(message='Customer not logged in')), 401
        except Exception as e:
            return APIResponse().dump(dict(message=f'Unable to add to cart {str(e)}')), 400


api.add_resource(Add_To_Cart, '/add_to_cart')
docs.register(Add_To_Cart)


# 3b
class Place_Order(MethodResource, Resource):
    @doc(description='Place Order API', tags=['Place Order API'])
    @marshal_with(APIResponse)
    def put(self):
        try:
            if session['cust_id']:
                cart_items = Cart.query.filter_by(cust_id=session['cust_id'])
                # print(cart_items)
                if cart_items.count() < 1:
                    return APIResponse().dump(dict(message='Cart is empty')), 400
                total_amount = 0
                for cart_item in cart_items:
                    food_item = Food.query.filter_by(
                        food_id=cart_item.food_id).first()
                    total_amount += cart_item.amount
                    food_item.available_quantity -= cart_item.quantity
                    if food_item.available_quantity < 0:
                        return APIResponse().dump(dict(message='ordered items are out of stock')), 400

                # cart_foods = Cart.query.filter_by(cust_id=session['cust_id'],food_id=cart_items.food_id)
                # for cart_food in cart_foods:
                    # food_item.available_quantity -= cart_food.quantity
                order = Orders(
                    order_id=generateId(),
                    cust_id=session['cust_id'],
                    total_amount=total_amount,
                    date=datetime.now().strftime('%Y-%m-%d')
                )
                db.session.add(order)
                db.session.commit()
                for cart_item in cart_items:
                    order_item = OrderItems(
                        item_id=generateId(),
                        order_id=order.order_id,
                        food_id=cart_item.food_id,
                        quantity=cart_item.quantity,
                        amount=cart_item.amount
                    )
                    db.session.add(order_item)
                    db.session.commit()
                Cart.query.filter_by(cust_id=session['cust_id']).delete()
                db.session.commit()
                return APIResponse().dump(dict(message='New order placed')), 201
            return APIResponse().dump(dict(message='Not logged in')), 401
        except Exception as e:
            return APIResponse().dump(dict(message=f'Unable to place order {str(e)}')), 400


api.add_resource(Place_Order, '/place_order')
docs.register(Place_Order)


# 3c
class Get_All_Orders_By_Customer(MethodResource, Resource):
    @doc(description='Get All Orders By Customers API', tags=['Get All Orders By Customers API'])
    @marshal_with(OrdersResponse)
    def get(self, **kwargs):
        try:
            if session['cust_id']:
                orders = getOrders(Orders.query.filter_by(
                    cust_id=session['cust_id']))
                return OrdersResponse().dump(dict(message='Orders fetched successfully', orders=orders)), 200
            return OrdersResponse().dump(dict(message='Not logged in', orders=[])), 401
        except Exception as e:
            return OrdersResponse().dump(dict(message=f'Unable to fetch orders {str(e)}', orders=[])), 400


api.add_resource(Get_All_Orders_By_Customer, '/get_all_orders_by_customer')
docs.register(Get_All_Orders_By_Customer)


# 3d
class Get_All_Orders(MethodResource, Resource):
    @doc(description='Get All Orders API', tags=['Get All Orders API'])
    @marshal_with(OrdersResponse)
    def get(self):
        try:
            if session['cust_id']:
                admin = Customer.query.filter_by(
                    cust_id=session['cust_id'], level=2).first()
                if not admin:
                    return OrdersResponse().dump(dict(message='Only admins can fetch all orders', orders=[])), 403
                orders = getOrders(Orders.query.all())
                return OrdersResponse().dump(dict(message='Orders fetched successfully', orders=orders)), 200
            return OrdersResponse().dump(dict(message='Not logged in', orders=[])), 401
        except Exception as e:
            return OrdersResponse().dump(dict(message=f'Unable to fetch orders {str(e)}', orders=[])), 400


api.add_resource(Get_All_Orders, '/get_all_orders')
docs.register(Get_All_Orders)
