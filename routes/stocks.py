from flask import Blueprint, request, jsonify
from services.alphavantage import get_stock_data

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