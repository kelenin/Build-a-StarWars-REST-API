from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Date

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favoriteses = db.relationship('Favorites', backref="owner")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__='character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    favoriteses = db.relationship('Favorites', backref="character")

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name_character": self.name,
            "description": self.description
        }

class Favorites(db.Model): 
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))
    planeta_id = db.Column(db.Integer, ForeignKey("planets.id"), nullable=True)
    character_id = db.Column(db.Integer, ForeignKey("character.id"), nullable=True)

    def __repr__(self):
        return '<Favorites %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name_favorites": self.name,
            "user_id": self.user_id,
            "planeta_id": self.planeta_id,
            "character_id": self.character_id,
        }

class Planets(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    favorites = db.relationship('Favorites', backref="planets")

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name_planets": self.name,
            "description": self.description,
            # do not serialize the password, its a security breach
        }

