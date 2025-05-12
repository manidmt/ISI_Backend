import os
import requests
from dotenv import load_dotenv
from datetime import datetime

from models.stock import Stock, Session

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
BASE_URL = "https://www.alphavantage.co/query"


def stock_to_dict(stock):
    return {
        "symbol": stock.symbol,
        "last_date": stock.date.strftime("%Y-%m-%d"),
        "open": stock.open,
        "high": stock.high,
        "low": stock.low,
        "close": stock.close,
        "volume": stock.volume,
        "variation_pct": stock.variation_pct
    }


from datetime import timedelta

def get_stock_data(symbol):
    session = Session()
    today = datetime.today().date()

    # Buscar datos en los últimos 4 días
    recent_stock = session.query(Stock).filter(
        Stock.symbol == symbol,
        Stock.date >= today - timedelta(days=4)
    ).order_by(Stock.date.desc()).first()

    if recent_stock:
        session.close()
        print(f"Datos encontrados en base de datos para {symbol} del día {recent_stock.date}")
        return stock_to_dict(recent_stock)

    # Si no hay datos recientes, llamar a la API
    print(f"No hay datos recientes en base de datos. Consultando API para {symbol}...")

    apikeys = [os.getenv("ALPHA_VANTAGE_API_KEY"), os.getenv("ALPHA_VANTAGE_API_KEY_2")]
    data = None

    for key in apikeys:
        print(f"Intentando con API key: {key}")
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": key
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "Time Series (Daily)" in data:
            break
        elif "Note" in data or "Error Message" in data:
            print("Error o límite alcanzado con esta clave:")
            print(data.get("Note") or data.get("Error Message"))
            continue

    if "Time Series (Daily)" not in data:
        session.close()
        return {"error": f"No se pudo obtener {symbol}"}

    series = data["Time Series (Daily)"]
    nuevos = 0

    for date_str, daily_data in series.items():
        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Si ya tenemos esa fecha almacenada, la saltamos
        if session.query(Stock).filter_by(symbol=symbol, date=date).first():
            continue

        open_price = float(daily_data["1. open"])
        close_price = float(daily_data["4. close"])
        variation = ((close_price - open_price) / open_price) * 100

        nuevo_stock = Stock(
            symbol=symbol,
            date=date,
            open=open_price,
            close=close_price,
            high=float(daily_data["2. high"]),
            low=float(daily_data["3. low"]),
            volume=float(daily_data["5. volume"]),
            variation_pct=round(variation, 2)
        )
        session.add(nuevo_stock)
        nuevos += 1

    session.commit()

    # Buscar el más reciente después del guardado
    latest = session.query(Stock).filter_by(symbol=symbol).order_by(Stock.date.desc()).first()
    session.close()

    if latest:
        print(f"Guardados {nuevos} registros nuevos. Devolviendo el dato más reciente: {latest.date}")
        return stock_to_dict(latest)
    else:
        return {"error": f"No se pudo guardar ningún dato para {symbol}"}





'''

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
'''
