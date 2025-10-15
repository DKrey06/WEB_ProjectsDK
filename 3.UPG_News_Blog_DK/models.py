from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'user'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	hashed_password = db.Column(db.String(200), nullable=False)
	created_date = db.Column(db.DateTime, default=datetime.now)

	articles = db.relationship('Article', backref='author', lazy=True)

	def set_password(self, password):
		self.hashed_password = generate_password_hash(password)
    
	def check_password(self, password):
		return check_password_hash(self.hashed_password, password)

class Article(db.Model):
	__tablename__ = 'article'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	text = db.Column(db.Text, nullable=False)
	created_date = db.Column(db.DateTime, default=datetime.now)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
