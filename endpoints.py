from flask_restful import Resource, reqparse
from flask import jsonify
from datetime import datetime
from models import db, ma, Account, BalanceHistory

# Schemas for returning data to the requester (not very familar with Marshmallow, but this seems to work!)
class AccountSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')

class BalanceHistorySchema(ma.Schema):
    class Meta:
        fields = ('assoc_acct_id', 'transaction_date', 'btc_balance', 'usd_balance','eth_balance')

account_schema = AccountSchema(many=True)

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

