"""
models.py
- defines all models and creates the SQLAlchemy instance
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)


# backref creates a virtual column in the PurchaseDetails table
# uselist=False ensures a One-to-One relation between the computer and PurchaseDetails table
class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50), unique=True, nullable=False)
    computer_name = db.Column(db.String(50), unique=True, nullable=False)
    purchase_details = db.relationship('PurchaseDetails', backref='computer', uselist=False)


class PurchaseDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    serial_number = db.Column(db.String(20), db.ForeignKey('computer.serial_number'), nullable=False)
