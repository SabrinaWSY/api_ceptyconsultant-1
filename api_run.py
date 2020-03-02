# coding: utf-8

from flask import Flask, request, json, jsonify, make_response
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import render_template
from flask import Response, redirect
import datetime

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

#======================================================================
# Gestion des identifiants des utilisateurs

def get_users(filename="LISTE_COLLABORATEURS.json"):
	"""On lit le fichier contenant les données des utilisateurs et on créé leurs identifants"""
	# TO DO : Changer les données des identifiants : actuellement les identifiants sont :
	# id:Prénom, mdp:Nom
	# Ceci est seulement pour faciliter la démonstration mais en production les mot de passe
	# seront beaucoup plus sécurisés
	with open(os.path.join("data", filename), "r", encoding="utf8") as data_file:
		data = json.load(data_file)
	users = {user[1]["prenom"]:generate_password_hash(user[1]["nom"]) for user in data.items()}
	return users
users = get_users()


@auth.verify_password
def verify_password(username, password):
	"""On vérifie que les iddentifiants de l'utilisateur sont corrects"""
	if username in users:
		return check_password_hash(users[username], password)
	return False

#========================================================================

file_data = "DONNEES_CLIENT.json"
# fonction de lecture
def get_data(filename=file_data):
	with open(os.path.join("data", filename), "r", encoding="utf8") as data_file:
		data = json.load(data_file)
	return data

# fonction d'écriture
def save_data(data, filename=file_data):
	with open(os.path.join("data", filename), "w", encoding="utf8") as data_file:
		data_file.write(json.dumps(data, indent=4))


class Login(Resource):
	"""retourne le contenu du fichier json"""
	#@auth.login_required
	def get(self):
		render_login = render_template("index.html")
		resp = Response(render_login, status=200, content_type="text/html")
		return resp

	def post(self):
		info = request.form
		return redirect("/ceptyconsultant.local/data", code=302)


class Data(Resource):
	"""retourne le contenu du fichier json"""
	def get(self, contrib_name, public_id=None):
		data = get_data()
		result = []
		if public_id == None:
			for d in data["contributions"]["data"]:
				if d["contrib_name"] == contrib_name: 
					result.append(d)
			if len(result) == 0:
				res = make_response({"ERROR":"contrib_name introuvable"}, 404)
			else : res = make_response({"data":result} , 200)
			return res

		else :
			for d in data["contributions"]["data"]:
				if d["contrib_name"] == contrib_name and d["public_id"] == public_id: 
					result.append(d)
			if len(result) == 0:
				res = make_response({"ERROR":"contrib_name ou public_id introuvable"}, 404)
			else : res = make_response({"data":result} , 200)
			return res


	def put(self):
		data = get_data()
		data_add = request.json
		# TODO Ajouter des conditions pour vérifier que les données entrées
		# ne rentrent pas en conflit avec les données du fichier json
		# Actuellement la seule condition est l'article_id
		list_id = [d["article_id"] for d in data["contributions"]["data"]]
		if data_add["article_id"] in list_id:
			res = make_response(jsonify({"ERROR": "article_id existe déjà"}), 400)
			return res
		else:
			time = datetime.datetime.utcnow()
			data_add['last_update'] = time
			data["contributions"]["data"].append(data_add)
			save_data(data)
			res = make_response(jsonify({"OK": "Article ajouté avec succès"}), 200)
			return res

	def post(self):
		data = get_data()
		data_edit = request.json
		article_id = request.args.get('article_id')
		for n, d in enumerate(data["contributions"]["data"]):
			if d["article_id"] == article_id:
				for key, value in data_edit.items():
					time = datetime.datetime.utcnow()
					d[key] = value
					d["last_update"] = time
				save_data(data)
				make_response(jsonify({"OK": "Données modifées avec succès"}), 200)
				return jsonify(d)
		else:
			res = make_response(jsonify({"ERROR": "Article non trouvé"}), 404)
			return res

	def delete(self):
		data = get_data()
		article_id = request.args.get('article_id')
		for n, d in enumerate(data["contributions"]["data"]):
			if d["article_id"] == article_id:
				del data["contributions"]["data"][n]
				save_data(data)
				res = make_response(jsonify({"OK": "Article supprimé avec succés"}), 200)
				return res
		else:
			res = make_response(jsonify({"ERROR": "Article non trouvé"}), 404)
			return res

api.add_resource(Login, "/","/ceptyconsultant.local/", "/ceptyconsultant.local/authentification")
api.add_resource(Data, "/ceptyconsultant.local/data", "/ceptyconsultant.local/data/<string:contrib_name>",
						"/ceptyconsultant.local/data/<string:contrib_name>/<string:public_id>")


if __name__ == '__main__':
	app.run(debug=True)
