"""Models for Iconicle app."""

from re import M
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Meme(db.Model):
    """Memes."""

    __tablename__ = "database_memes"

    id = db.Column(db.Integer,
                    primary_key=True,
                    unique=True,
                    nullable=False)

    meme_name = db.Column(db.Text,
                            nullable=False)
    
    meme_words = db.Relationship('MemeWords', backref='meme')

class MemeWords(db.Model):
    """Keywords of Memes."""

    __tablename__ = "memes_words"

    id = db.Column(db.Integer,
                    primary_key=True,
                    unique=True,
                    nullable=False)

    word = db.Column(db.Text,
                    nullable=False)
    
    meme_id = db.Column(db.Integer,
                        db.ForeignKey("database_memes.id"))
                        
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)