from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow)

    # Renamed backrefs to avoid conflict with model name
    cart_items = db.relationship('Cart', backref=db.backref('customer', lazy=True))
    orders = db.relationship('Order', backref=db.backref('customer', lazy=True))

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password=password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password=password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def __str__(self):
        return f'Customer: {self.id}'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    previous_price = db.Column(db.Float, nullable=False)
    product_picture = db.Column(db.String(100), nullable=False)
    flash_sale = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Renamed backrefs to avoid conflict with model name
    carts = db.relationship('Cart', backref=db.backref('product_in_cart', lazy=True))
    orders = db.relationship('Order', backref=db.backref('product_in_order', lazy=True))

    def __str__(self):
        return f'Product: {self.product_name}'


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    employee_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.Date, nullable=False, default=datetime.utcnow)



    def __str__(self):
        return f'Employee: {self.employee_name}'


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return f'Cart {self.id}'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __str__(self):
        return f'Order {self.id}'
