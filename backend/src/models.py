"""
models.py
- defines all models and creates the SQLAlchemy instance
"""
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

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
    

class PurchaseDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    computer_id = db.Column(db.Integer, db.ForeignKey('computer.id'), nullable=False)
    computer = db.relationship('Computer', backref='purchase_details', uselist=False)


# Model schemas
class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()

class PurchaseDetailsSchema(Schema):
    id = fields.Integer()
    supplier = fields.String()
    price = fields.Integer()
    purchase_date = fields.Date()
    notes = fields.String()

class ComputerSchema(Schema):
    id = fields.Integer()
    serial_number = fields.String()
    computer_name = fields.String()
    purchase_details = fields.Nested(PurchaseDetailsSchema, many=True)


