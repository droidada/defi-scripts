from requests import Session
import json
import pandas as pd

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '<API_KEY>'
}

session = Session()
session.headers.update(headers)

def get_response(symbol):
    parameters = {
        'symbol': symbol
    }
    response = session.get(url, params = parameters)
    return json.loads(response.text)

def clean_response(symbol):
    data = get_response(symbol)
    new_dict = data['data'][symbol][0]['quote']['USD']
    new_dict['symbol'] = symbol
    df = pd.DataFrame(new_dict, index=[0])
    df.set_index('symbol', inplace=True)
    return df

def get_response_multiple(symbols):
    parameters = {
        'symbol': ','.join(symbols)
    }
    response = session.get(url, params=parameters)
    return json.loads(response.text)

def clean_response_multiple(symbols):
    data = get_response_multiple(symbols)
    df = pd.DataFrame(
        [{'symbol': symbol, **data['data'][symbol][0]['quote']['USD']} for symbol in symbols]
    ).set_index('symbol')
    return df



print(clean_response('BTC'))
print(clean_response_multiple(['BTC', 'ETH', 'SOL']))