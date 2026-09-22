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
from models import db, Usuario, Personaje, Favorito, Planeta

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

# ==========================================
# ENDPOINTS DE USUARIOS Y FAVORITOS
# ==========================================

@app.route('/users', methods=['GET'])
def get_all_users():
    usuarios = Usuario.query.all()
    results = list(map(lambda u: u.serialize(), usuarios))
    return jsonify(results), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # Solución: Buscamos dinámicamente al primer usuario que exista
    usuario = Usuario.query.first()
    if not usuario:
        return jsonify({"msg": "No hay usuarios en la base de datos"}), 404
    current_user_id = usuario.id
    
    favoritos = Favorito.query.filter_by(user_id=current_user_id).all()
    results = list(map(lambda f: f.serialize(), favoritos))
    return jsonify(results), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    usuario = Usuario.query.first()
    if not usuario:
        return jsonify({"msg": "No hay usuarios en la base de datos"}), 404
    current_user_id = usuario.id

    # Validar que el planeta exista
    planeta = Planeta.query.get(planet_id)
    if not planeta:
        return jsonify({"msg": "Planeta no existe"}), 404

    # Validar que no esté ya en favoritos
    favorito_existente = Favorito.query.filter_by(user_id=current_user_id, planeta_id=planet_id).first()
    if favorito_existente:
        return jsonify({"msg": "El planeta ya está en favoritos"}), 400

    nuevo_favorito = Favorito(user_id=current_user_id, planeta_id=planet_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify({"msg": "Planeta añadido a favoritos"}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    usuario = Usuario.query.first()
    if not usuario:
        return jsonify({"msg": "No hay usuarios en la base de datos"}), 404
    current_user_id = usuario.id

    # Validar que el personaje exista
    personaje = Personaje.query.get(people_id)
    if not personaje:
        return jsonify({"msg": "Personaje no existe"}), 404

    # Validar que no esté ya en favoritos
    favorito_existente = Favorito.query.filter_by(user_id=current_user_id, personaje_id=people_id).first()
    if favorito_existente:
        return jsonify({"msg": "El personaje ya está en favoritos"}), 400

    nuevo_favorito = Favorito(user_id=current_user_id, personaje_id=people_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    return jsonify({"msg": "Personaje añadido a favoritos"}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    usuario = Usuario.query.first()
    if not usuario:
        return jsonify({"msg": "No hay usuarios en la base de datos"}), 404
    current_user_id = usuario.id

    favorito = Favorito.query.filter_by(user_id=current_user_id, planeta_id=planet_id).first()
    if not favorito:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorito)
    db.session.commit()

    return jsonify({"msg": "Planeta favorito eliminado"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    usuario = Usuario.query.first()
    if not usuario:
        return jsonify({"msg": "No hay usuarios en la base de datos"}), 404
    current_user_id = usuario.id

    favorito = Favorito.query.filter_by(user_id=current_user_id, personaje_id=people_id).first()
    if not favorito:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorito)
    db.session.commit()

    return jsonify({"msg": "Personaje favorito eliminado"}), 200

# ==========================================
# ENDPOINTS DE PERSONAJES (PEOPLE)
# ==========================================

@app.route('/people', methods=['GET'])
def get_all_people():
    personajes = Personaje.query.all()
    results = list(map(lambda p: p.serialize(), personajes))
    return jsonify(results), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_personaje(people_id):
    personaje = Personaje.query.get(people_id)
    if personaje is None:
        return jsonify({"msg": "Personaje no encontrado"}), 404
    return jsonify(personaje.serialize()), 200

# ==========================================
# ENDPOINTS DE PLANETAS (PLANETS)
# ==========================================

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planetas = Planeta.query.all()
    results = list(map(lambda p: p.serialize(), planetas))
    return jsonify(results), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planeta(planet_id):
    planeta = Planeta.query.get(planet_id)
    if planeta is None:
        return jsonify({"msg": "Planeta no encontrado"}), 404
    return jsonify(planeta.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)