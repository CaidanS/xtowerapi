from flask_restful import Resource, reqparse
from flask import jsonify
from datetime import datetime
from models import db, ma, Account, BalanceHistory

# These exchange rates are just hardcoded from the current rates
# but would be fairly straightforward to pull rates from some api whenever a user makes an exchange
exchange_rates = {
    "btc": {
        "eth": 14.53,
        "usd": 40057.90
    }, 
    "eth": {
        "btc": 0.06882312,
        "usd": 2757.37
    },
    "usd": {
        "btc": 0.00002496,
        "eth": 0.5,
    }
}


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


class Withdraw(Resource):
    '''
    Resource to be called by the appropriate api request
    
    Accepts PUT request to withdraw assets of given type from a user's account
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
            
            if new_balance_temp[args['asset_type']] >= float(args['asset_amount']):
                new_balance_temp[args['asset_type']] -= float(args['asset_amount'])

                new_balance_record = BalanceHistory(args['username'], new_balance_temp['btc'], new_balance_temp['usd'], new_balance_temp['eth'],  datetime.now())
                
                db.session.add(new_balance_record)
                db.session.commit()

                return {'balances': new_balance_temp}, 200

            else:
                return {'message': 'insufficent funds.', 'balances': new_balance_temp}, 401
        
        else:
            return {'message': f"username '{args['username']}' not found"}, 404


class Exchange(Resource):
    '''
    Resource to be called by the appropriate api request
    
    Accepts PUT request to exchange assets between types and users.
    '''
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username_from', required=True)
        parser.add_argument('username_to', required=True)
        parser.add_argument('asset_type_from', required=True)
        parser.add_argument('asset_type_to', required=True)
        parser.add_argument('asset_amount_from', required=True)

        args = parser.parse_args()

        # check if the it's an internal exchange
        if Account.query.filter_by(username = args['username_from']).first() is not None:
            if args['username_from'] == args['username_to']:
                old_balance = BalanceHistory.query.filter_by(assoc_acct_id=args['username_from']).order_by(BalanceHistory.id.desc()).first()
                
                new_balance_temp = {
                        'btc': old_balance.btc_balance,
                        'usd': old_balance.usd_balance,
                        'eth': old_balance.eth_balance
                }
                
                if new_balance_temp[args['asset_type_from']] >= float(args['asset_amount_from']):
                    new_balance_temp[args['asset_type_from']] -= float(args['asset_amount_from'])

                    converted_amount = exchange_rates[args['asset_type_from']][args['asset_type_to']] * float(args['asset_amount_from'])
                    new_balance_temp[args['asset_type_to']] += converted_amount

                    new_balance_record = BalanceHistory(args['username_from'], new_balance_temp['btc'], new_balance_temp['usd'], new_balance_temp['eth'], datetime.now())
                    db.session.add(new_balance_record)
                    db.session.commit()

                    return {'balances': new_balance_temp}, 200

                else:
                    return {'message': 'insufficent funds.', 'balances': new_balance_temp}, 401
            # check if user exits in current userbase
            elif Account.query.filter_by(username = args['username_to']).first() is not None:
                    old_balance_from = BalanceHistory.query.filter_by(assoc_acct_id=args['username_from']).order_by(BalanceHistory.id.desc()).first()
                    old_balance_to = BalanceHistory.query.filter_by(assoc_acct_id=args['username_to']).order_by(BalanceHistory.id.desc()).first()
                    
                    new_balance_temp_from = {
                        'btc': old_balance_from.btc_balance,
                        'usd': old_balance_from.usd_balance,
                        'eth': old_balance_from.eth_balance
                    }
                    
                    new_balance_temp_to = {
                        'btc': old_balance_to.btc_balance,
                        'usd': old_balance_to.usd_balance,
                        'eth': old_balance_to.eth_balance
                    }

                    if new_balance_temp_from[args['asset_type_from']] >= float(args['asset_amount_from']):
                        new_balance_temp_from[args['asset_type_from']] -= float(args['asset_amount_from'])

                        converted_amount = exchange_rates[args['asset_type_from']][args['asset_type_to']] * float(args['asset_amount_from'])
                        new_balance_temp_to[args['asset_type_to']] += float(converted_amount)

                        new_balance_record_from = BalanceHistory(args['username_from'], new_balance_temp_from['btc'], new_balance_temp_from['usd'], new_balance_temp_from['eth'], datetime.now())
                        new_balance_record_to = BalanceHistory(args['username_to'], new_balance_temp_to['btc'], new_balance_temp_to['usd'], new_balance_temp_to['eth'],  datetime.now())
                        db.session.add(new_balance_record_from)
                        db.session.add(new_balance_record_to)
                        db.session.commit()

                        return {'new_balance_from': new_balance_temp_from, 'new_balance_to': new_balance_temp_to}, 200
                    else:
                        return {'message': 'insufficent funds.'}, 401
            else:
                 return {'message': f"recipient username '{args['username_to']}' not found"}, 404
        else:
            return {'message': f"sender username '{args['username_from']}' not found"}, 404
