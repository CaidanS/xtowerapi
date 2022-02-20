from flask_restful import Api
import os
from endpoints import Accounts, Withdraw, Deposit, Exchange, Balances
from models import app, db

api = Api(app)

thisdir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(thisdir, 'xtowerdb.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api.add_resource(Accounts, '/accounts')