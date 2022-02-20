# Crosstower Programming Project

Simple API backend to handle account balance management.

## Tools Used:
* Python
* SQLite
* SQLAlchemy
* Flask

## Installation
```
$ git clone https://github.com/CaidanS/xtowerapi.git
```
Virtual environment setup up to you but I did it as follows
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
## Running the project
```
$ python3 main.py
```

## Testing project
There are several endpoints exposed at http://127.0.0.1:5000/. Requests should be sent with url encoding. 

### POST `/accounts`
Perameters:
* username: username to create (string, required)

Wget example: 

``` 
wget -O - --post-data 'username=alice' http://127.0.0.1:5000/accounts
```

### PUT `/deposit`
Perameters:
* username: username to deposit to (string, required)
* asset_type: asset type to deposit (possible values: "eth", "btc", "usd", required)
* asset_amount: amount to deposit (float, required)

Wget example: 

```
wget -O - --method=PUT --body-data 'username=alice&asset_type=eth&asset_amount=10' http://127.0.0.1:5000/deposit
```

### PUT `/withdraw`
Perameters:
* username: username to withdraw from (string, required)
* asset_type: asset type to withdraw (possible values: "eth", "btc", "usd", required)
* asset_amount: amount to withdraw (float, required)

Wget example: 

``` 
wget -O - --method=PUT --body-data 'username=alice&asset_type=eth&asset_amount=5' http://127.0.0.1:5000/withdraw
```

### PUT `/exchange`
Perameters: 
* username_from: username to withdraw from (string, required)
* username_to: username to deposit to (string, required)
* asset_type_from: asset type to withdraw (possible values: "eth", "btc", "usd", required)
* asset_type_to: asset type to deposit (possible values: "eth", "btc", "usd", required)
* asset_amount_from: amount to withdraw (float, required)

Wget example: 

```
wget -O - --method=PUT --body-data 'username_from=alice&username_to=bob&asset_type_from=eth&asset_type_to=btc&asset_amount_from=10' http://127.0.0.1:5000/exchange
```

### GET `/balances`
Perameters (must be passed as query string parameters)
* username (string, required)
* asset_types: asset types to retieve (tuple including one or more of "eth_balance", "btc_balance", and "usd_balance", optional, defaults to all)
* start_time: earliest balance history item to include (string of datetime, optional, defaults to all transactions)
* end_time: latest balance history item to include (string of datetime, optional, defaults to all transactions)

Wget example: 

```
wget -O - 'http://127.0.0.1:5000/balances?username=alice&asset_types=("eth_balance",)&start_time=2022-02-19 14:43:46.103556&end_time=2022-02-19 14:45:56.287979'
```
