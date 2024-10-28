import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from flask_sqlalchemy import  SQLAlchemy

db =  SQLAlchemy()



Base = db.Model

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False )
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    favorite_planet = relationship('Favorite_planet')
    favorite_character = relationship('Favorite_character')

class Favorite_planet(Base):
    __tablename__ = 'favorite_planet'
    user_primary_id = Column(Integer, primary_key=True)
    planet_primary_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id') )
    planet_id = Column(Integer, ForeignKey('planet.id') )

class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key= True)
    name = Column(String(100), unique= True, nullable=False)
    rotation_period = Column(Integer)
    orbital_period = Column(Integer)
    diameter = Column(Integer)
    climate = Column(String(50))
    gravity = Column(String(50))
    terrain = Column(String(50)) 
    surface_water = Column(Integer)
    population = Column(Integer)
    planet = relationship('Favorite_planet') 

class Favorite_character(Base):
    __tablename__ = 'favorite_character'
    user_primary_id = Column(Integer, primary_key=True)
    character_primary_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id') )
    character_id = Column(Integer, ForeignKey('character.id') )

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key= True)
    description = Column(String(200))
    name = Column(String(200 ), unique= True, nullable=False )
    skin_color = Column(String(20))
    mass = Column(Integer)
    hair_color = Column(String(20))
    gender = Column(String(20)) 
    eye_color = Column(String(200))
    planet_id = Column(Integer)
    film_id = Column(Integer)
    favorite_character = relationship('Favorite_character')

    def to_dict(self):
        return {}


