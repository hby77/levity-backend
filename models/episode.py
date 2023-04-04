from datetime import datetime
from models.track import Track
from models.db import db


class Episode(db.Document):
    title = db.StringField()
    description = db.StringField()
    image = db.StringField()
    date = db.StringField()
    embeddedEpisode = db.StringField()
    likes = db.IntField()
    track = db.EmbeddedDocumentListField(Track)
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)