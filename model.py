from datetime import datetime
from database import db


class ShortUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # url = db.Column(db.String(), index=True, unique=True)
    url = db.Column(db.String(), index=True)
    hash = db.Column(db.String(8), index=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now())


class HitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_url_id = db.Column(db.Integer,
                             db.ForeignKey('short_url.id'), index=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
