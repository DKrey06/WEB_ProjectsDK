from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	hashed_password = db.Column(db.String(200), nullable=False)
	created_date = db.Column(db.DateTime, default=datetime.utcnow)
