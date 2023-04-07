from datetime import datetime
import requests
from colorama import Fore, Style

import json
import sys
import os

# ############################################################################# #
#################################################################################
# ----------------------------------------------------------------------------- #
#                              CONFIGURATION                                    #   
# ----------------------------------------------------------------------------- #                               

interval = '4h'     # Specify the interval, for example 1 day
symbol = 'BTCUSDT'  # Specify the symbol, for example BTCUSDT
limit = 1000        # Specify the limit of the data per request

url = 'https://api3.binance.com'    # The base URL of the API
endpoint = '/api/v3/klines'         # The endpoint of the API

# The key of the parameters of the request 
START_TIME = 'startTime'
INTERVAL = 'interval'
SYMBOL = 'symbol'
LIMIT = 'limit'

# configure the parameters of the request
params = {
    SYMBOL: symbol,
    INTERVAL: interval,
    LIMIT: limit,
    # START_TIME: 0, # 0 means the first data point available
}

OUTPUT_FOLDER = './data' # The folder where the data will be exported
#################################################################################
# ############################################################################# #


def export_data(data: list) -> None:
    """
    Export the data to a JSON file
    param data: The data to export
    return: None
    """
    
    start_date = data[0]['date'].split(' ')[0]
    end_date = data[-1]['date'].split(' ')[0]
    
    filename = f'{params[SYMBOL]}_{start_date}_to_{end_date}_{params[INTERVAL]}.json'
    if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)
        

def timestamp_to_date_format(timestamp: int, format='%Y-%m-%d') -> str:
    """
    Convert the timestamp to a date
    param timestamp: The timestamp to convert
    param format: The format of the date
    return: The date in the specified format
    """    
    
    return datetime.fromtimestamp(timestamp / 1000).strftime(format)


def extract_data(response: list) -> tuple:
    """
    Extract the data from the API response
    param response: The response of the API
    return: The date and the values
    """
    
    date = timestamp_to_date_format(response[0], '%Y-%m-%d %H:%M:%S')
    values = {
        'open': response[1],
        'high': response[2],
        'low': response[3],
        'close': response[4],
        'volume': response[5],
        'close_time': timestamp_to_date_format(response[6], '%Y-%m-%d %H:%M:%S'),
        'quote_asset_volume': response[7],
        'number_of_trades': response[8],
        'taker_buy_base_asset_volume': response[9], 
        'taker_buy_quote_asset_volume': response[10],
    }
    
    return date, values

def request_data() -> list:
    """
    Request the data from the API
    param: None
    return: The retrieved data from the API
    """
    
    print(f"START: Requesting data from {Style.BRIGHT}{url}{Style.NORMAL}...")

    data = []
    while True:
        response = requests.get(url+endpoint, params=params)
        if response.status_code == 200:
            klines = json.loads(response.text)
            
            if len(klines) == 0: break
            for kline in klines:
                date, values = extract_data(kline)
                data.append({'date': date, 'values': values})
                
            params[START_TIME] = klines[-1][0] + 1 # define the start time for the next request
            print(f" - Requesting data from {Style.BRIGHT}{timestamp_to_date_format(params[START_TIME], '%Y-%m-%d %H:%M:%S')}{Style.NORMAL}")
        else:
            print(f"Error {response.status_code}: {response.reason}")
            break
            
    return data


# ------------------------------------------------------------------------------ #
#                               * MAIN *                                         #
# ------------------------------------------------------------------------------ #

def main(argv):
    data = request_data()
    print("=========================================")
    print(f" {Fore.GREEN}Retrieved {Style.BRIGHT}{len(data)}{Style.NORMAL} data points{Fore.RESET}")
    print("=========================================")

    export_data(data)

if __name__ == '__main__':
    main(sys.argv[1:])