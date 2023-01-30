from flask import Flask, render_template, request, session
import requests, random
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Meme, MemeWords

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

@app.route('/api/get-images-list')
def get_api_list_images():
    """Get API list from Meme Generator API and send response to parseList function in JS"""

    url = "https://ronreiter-meme-generator.p.rapidapi.com/images"

    headers = {
    	"X-RapidAPI-Key": "4107f9a719msh7b803084f28bdd6p10d9b2jsn4c84f0422879",
    	"X-RapidAPI-Host": "ronreiter-meme-generator.p.rapidapi.com"
    }
    
    try:
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        return response.text

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occured: {req_err}')
    except Exception as e:
        print(f'An error occurred:{e}')   

@app.route('/api/post-meme-names-seed-db', methods=["POST"])
def post_meme_names_seed_iconicle_db():
    """Seed database with post request from JS file, 
    parse random_images phrases into Meme class, 
    parse again into MemeWords class """

    try:
        random_images = request.get_json()
        try:
            for meme_name in random_images:
                meme = Meme(meme_name=meme_name)
                db.session.add(meme)
                db.session.commit()
                for phrase in meme_name:
                    try:
                        cleaned_phrase = phrase.replace('"','')
                        words = cleaned_phrase.split('-')
                        for word in words:
                            try:
                                meme_word = MemeWords(word=word, meme_id=meme.id)
                                db.session.add(meme_word)
                                db.session.commit()

                            except Exception as e:
                                print(f"Error adding word {word} to the database: {e}")
                                db.session.rollback()
                    except Exception as e:
                        print(f"Error cleaning phrase {phrase}: {e}")
                        db.session.rollback()
        except Exception as e:
            print(f"Error adding meme {meme_name} to the database: {e}")
            db.session.rollback()
    except Exception as e:
        print(f"Error getting data from request: {e}")
        return "Error getting data from request", 500

    session['meme'] = random.choice(random_images)

@app.route('/api/get-generate-meme')
def get_api_generate_meme():
    """Get random meme from session 
    using predefined images in API Meme Generator."""
    meme = session['meme']

    url = "https://ronreiter-meme-generator.p.rapidapi.com/meme"

    querystring = {"top":".",
                    "bottom":".",
                    "meme":f"{meme}",
                    "font_size":"1",
                    "font":"Impact"
                    }

    headers = {
	    "X-RapidAPI-Key": "4107f9a719msh7b803084f28bdd6p10d9b2jsn4c84f0422879",
	    "X-RapidAPI-Host": "ronreiter-meme-generator.p.rapidapi.com"
    }
    
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occured: {req_err}')
    except Exception as e:
        print(f'An error occurred:{e}') 
   
