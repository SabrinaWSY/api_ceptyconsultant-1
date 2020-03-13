# coding: utf-8

from flask import Flask, request, json, jsonify, make_response, Response, redirect
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import datetime
import jwt
import json


app = Flask(__name__)
api = Api(app)


#======================================================================
# Gestion des identifiants des utilisateurs
class User:
	"Un utilisateur avec son id, son nom d'utilisateur, et son mot de passe"
	def __init__(self, cepty_id:str, username:str, password):
		self.id = cepty_id
		self.username = username
		self.password = password

	def to_json(self):
		return {
			"cepty_id":self.id,
			"username":self.username,
			"password":self.password
			}


def get_users(filename="accounts.json"):
	"""Crée les comptes utilisateur"""
	with open(os.path.join("data", filename), "r", encoding="utf8") as data_file:
		accounts = json.load(data_file)
	users = []
	for account in accounts:
		user = User(account["id"], account["username"], generate_password_hash(account["password"]))
		users.append(user)
	return users

users = get_users()


# la clé (très) secrête
key = "\xd5PE\xa3t\x96D\xa2\xae\xc2\xcfIq\xe7\xefk"



def make_token(user):
		"""Génère le auth token"""
		encode_params = { 
			"id": user.id,
			"exp": datetime.datetime.utcnow()+\
			datetime.timedelta(minutes=30)
		}
		try:
			token = jwt.encode(encode_params, key, algorithm='HS256')
			return token
		except jwt.ExpiredSignatureError:
			return "token expired!"


def verify_password(username:str, password:str):
	"""Vérifie que les iddentifiants de l'utilisateur sont corrects"""
	for user in users:
		if user.username == username:
			if check_password_hash(user.password, password): 
				return user
		return False
	
# =====================================================================


def token_required(f):
	"""Crée le décorateur qui permettra de vérifier la présence
	du token dans le header pour chaque requête""" 
	@wraps(f)
	def decorator(*args, **kwargs):
		token = None
		if 'x-access-tokens' in request.headers:
			token = request.headers['x-access-tokens']
		if not token:
			return {'message': 'token manquant'}
		try:
			data = jwt.decode(token, key)
			current_user = data["id"]
		except:
			return {'message': 'token invalide'}
		return f(current_user, *args, **kwargs)
	return decorator



#========================================================================

file_data = "DONNEES_CLIENT.json"
def get_data(filename=file_data):
	"""Retourne les données contenues dans notre fichier de données"""
	with open(os.path.join("data", filename), "r", encoding="utf8") as data_file:
		data = json.load(data_file)
	return data

def save_data(data, filename=file_data):
	""""Enregistre les nouvelles données dans notre fichier de données"""
	with open(os.path.join("data", filename), "w", encoding="utf8") as data_file:
		data_file.write(json.dumps(data, indent=4))


#=========================================================================

class Login(Resource):
	"""Login"""
	def post(self):
		""""Crée le token d'un utilisateur si les informations reçues 
		correspondent bien à un compte utilisateur"""

		# On récupère les informations
		info = request.json

		# On vérifie que les identifiants correpondent à un utilisateur
		# Si oui on crée le token, l'utilisateur correspondant et le token sont renvoyés
		# Si non, une erreur est renvoyé
		user = verify_password(info["username"],info["password"])
		if user:
			token = make_token(user)
			return {'User':user.to_json(), 'Token': token.decode('UTF-8')}
		else:
			return {"ERROR":"Username ou mot de passe incorrect"}, 400


class Data(Resource):
	"""Gère la manipulation des données"""

	@token_required
	def get(self, current_user, contrib_name=None, public_id=None):
		"""Gère l'accès et le filtrage des données"""

		data = get_data()
		result = []

		# Renvoie toutes les données
		if public_id==None and contrib_name==None:
			result = data["contributions"]["data"]
			res = {"data":result}, 200

		# Renvoie les données filtrées sur un contrib_name
		# Si aucune données n'est trouvée une erreur est renvoyée
		if public_id==None and contrib_name!=None:
			for d in data["contributions"]["data"]:
				if d["contrib_name"] == contrib_name: 
					result.append(d)
			if len(result) == 0:
				res = {"ERROR":"Aucune donnée n'a été trouvée"}, 404
			else : res = {"data":result}, 200

		# Renvoie les données filtrées sur un contrib_name + public_id
		# Si aucune données n'est trouvée une erreur est renvoyée
		if public_id!=None and contrib_name!=None:
			for d in data["contributions"]["data"]:
				if d["contrib_name"] == contrib_name and d["public_id"] == public_id: 
					result.append(d)
			if len(result) == 0:
				res = {"ERROR":"Aucune donnée n'a été trouvée"}, 404
			else : res = {"data":result}, 200
		
		return res
		


	@token_required
	def put(self, current_user):
		"""Ajoute des données"""

		# On va chercher les données déjà existantes
		data = get_data()

		# On reçoit les informations à ajouter
		# envoyées par l'utilisateur  
		data_add = request.json

		# On suppose que l'article_id est unique, 
		# on l'uitilise donc pour identifier les éléments
		# Si l'article_id existe déjà on renvoie une erreur,
		# sinon on peut ajouter les nouvelles données
		list_id = [d["article_id"] for d in data["contributions"]["data"]]
		if data_add["article_id"] in list_id:
			res = {"ERROR": "Article_id existe déjà"}, 400
			return res
		else:
			time = datetime.datetime.utcnow()
			data_add["last_update"] = str(time)
			data["contributions"]["data"].append(data_add)
			save_data(data)
			res = {"OK": "Article ajouté avec succès"}, 200
			return res

	@token_required
	def post(self, current_user):
		"""Modifie des données"""

		# On va chercher les données déjà existantes
		data = get_data()

		# On reçoit les informations à modifier
		# envoyées par l'utilisateur  
		data_edit = request.json

		# On recupère l'article_id pour connaître l'élément à modifier
		article_id = request.args.get('article_id')
		
		# On cherche l'élément correspondant à l'article_id
		# Si on le trouve alors on le modifie avec les informations reçues,
		# Sinon on retourne un erreur
		for n, d in enumerate(data["contributions"]["data"]):
			if d["article_id"] == article_id:
				for key, value in data_edit.items():
					d[key] = value
				time = datetime.datetime.utcnow()
				d["last_update"] = str(time)
				save_data(data)
				res = {"OK": "Données modifées avec succès"}, 200
				return res
		else : 
			res = {"ERROR": "Article non trouvé"}, 404


	@token_required
	def delete(self, current_user):
		"""Supprime des données"""

		# On va chercher les données déjà existantes
		data = get_data()

		# On recupère l'article_id pour connaître l'élément à supprimer
		article_id = request.args.get('article_id')

		# On cherche l'élément correspondant à l'article_id
		# Si on le trouve alors on le supprime,
		# Sinon on retourne un erreur
		for n, d in enumerate(data["contributions"]["data"]):
			if d["article_id"] == article_id:
				del data["contributions"]["data"][n]
				save_data(data)
				res = {"OK": "Article supprimé avec succés"}, 200
				return res
		else:
			res = {"ERROR": "Article non trouvé"}, 404
			return res


api.add_resource(Login, "/", "/login")
api.add_resource(Data, "/data","/data/<string:contrib_name>", "/data/<string:contrib_name>/<string:public_id>")

if __name__ == '__main__':
	app.run(debug=True)
