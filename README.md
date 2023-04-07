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
python binance_data_exporter.py
````

## Dependencies

The script requires the following dependencies:

- requests
- colorama
- datetime
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