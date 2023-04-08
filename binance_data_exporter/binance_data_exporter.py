#!/usr/bin/env python3

from colorama import Fore, Style
from tabulate import tabulate
from datetime import datetime
import requests

import getopt
import time
import json
import sys
import os

# ############################################################################# #
#################################################################################
# ----------------------------------------------------------------------------- #
#                              CONFIGURATION                                    #   
# ----------------------------------------------------------------------------- #                               

interval = '1d'                 # Specify the interval, for example 1 day
symbol = 'BTCUSDT'              # Specify the symbol, for example BTCUSDT
limit = 500                     # Specify the limit of the data per request
start_time = None               # Specify the start time of the data, if None, the first data point available will be used
end_time = int(time.time() * 1000)   # Specify the end time of the data

url = 'https://api3.binance.com'    # The base URL of the API
endpoint = '/api/v3/klines'         # The endpoint of the API

# The key of the parameters of the request 
START_TIME = 'startTime'
END_TIME = 'endTime'
INTERVAL = 'interval'
SYMBOL = 'symbol'
LIMIT = 'limit'

# configure the parameters of the request
params = {
    SYMBOL: symbol,
    INTERVAL: interval,
    LIMIT: limit,
    END_TIME: end_time
}

OUTPUT_FOLDER = './data'    # The default folder where the data will be exported

#################################################################################
# ############################################################################# #

# ----------------------------------------------------------------------------- #
#                            * USAGE FUNCTION *                                 #
# ----------------------------------------------------------------------------- #

def usage(program_name: str) -> None:
    """
    Print the usage of the program
    param program_name: The name of the program
    return: None
    """
    
    headers = [f"{Style.BRIGHT}Option{Style.NORMAL}", f"{Style.BRIGHT}Description{Style.NORMAL}", 
               f"{Style.BRIGHT}Possible Values{Style.NORMAL}", f"{Style.BRIGHT}Default Values{Style.NORMAL}"]
    rows = [
        ["-i, --interval", "The interval of the data", "1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M", f"{interval}"],
        ["-p, --pair", "The pair of coin (refer to the binance symbol list)", "BTCUSDT, ETHUSDT, etc.", f"{symbol}"],
        ["-l, --limit", "The limit of the data per request", "1, 2, ..., 1000 (Should be integer)", f"{limit}"],
        ["-s, --start-time", "The start time of the data", "YYYY_MM_DD", f"{timestamp_to_date_format(start_time, '%Y_%m_%d') if start_time else 'None'}"],
        ["-e, --end-time", "The end time of the data", "YYYY_MM_DD", f"{timestamp_to_date_format(end_time, '%Y_%m_%d')}"],
        ["-o, --output-folder", "The folder where the data will be exported", "Path", f"{OUTPUT_FOLDER}"]
    ]
    
    print(f"{Fore.MAGENTA}Usage: {program_name} [OPTIONS]{Style.RESET_ALL}")
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid"), end='\n\n')
    print(f"{Fore.RED}ATTENTION: Make sure to not exceed the number of requests allowed by the API, when configuring the {Style.BRIGHT}`limit`{Style.NORMAL} and {Style.BRIGHT}`interval`{Style.NORMAL} parameters.{Fore.RESET}", end='\n\n')
    print(f"{Fore.YELLOW}NOTE: if you don't specify a start time for your request, it will use the earliest available data for the requested time interval.{Fore.RESET}")
    print(f"Checkout the Binance API documentation for more information: {Fore.CYAN}{Style.BRIGHT}https://binance-docs.github.io/apidocs/spot/en/{Style.NORMAL}{Fore.RESET}", end='\n\n')

    print(f"{Style.BRIGHT}Example:{Style.NORMAL} {Fore.MAGENTA}{program_name}{Fore.RESET}{Style.BRIGHT} -l 10 -i 1h -p ETHUSDT -s 2018_01_15 -e 2018_01_16 -o ./data/eth_usdt/{Style.NORMAL}")
    exit(0)


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
    
    if os.path.exists(filepath):
        response = input(f"{Fore.YELLOW}WARNING: The file {Fore.BLUE}{Style.BRIGHT}{filepath}{Style.NORMAL}{Fore.YELLOW} already exists. Do you want to overwrite it? [y/n]{Fore.RESET} ")
        if response.lower() != 'y': return
        
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)
    
    print(f"\n{Fore.GREEN}> END:{Fore.RESET} Data exported to {Fore.BLUE}{Style.BRIGHT}{filepath}{Style.NORMAL}{Fore.RESET}")
        

def timestamp_to_date_format(timestamp: int, format='%Y-%m-%d') -> str:
    """
    Convert the timestamp to a date
    param timestamp: The timestamp to convert
    param format: The format of the date
    return: The date in the specified format
    """    
    
    return datetime.fromtimestamp(timestamp / 1000).strftime(format)


def extract_data(response: list) -> dict:
    """
    Extract the data from the API response
    param response: The response of the API
    return: The extracted data as a dictionary
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
    
    return { 'date': date, **values }

def request_data() -> list:
    """
    Request the data from the API
    param: None
    return: The retrieved data from the API
    """
    
    print(f"\n{Fore.GREEN}> START:{Fore.RESET} Requesting data from: {Fore.BLUE}{Style.BRIGHT}{url+endpoint}{Style.NORMAL}{Fore.RESET}")

    data = []
    while True:
        response = requests.get(url+endpoint, params=params)
        if response.status_code == 200:
            klines = json.loads(response.text)
            
            if len(klines) == 0: break
            for kline in klines:
                data.append(extract_data(kline))
                
            params[START_TIME] = klines[-1][0] + 1 # define the start time for the next request
            print(f" - Requesting data from {Style.BRIGHT}{timestamp_to_date_format(params[START_TIME], '%Y-%m-%d %H:%M:%S')}{Style.NORMAL}")
        else:
            print(f"Error {response.status_code}: {response.reason}")
            break
            
    return data


def parse_command_line_args(argv: list) -> None:
    """
    Parse the command line arguments and update the default values if necessary
    param argv: The command line arguments
    return: None
    """
    
    program_name = argv[0]
    argv = argv[1:]
    try:
        opts, _ = getopt.getopt(argv,"hi:p:l:s:e:o:",["interval=","pair=","limit=","start_time=","end_time=","output_folder="])
    except getopt.GetoptError:
        usage(program_name)

    # We rewrite the default values with the command line arguments
    global OUTPUT_FOLDER
    global params
                
    for opt, arg in opts:
        if opt == '-h':
            usage(program_name)
        elif opt in ("-i", "--interval"):
            params[INTERVAL] = arg
        elif opt in ("-p", "--pair"):
            params[SYMBOL] = arg
        elif opt in ("-l", "--limit"):
            params[LIMIT] = int(arg)
        elif opt in ("-s", "--start_time"):
            params[START_TIME] = int(datetime.strptime(arg, '%Y_%m_%d').timestamp() * 1000)
        elif opt in ("-e", "--end_time"):
            params[END_TIME] = int(datetime.strptime(arg, '%Y_%m_%d').timestamp() * 1000)
        elif opt in ("-o", "--output_folder"):
            OUTPUT_FOLDER = arg


# ------------------------------------------------------------------------------ #
#                               * MAIN *                                         #
# ------------------------------------------------------------------------------ #
def main(argv=sys.argv) -> None:
    """
    Main function
    param argv: The command line arguments
    """
    
    if argv is not None: parse_command_line_args(argv)
    data = request_data()
    
    if len(data) == 0:
        print(f"{Fore.RED}No data Found{Fore.RESET}")
        exit(0)

    print("=========================================")
    print(f" {Fore.GREEN}Retrieved {Style.BRIGHT}{len(data)}{Style.NORMAL} data points{Fore.RESET}")
    print("=========================================")

    export_data(data)

if __name__ == '__main__':
    main(sys.argv)