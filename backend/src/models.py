"""
models.py
- defines all models and creates the SQLAlchemy instance
"""
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, validate
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class Computer(db.Model):
    serial_number = db.Column(db.String(255), primary_key=True)
    computer_name = db.Column(db.String(255), unique=True, nullable=False)
    ip_address = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    os = db.Column(db.String(255), nullable=False)
    os_install_date = db.Column(db.DateTime(), nullable=False)
    computerModel = db.Column(db.String(255), nullable=False)
    cpu = db.Column(db.String(255), nullable=False)
    memory = db.Column(db.String(255), nullable=False)
    hardDisk = db.Column(db.String(255), nullable=False)    

# backref creates a virtual column in the PurchaseDetails table
# uselist=False ensures a One-to-One relation between the computer and PurchaseDetails table
class PurchaseDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(255))
    price = db.Column(db.Numeric(10,2))
    purchase_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    computer_sn = db.Column(db.String(255), db.ForeignKey('computer.serial_number'), nullable=False)
    computer = db.relationship('Computer', backref='purchase_details', uselist=False)

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_account = db.Column(db.String(255), nullable=False)
    previous_account = db.Column(db.String(255))
    computer_sn = db.Column(db.String(255), db.ForeignKey('computer.serial_number'), nullable=False)
    computer = db.relationship('Computer', backref='accounts', uselist=False)


# Model schemas
class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()

class PurchaseDetailsSchema(Schema):
    id = fields.Integer()
    supplier = fields.String()
    price = fields.Decimal(as_string=True)
    purchase_date = fields.Date()
    notes = fields.String()

class AccountsSchema(Schema):
    id = fields.Integer()
    current_account = fields.String()
    previous_account = fields.String()

class ComputerSchema(Schema):
    serial_number = fields.String()
    computer_name = fields.String()
    ip_address = fields.String()
    timestamp = fields.DateTime(format="%Y-%m-%d, %H:%M")
    os = fields.String()
    os_install_date = fields.DateTime(format="%Y-%m-%d")
    computerModel = fields.String()
    cpu = fields.String()
    memory = fields.String()
    hardDisk = fields.String()
    purchase_details = fields.Nested(PurchaseDetailsSchema, many=True)
    accounts = fields.Nested(AccountsSchema, many=True)



