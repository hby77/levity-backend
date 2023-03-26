from datetime import datetime
from models.db import db


class Track(db.EmbeddedDocument):
    title = db.StringField()
    episode_title = db.StringField()
    creation_date = db.DateTimeField(default=datetime.now)
    modified_date = db.DateTimeField(default=datetime.now)