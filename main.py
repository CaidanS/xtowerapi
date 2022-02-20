from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime


app = Flask(__name__)

db = SQLAlchemy(app)

class Account(db.Model):
    '''
    Table which records users with an incremented id
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    assoc_BalanceHistory = db.relationship('BalanceHistory', backref='Account')

    def __init__(self, username):
        self.username = username
        
        db.session.add(initial_balance_entry)
        db.session.commit()