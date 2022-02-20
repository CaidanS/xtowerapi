from flask_restful import Api
import os
from endpoints import Accounts, Withdraw, Deposit, Exchange, Balances
from models import app, db

api = Api(app)

thisdir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(thisdir, 'xtowerdb.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api.add_resource(Accounts, '/accounts')
api.add_resource(Deposit, '/deposit')
api.add_resource(Withdraw, '/withdraw')
api.add_resource(Exchange, '/exchange')

if __name__ == '__main__':
    # db.create_all() # Uncomment if database is deleted somehow
    app.run(debug=True)