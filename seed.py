from app import app

from models import Images, ImageWords, GuessedImages, InProgessImages, GeneratedMemes, db

db.drop_all()
db.create_all()

Images.query.delete()
ImageWords.query.delete()

meme1 = Images(phrase="TestMemeName")

db.session.add(meme1)
db.session.commit()

word1 = ImageWords(word="Test", image_id=1)
word2 = ImageWords(word="Meme", image_id=1)
word3 = ImageWords(word="Name", image_id=1)

db.session.add_all([word1, word2, word3])


db.session.commit()