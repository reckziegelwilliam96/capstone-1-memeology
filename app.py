from flask import Flask, render_template, jsonify
import requests, random
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Memes, MemeWords

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
    url = "https://ronreiter-meme-generator.p.rapidapi.com/images"

    headers = {
    	"X-RapidAPI-Key": "4107f9a719msh7b803084f28bdd6p10d9b2jsn4c84f0422879",
    	"X-RapidAPI-Host": "ronreiter-meme-generator.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    image_list = response.text
    phrases = image_list.split(',')
    """get a sample of image_list"""
    random_indices = random.sample(range(len(phrases)), 20)
    print(random_indices)
    random_images = [phrases[i] for i in random_indices]
    print(random_images)

    """separate image list into phrases for Meme class and words for MemeWords class"""
    
    # result=[]
    # for phrase in phrases:
    #     cleaned_phrase = phrase.replace('"','')
    #     print(cleaned_phrase)
    #     # meme = Memes(meme_name=cleaned_phrase)
    #     # db.session.add(meme)
    #     # db.session.commit()
    #     words = cleaned_phrase.split('-')
    #     for word in words:
    #         # MemeWords(word=word, meme_id=meme.id)
    #         print(word)
    #     print(words)
    #     result.append(words)
    # print(result)

    return response.text