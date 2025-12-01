# main.py
import os
from flask import Flask
from app.database import SessionLocal, Base, engine  # Import Base and engine
from app.auth import auth
#from app.home import home 
from app.webui import webui
from app.attendance import attendance

from app.models import Employee 
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='templates')
bcrypt = Bcrypt(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Create tables
Base.metadata.create_all(bind=engine)

app.secret_key = "dev-key-123"

# Routes
app.register_blueprint(auth)
app.register_blueprint(attendance)
#app.register_blueprint(home) 
app.register_blueprint(webui)  

if __name__ == "__main__":
    print("Flask server running on http://127.0.0.1:5000")
    app.run(debug=True)
