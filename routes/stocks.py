from flask import Blueprint, request, jsonify
from datetime import datetime

from services.alphavantage import get_stock_data
from models.stock import Stock, Session
from services.alphavantage import stock_to_dict
from services.scraper import scrape_or_get_company_info

stocks_bp = Blueprint('stocks', __name__)

@stocks_bp.route('/stock/<symbol>', methods=['GET'])
def stock_info(symbol):
    data = get_stock_data(symbol)
    return jsonify(data)



@stocks_bp.route('/stock/compare', methods=['GET'])
def compare_stocks():
    symbols = request.args.get('symbols')

    if not symbols:
        return jsonify({"error": "Missing symbols query parameter"}), 400


    symbols = symbols.split(',')
    data = [get_stock_data(symbol) for symbol in symbols]
    return jsonify(data)


@stocks_bp.route('/stock/history/<symbol>', methods=['GET'])
def stock_history(symbol):
    session = Session()
    today = datetime.today().date()
    if not session.query(Stock).filter_by(symbol=symbol, date=today).first():
        get_stock_data(symbol)
    rows = session.query(Stock).filter_by(symbol=symbol).order_by(Stock.date.asc()).all()
    session.close()
    return jsonify([stock_to_dict(row) for row in rows])


@stocks_bp.route('/company/<symbol>', methods=['GET'])
def company_info(symbol):
    data = scrape_or_get_company_info(symbol.upper())
    return jsonify(data)
