# importações
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# caminho do arquivo de banco de dados - sqlite
path = os.path.dirname(os.path.abspath(__file__)) 
arquivobd = os.path.join(path, 'game.db')
# sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)