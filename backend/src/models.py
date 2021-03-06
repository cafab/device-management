"""
models.py
- defines all models and creates the SQLAlchemy instance
"""
from flask_sqlalchemy import SQLAlchemy
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
    os = db.Column(db.String(255), nullable=False)
    os_install_date = db.Column(db.Date(), nullable=False)
    computer_model = db.Column(db.String(255), nullable=False)
    cpu = db.Column(db.String(255), nullable=False)
    memory = db.Column(db.String(255), nullable=False)
    hard_disk = db.Column(db.String(255), nullable=False)    

# backref creates a virtual column in the PurchaseDetails table
# uselist=False ensures a One-to-One relation between the computer and PurchaseDetails table
class PurchaseDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(255))
    price = db.Column(db.Numeric(10,2))
    purchase_date = db.Column(db.Date())
    notes = db.Column(db.Text)
    computer_sn = db.Column(db.String(255), db.ForeignKey('computer.serial_number'), nullable=False)
    computer = db.relationship('Computer', backref='purchase_details', uselist=False)

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_account = db.Column(db.String(255), nullable=False)
    previous_account = db.Column(db.String(255))
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    computer_sn = db.Column(db.String(255), db.ForeignKey('computer.serial_number'), nullable=False)
    computer = db.relationship('Computer', backref='accounts', uselist=False)
