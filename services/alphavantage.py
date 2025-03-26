import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"

def get_stock_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if "Time Series (Daily)" not in data:
        return {"error": "Invalid symbol // API limit reached"}

    series = data["Time Series (Daily)"]
    last_date = sorted(series.keys())[-1]
    last_data = series[last_date]

    open_price = float(last_data["1. open"])
    close_price = float(last_data["4. close"])
    variation = ((close_price - open_price) / open_price) * 100


    return {
        "symbol": symbol,
        "last_date": last_date,
        "open": last_data["1. open"],
        "high": last_data["2. high"],
        "low": last_data["3. low"],
        "close": last_data["4. close"],
        "volume": last_data["5. volume"],
        "variation": f"{variation:.2f}%"
    }
