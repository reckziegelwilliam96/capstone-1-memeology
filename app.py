from flask import Flask, render_template, jsonify
import json
import requests
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///iconicle-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'iconicle-key'
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def display_home():
    """Show home page."""

    return render_template('homepage.html')

# @app.route('/render-game')
# def display_game():
#     """Show game page."""

#     return render_template('gamepage.html')

@app.route('/api/get-images-list')
def get_api_list_images():
    url = "https://ronreiter-meme-genertor.p.rapidapi.com/images"

    headers = {
        "X-RapidAPI-Key": "4107f9a719msh7b803084f28bdd6p10d9b2jsn4c84f0422879",
        "X-RapidAPI-Host": "ronreiter-meme-generator.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    response = json.loads(response.text)
    return jsonify(response)