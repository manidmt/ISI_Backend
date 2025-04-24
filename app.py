from flask import Flask
from flask_cors import CORS
from routes.stocks import stocks_bp
from routes.bonds import bonds_bp

app = Flask(__name__)
CORS(app)  # Permite peticiones del frontend

app.register_blueprint(stocks_bp)
app.register_blueprint(bonds_bp)

if __name__ == '__main__':
    app.run(debug=True)
