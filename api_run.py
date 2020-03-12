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


def get_users(filename="LISTE_COLLABORATEURS.json"):
	"""Lit le fichier contenant les données des utilisateurs et créé leurs identifants"""
	with open(os.path.join("data", filename), "r", encoding="utf8") as data_file:
		data = json.load(data_file)
	users = []
	for user in data.values():
		user = User(user["id"], user["nom"], generate_password_hash(user["prenom"]))
		users.append(user)
	return users
	# [User("cepty_001", "Bernard", "*******"), etc.]

users = get_users()


key = 'ceptyconsultant'
# key = "\xd5PE\xa3t\x96D\xa2\xae\xc2\xcfIq\xe7\xefk"

def make_token(user):
		"""Génère le Auth Token """
		encode_params = { 
			"id": user.id,
			"exp": datetime.datetime.utcnow()+\
			datetime.timedelta(minutes=30)
		}
		try:
			token = jwt.encode(encode_params, key, algorithm='HS256')
			# print("token generated")
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
			#print(current_user)
		except:
			return {'message': 'token invalide'}
		return f(current_user, *args, **kwargs)
	return decorator



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


#=========================================================================

class Login(Resource):
	"""Login"""
	def post(self):
		info = request.json
		user = verify_password(info["username"],info["password"])
		if user:
			token = make_token(user)
			#print(token)
			return {'User':user.to_json(), 'Token': token.decode('UTF-8')}
			#return redirect("/data", code=302)
		else:
			return {"ERREUR":"Username ou mot de passe incorrect!"}, 400


class Data(Resource):
	"""Retourne le contenu du fichier json"""
	@token_required
	def get(self, current_user, contrib_name=None, public_id=None):
		data = get_data()
		result = []

		# user_search = request.args.get('user_search')
		# if user_search:
		# 	for d in data["contributions"]["data"]:
		# 		if d["user_name"] == user_search: 
		# 			result.append(d)
		# 	res = {"data":result}, 200



		if public_id==None and contrib_name==None:
			result = data["contributions"]["data"]
			res = {"data":result}, 200
		
		if public_id==None and contrib_name!=None:
			for d in data["contributions"]["data"]:
				if d["contrib_name"] == contrib_name: 
					result.append(d)
			if len(result) == 0:
				res = {"ERROR":"contrib_name introuvable"}, 404
			else : res = {"data":result}, 200

		if public_id!=None and contrib_name!=None:
			for d in data["contributions"]["data"]:
				if d["contrib_name"] == contrib_name and d["public_id"] == public_id: 
					result.append(d)
			if len(result) == 0:
				res = {"ERROR":"contrib_name ou public_id introuvable"}, 404
			else : res = {"data":result}, 200
		
		return res


	@token_required
	def put(self, current_user):
		data = get_data()
		data_add = request.json
		# TODO Ajouter des conditions pour vérifier que les données entrées
		# ne rentrent pas en conflit avec les données du fichier json
		# Actuellement la seule condition est l'article_id
		list_id = [d["article_id"] for d in data["contributions"]["data"]]
		if data_add["article_id"] in list_id:
			res = {"ERROR": "article_id existe déjà"}, 400
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
		print("TTTTTTTTTTTTTTTTESSSSSSSSSST")
		data = get_data()
		print("TTTTTTTTTTTTTTTTESSSSSSSSSST")
		data_edit = request.json
		print(data_edit)
		article_id = request.args.get('article_id')
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
		data = get_data()
		article_id = request.args.get('article_id')
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
