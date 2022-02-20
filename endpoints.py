from flask_restful import Resource, reqparse
from flask import jsonify
from datetime import datetime
from models import db, ma, Account, BalanceHistory

class Accounts(Resource):
    '''
    Resource to be called by the appropriate api request
    
    Accepts POST request to create a new user with a zero balance with a specified username
    '''
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('username', required=True)
        args = parser.parse_args()

        new_account = Account(args['username'])

        db.session.add(new_account)
        db.session.commit()

        accounts_list = jsonify(account_schema.dump(Account.query.all()))
        return accounts_list
