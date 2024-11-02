from flask import Blueprint, jsonify, request
from models import db, Usuario, Planeta, Personaje, Favorito


api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def get_users():
    users = Usuario.query.all()
    return jsonify([user.serialize() for user in users]), 200

@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    user = Usuario.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify([fav.serialize() for fav in user.favoritos]), 200




@api.route('/people', methods=['GET'])
def get_people():
    people = Personaje.query.all()
    return jsonify([person.serialize() for person in people]), 200

@api.route('/people/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = Personaje.query.get(person_id)
    if not person:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(person.serialize()), 200




@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planeta.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planeta.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200




@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    user = Usuario.query.get(user_id)
    planet = Planeta.query.get(planet_id)
    
    if not user or not planet:
        return jsonify({"error": "Usuario o planeta no encontrado"}), 404
    
    favorito = Favorito(usuario_id=user.id, planeta_id=planet.id)
    db.session.add(favorito)
    db.session.commit()
    return jsonify(favorito.serialize()), 201

@api.route('/favorite/people/<int:person_id>', methods=['POST'])
def add_favorite_person(person_id):
    user_id = request.json.get("user_id")
    user = Usuario.query.get(user_id)
    person = Personaje.query.get(person_id)
    
    if not user or not person:
        return jsonify({"error": "Usuario o personaje no encontrado"}), 404
    
    favorito = Favorito(usuario_id=user.id, personaje_id=person.id)
    db.session.add(favorito)
    db.session.commit()
    return jsonify(favorito.serialize()), 201

@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get("user_id")
    favorito = Favorito.query.filter_by(usuario_id=user_id, planeta_id=planet_id).first()
    
    if not favorito:
        return jsonify({"error": "Favorito no encontrado"}), 404
    
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "Favorito eliminado"}), 200

@api.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def delete_favorite_person(person_id):
    user_id = request.json.get("user_id")
    favorito = Favorito.query.filter_by(usuario_id=user_id, personaje_id=person_id).first()
    
    if not favorito:
        return jsonify({"error": "Favorito no encontrado"}), 404
    
    db.session.delete(favorito)
    db.session.commit()
    return jsonify({"message": "Favorito eliminado"}), 200


def init_app(app):
    app.register_blueprint(api, url_prefix='/api')
