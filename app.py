from flask import Flask
from flask_cors import CORS
from routes.stocks import stocks_bp

app = Flask(__name__)
CORS(app)  # Permite peticiones del frontend

app.register_blueprint(stocks_bp)

if __name__ == '__main__':
    app.run(debug=True)
