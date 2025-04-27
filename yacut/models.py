from datetime import datetime

from . import db
from .constants import SHORT_ID_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(SHORT_ID_LENGTH),
                      nullable=False, unique=True, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
