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


class Deposit(Resource):
    '''
    Resource to be called by the appropriate api request
    
    Accepts PUT request to deposit assets of given type into a user's account
    '''
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('asset_type', required=True)
        parser.add_argument('asset_amount', required=True)
        
        args = parser.parse_args()
        
        if Account.query.filter_by(username = args['username']).first() is not None:
            old_balance = BalanceHistory.query.filter_by(assoc_acct_id=args['username']).order_by(BalanceHistory.id.desc()).first()
            new_balance_temp = {
                'btc': old_balance.btc_balance,
                'usd': old_balance.usd_balance,
                'eth': old_balance.eth_balance
            }
            new_balance_temp[args['asset_type']] += float(args['asset_amount'])

            new_balance_record = BalanceHistory(args['username'], new_balance_temp['btc'], new_balance_temp['usd'], new_balance_temp['eth'], datetime.now())
            db.session.add(new_balance_record)
            db.session.commit()

            return {'balances': new_balance_temp}, 200

        else:
            return {'message': f"username '{args['username']}' not found"}, 404

