from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
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
                
        initial_balance_entry = BalanceHistory(username, 0,0,0, datetime.now())

        db.session.add(initial_balance_entry)
        db.session.commit()

class BalanceHistory(db.Model):
    '''
    Table which records balance entries per username (includes transaction date and all asset balances)
    '''
    id = db.Column(db.Integer, primary_key=True)
    
    assoc_acct_id = db.Column(db.Integer, db.ForeignKey(Account.id))
    transaction_date = db.Column(db.DateTime)

    btc_balance = db.Column(db.Float)
    usd_balance = db.Column(db.Float)
    eth_balance = db.Column(db.Float)

    def __init__(self, assoc_acct_id, btc_balance, usd_balance, eth_balance, transaction_date):
        self.assoc_acct_id = assoc_acct_id
        self.btc_balance = btc_balance
        self.usd_balance = usd_balance
        self.eth_balance = eth_balance
        self.transaction_date = transaction_date
