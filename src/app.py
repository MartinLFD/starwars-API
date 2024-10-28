"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Favorite_character, Favorite_planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#Endpoints Tabla User

@app.route('/post-new-user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        age=data.get('age'),
        name=data.get('name'),
        email=data.get('email')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
#Traer los favoritos de planetas
    favorite_planets = [favorite.planet.serialize() for favorite in user.favorite_planet]
#Traer los favoritos de characters
    favorite_characters = [favorite.character.serialize() for favorite in user.favorite_character]

    return jsonify({
        "user_id": user.id,
        "favorites": {
            "planets": favorite_planets,
            "characters": favorite_characters
        }
    }), 200




#Endpoints Tabla Planet
@app.route('/post-new-planet', methods=['POST'])
def create_planet():
    data = request.get_json()
    new_planet = Planet(
        name=data.get('name'),
        rotation_period=data.get('rotation_period'),
        orbital_period=data.get('orbital_period'),
        diameter=data.get('diameter'),
        climate=data.get('climate'),
        gravity=data.get('gravity'),
        terrain=data.get('terrain'),
        surface_water=data.get('surface_water'),
        population=data.get('population')
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/users/<int:user_id>/favorites/planets', methods=['POST'])
def add_favorite_planet(user_id):
    data = request.get_json()
    planet_id = data.get('planet_id')

    # Verificar si el usuario y el planeta existen
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)
    if user is None or planet is None:
        return jsonify({"error": "User or planet not found"}), 404

    # Crear y agregar el planeta favorito
    favorite_planet = Favorite_planet(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite_planet)
    db.session.commit()

    return jsonify({"message": "Favorite planet added successfully"}), 201

@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite_planet = Favorite_planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    
    if favorite_planet is None:
        return jsonify({"error": "Favorite planet not found"}), 404

    db.session.delete(favorite_planet)
    db.session.commit()

    return jsonify({"message": "Favorite planet deleted successfully"}), 200




#Endpoint Tabla Character
@app.route('/post-new-character', methods=['POST'])
def create_character():
    data = request.get_json()
    new_character = Character(
        description=data.get('description'),
        name=data.get('name'),
        skin_color=data.get('skin_color'),
        mass=data.get('mass'),
        hair_color=data.get('hair_color'),
        gender=data.get('gender'),
        eye_color=data.get('eye_color'),
        planet_id=data.get('planet_id'),
        film_id=data.get('film_id')
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_character_by_id(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.serialize()), 200

@app.route('/users/<int:user_id>/favorites/characters', methods=['POST'])
def add_favorite_character(user_id):
    data = request.get_json()
    character_id = data.get('character_id')

    # Verificar si el usuario y el personaje existen
    user = User.query.get(user_id)
    character = Character.query.get(character_id)
    if user is None or character is None:
        return jsonify({"error": "User or character not found"}), 404

    # Crear y agregar el personaje favorito
    favorite_character = Favorite_character(user_id=user_id, character_id=character_id)
    db.session.add(favorite_character)
    db.session.commit()

    return jsonify({"message": "Favorite character added successfully"}), 201

@app.route('/users/<int:user_id>/favorites/characters/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    favorite_character = Favorite_character.query.filter_by(user_id=user_id, character_id=character_id).first()
    
    if favorite_character is None:
        return jsonify({"error": "Favorite character not found"}), 404

    db.session.delete(favorite_character)
    db.session.commit()

    return jsonify({"message": "Favorite character deleted successfully"}), 200





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
