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
from models import db, User, Peoples, Favorites, Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/user', methods=['GET'])
def handle_hello():

    all_user = User.query.all()
    return jsonify(
        [ users.serialize() for users in all_user]
    ), 200

@app.route('/user/favorites', methods=['GET'])
def get_users_favorites():

    all_favorites = Favorites.query.all()
    return jsonify(
        [ favorites.serialize() for favorites in all_favorites]
    ), 200


@app.route('/people', methods=['GET'])
def people_todos():
    #consultas los personajes
    #devolver personas serializadas
    all_people = Peoples.query.all()
    return jsonify(
        [ people.serialize() for people in all_people]
    ), 200

@app.route('/favorites/people/<int:people_id>', methods=['GET','POST','DELETE'])
def post_people(people_id):
    body = request.json
    search = Peoples.query.get(people_id)

    if request.method == 'GET':
        if search != None:
            return jsonify(search.serialize()), 200
        else:
            return 'No se encontro el people', 404
    elif request.method == 'POST':
        if "name" not in body:
            return 'Debe indicar la descripcion porque es favorito!', 400
        if "user_id" not in body:
            return 'Debe indicar el usuario', 400
        if "people_id" not in body:
            return 'Debe indicar el people', 400
        new_row = Favorites.new_registro_favorites(body["name"], body["user_id"], None, body["people_id"])
        if new_row == None:
            return 'Un error ha ocurrido, upps!', 500
        else:
            return jsonify(new_row.serialize()), 200
    else:
        searchdelete = Favorites.query.get(people_id)

        result = searchdelete.delete()
        if result == True:
            return f'El people {people_id} ha sido eliminado con exito!', 200
        else:
            return 'Un error ha ocurrido, upps!', 500

@app.route('/planets', methods=['GET'])
def get_planets():
    #consultas todos los planetas
    all_planets = Planets.query.all()
    return jsonify(
        [ planets.serialize() for planets in all_planets]
    ), 200

@app.route('/favorites/planets/<int:planet_id>', methods=['GET','POST','DELETE'])
def post_planets(planet_id):
    body = request.json
    search = Planets.query.get(planet_id)

    if request.method == 'GET':
        if search != None:
            return jsonify(search.serialize()), 200
        else:
            return 'No se encontro el planeta', 404
    elif request.method == 'POST':
        if "name" not in body:
            return 'Debe indicar la descripcion porque es favorito!', 400
        if "user_id" not in body:
            return 'Debe indicar el usuario', 400
        if "planet_id" not in body:
            return 'Debe indicar el planeta', 400
        new_row = Favorites.new_registro_favorites(body["name"], body["user_id"], body["planet_id"], None)
        if new_row == None:
            return 'Un error ha ocurrido, upps!', 500
        else:
            return jsonify(new_row.serialize()), 200
    else:
        searchdelete = Favorites.query.get(planet_id)

        result = searchdelete.delete()
        if result == True:
            return f'El planeta {planet_id} ha sido eliminado con exito!', 200
        else:
            return 'Un error ha ocurrido, upps!', 500



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
