import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    favorite_planet = relationship('Favorite_planet', back_populates='user')
    favorite_character = relationship('Favorite_character', back_populates='user')

    def serialize(self):
        return {
            'id': self.id,
            'age': self.age,
            'name': self.name,
            'email': self.email
        }

class Favorite_planet(db.Model):
    __tablename__ = 'favorite_planet'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), primary_key=True)

    user = relationship('User', back_populates='favorite_planet')
    planet = relationship('Planet', back_populates='favorites')  # Relación inversa

    def serialize(self):
        return {
            'user_id': self.user_id,
            'planet_id': self.planet_id
        }


class Planet(db.Model):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    rotation_period = Column(Integer)
    orbital_period = Column(Integer)
    diameter = Column(Integer)
    climate = Column(String(50))
    gravity = Column(String(50))
    terrain = Column(String(50))
    surface_water = Column(Integer)
    population = Column(Integer)

    favorites = relationship('Favorite_planet', back_populates='planet')  # Relación inversa

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'rotation_period': self.rotation_period,
            'orbital_period': self.orbital_period,
            'diameter': self.diameter,
            'climate': self.climate,
            'gravity': self.gravity,
            'terrain': self.terrain,
            'surface_water': self.surface_water,
            'population': self.population
        }

class Favorite_character(db.Model):
    __tablename__ = 'favorite_character'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    character_id = Column(Integer, ForeignKey('character.id'), primary_key=True)

    user = relationship('User', back_populates='favorite_character')
    character = relationship('Character', back_populates='favorites')  # Relación inversa

    def serialize(self):
        return {
            'user_id': self.user_id,
            'character_id': self.character_id
        }


class Character(db.Model):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    description = Column(String(200))
    name = Column(String(200), unique=True, nullable=False)
    skin_color = Column(String(20))
    mass = Column(Integer)
    hair_color = Column(String(20))
    gender = Column(String(20))
    eye_color = Column(String(200))
    planet_id = Column(Integer)
    film_id = Column(Integer)

    favorites = relationship('Favorite_character', back_populates='character')  # Relación inversa

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'name': self.name,
            'skin_color': self.skin_color,
            'mass': self.mass,
            'hair_color': self.hair_color,
            'gender': self.gender,
            'eye_color': self.eye_color,
            'planet_id': self.planet_id,
            'film_id': self.film_id
        }
