## You will need to run the following command before running the script for the first time:
## pip install py3cw

from py3cw.request import Py3CW

API_key = ''
SECRET_key = ''
account = '' # This can be found in the URL when you go to the page for the exchange on 3commas.


p3cw = Py3CW(
    key=API_key, 
    secret=SECRET_key,
    request_options={
        'request_timeout': 50,
        'nr_of_retries': 1,
        'retry_status_codes': [502]
    }
)

error, data = p3cw.request(
    entity='deals',
    action='',
    payload={
        "limit": 1000,
        "scope": 'active',
        "account_id": account,
    }
)

used_capital_by_coin = {}

used_capital_by_bot = {}

def get_used_capital(deal):
    bo = float(deal['base_order_volume'])
    so = float(deal['safety_order_volume'])
    mart_coeff = float(deal['martingale_volume_coefficient'])
    comp_so = int(deal['completed_safety_orders_count'])
    active_so = int(deal['current_active_safety_orders_count'])

    total = (bo + so) * mart_coeff ** ((comp_so - 1) + active_so)

    return total
    
for deal in data:
    amount = get_used_capital(deal)
    coin = deal['from_currency']
    bot = deal['bot_name']
    
    if coin in used_capital_by_coin:
        used_capital_by_coin[coin] += amount
    else:
        used_capital_by_coin[coin] = amount
    
    if bot in used_capital_by_bot:
        used_capital_by_bot[bot] += amount
    else:
        used_capital_by_bot[bot] = amount

print('=================================\n')

print('Capital by Coin')
print('---------------\n')
for coin in used_capital_by_coin:
    print(coin + ': ' + str(used_capital_by_coin[coin]))

print('-------------------------------------\n')

print('Capital by Bot')
print('--------------\n')
for bot in used_capital_by_bot:
    print(bot + ': ' + str(used_capital_by_bot[bot]))
    
print('-------------------------------------\n')
