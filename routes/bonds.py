from flask import Blueprint, request, jsonify
from datetime import datetime

from models.stock import Stock, Session
from services.scraper import get_bonds_info

bonds_bp = Blueprint('bonds', __name__)

@bonds_bp.route('/bonds/<country>', methods=['GET'])
def get_bond_data(country):
    if not country:
        return jsonify({"error": "Missing symbols query parameter"}), 400
    
    data = get_bonds_info(country)
    return jsonify(data)