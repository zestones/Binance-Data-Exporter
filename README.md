# Binance API Data Retrieval

This Python script allows you to retrieve historical data from Binance API and export it to a JSON file. The data can be retrieved for any specified symbol (e.g. BTCUSDT) and interval (e.g. 1m, 1h, 1d) for a given period of time.

## Configuration

Before running the script, you need to configure the following parameters in the script:

- `interval`: The interval of the data, e.g., 1 day, 4 hours, etc.
- `symbol`: The symbol of the cryptocurrency, e.g., BTCUSDT, ETHUSDT, etc.
- `limit`: The number of data points per request.
- `OUTPUT_FOLDER`: The folder where the data will be exported.

## Usage

To run the script, use the following command:

````bash
python binance_data_exporter.py [OPTIONS]
````

Bellow the list of available options you can use to customize the request to the Binance API:

| **Option**          | **Description**                   | **Possible Values**               | **Default Value** 	|
|-------------------	|----------------------------------	|---------------------------------	|:-----------------:	|
| `-i`,<br> `--interval`      	| The interval of the data                                                 	| 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M 	|        `1d`       	|
| `-p`,<br> `--pair`          	| The pair of coin (refer to the binance symbol list)                      	| BTCUSDT, ETHUSDT, etc                                         	|     `BTCUSDT`     	|
| `-l`,<br> `--limit`         	| The limit of the data per request \| 1, 2, ..., 1000 (Should be integer) 	| 1, 2, ..., 1000 (Should be integer)                           	|       `500`       	|
| `-s`,<br> `--start-time`    	| The start time of the data                                               	| YYYY_MM_DD                                                    	|        None       	|
| `-e`,<br> `--end-time`      	| The end time of the data                                                 	| YYYY_MM_DD                                                    	|      `TODAY`      	|
| `-o`,<br> `--output-folder` 	| The folder where the data will be exported                               	| Path                                                          	|      `./data`     	|


> **NOTE** 
> 
> - If you don't specify a start time for your request, it will use the earliest available data for the requested time interval.
> - If the end-time is not specified the date of the day will be choosed by default.
### Examples

To retrieve data for ETHUSDT from 2018-01-15 to 2018-01-16 with an interval of 1 hour, a limit of 10, and export the data to `./data/eth_usdt/`, use the following command:

````bash
python binance_data_exporter.py -l 10 -i 1h -p ETHUSDT -s 2018_01_15 -e 2018_01_16 -o ./data/eth_usdt/
````

You can customize the parameters to retrieve data as you wish.


## Dependencies

The script requires the following dependencies:

- requests
- colorama
- datetime
- tabulate
- json

You can install the dependencies using the following command:

````bash
pip install -r requirements.txt
````	


## Output

The script exports the retrieved data as a JSON file in the `OUTPUT_FOLDER` specified in the configuration. The filename of the JSON file is in the following format: **symbol**\_**start-date**\_to\_**end-date**\_**interval**.json

where `start_date` and `end_date` are the start and end dates of the data retrieved, respectively and ``interval`` is the interval between each data point.

## API Limits and Maximum Number of Requests

Please note that Binance API has certain limits on the number of requests that can be made within a specific time frame. 

It is important to be mindful of these limits when making requests to avoid being disconnected or banned. Make sure to not exceed the number of requests allowed by the API, when configuring the `limit` and `interval` parameters in the script.

## Binance API Documentation
For more information on the Binance API, you can refer to the official documentation at:

https://binance-docs.github.io/apidocs/spot/en/
