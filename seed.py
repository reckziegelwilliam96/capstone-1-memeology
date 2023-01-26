from app import app

from models import Memes, Words, db

db.drop_all()
db.create_all()

Memes.query.delete()
Words.query.delete()

meme1 = Memes(meme_name="TestMemeName")

db.session.add(meme1)
db.session.commit()

word1 = Words(word="Test", meme_id=1)
word2 = Words(word="Meme", meme_id=1)
word3 = Words(word="Name", meme_id=1)

db.session.add_all([word1, word2, word3])
db.session.commit()