# coding: utf-8
from flask import Flask, request, json, jsonify, request, Response, make_response, abort, redirect, render_template, url_for
from flask_restful import Resource, Api
import json
import requests

app = Flask(__name__)
api = Api(app)

# URL de notre application backend
api_backend = "https://api.ceptyconsultant.localhost"


def _check_cookie_auth():
	"""Recupère le token stocké dans le cookie"""
	token = request.cookies.get('token')
	return token

def _login_error():
	""" Renvoie la page login_error.html """
	render_response = render_template("login_error.html", message="Vous n'êtes pas connecté(e) !")
	resp = Response(render_response, status=403, content_type="text/html")
	return resp


class Login(Resource):
	"""Login"""

	def get(self):
		"""Envoie le formulaire à remplir pour se connecter.
		Si il y a un token dans le cookie alors il est supprimée. 
		Ceci permet de gérer la déconnexion automatique lorsqu'on recharge la page de login
		ou lorsque qu'une redirection est effectuée"""
		render_login = render_template("login.html")
		resp = Response(render_login, status=200, content_type="text/html")
		
		# S'il n'y a pas de token alors le client n'est pas connecté
		if _check_cookie_auth() != None:
			resp.delete_cookie('token', domain="ceptyconsultant.localhost")
		return resp

	def post(self):
		"""Récupére les informations du formulaire de login et envoie une requête post
		au backend qui renvoie le token, le stock dans un cookie puis redirige vers les données.
		Si les identifiants sont incorrects alors une erreur est renvoyée"""
		info = request.form
		user_id = {"username":info["username"], "password":info["password"]}
		r = requests.post(api_backend + '/login', json=user_id, verify=False)


		# Si les identifiants sont corrects, on enregistre le token dans un cookie 
		# puis on redirige vers les données :
		if "Token" in r.json():
			token = r.json()["Token"]
			resp = redirect('/data')
			resp.set_cookie("token", token, domain="ceptyconsultant.localhost")
			return resp

		# Si les identifiants sont incorrects :
		elif r.json()["ERROR"] == "Username ou mot de passe incorrect!":
			render_response = render_template("login_error.html", message="Identifiant ou mot de passe incorrect !")
			resp = Response(render_response, status=403, content_type="text/html")
			return resp
		


class Data(Resource):
	"""Gére les accès et les recherches des données"""

	def get(self, contrib_name=None, public_id=None):
		"""Affiche et filtre les données"""
		
		# On vérifié que le client est bien connecté grâce à la présence du token dans le cookie
		# Sinon on redirige vers une page d'erreur
		token = _check_cookie_auth()
		if token == None:
			return _login_error()


		# On prépare le header pour l'envoie de la requête au serveur
		headers = { 'x-access-tokens' : token }

		# Fitre les données à afficher en fonction de la l'url envoyée
		# Renvoie toutes les données :
		if public_id==None and contrib_name==None:
			r = requests.get(api_backend + "/data", headers=headers, verify=False)
		# Filtre les données par contrib_name :
		if public_id==None and contrib_name!=None:
			r = requests.get(api_backend + "/data/" + contrib_name, headers=headers, verify=False)
		# Filtre les données par contrib_name et public_id
		if public_id!=None and contrib_name!=None:
			r = requests.get(api_backend + "/data/" + contrib_name + "/" + public_id, headers=headers, verify=False)

		# Récupère le contenu de la réponse de la requête
		data_get = r.json()
		# Si des données ont bien été trouvées on les affiches 
		if "data" in data_get:
			data = data_get["data"]
			render_data = render_template("data.html", data=data)
			resp = Response(render_data, status=200, content_type="text/html")
			return resp

		# Si aucune donnée n'a été trouvée alors on prévient le client
		elif data_get['ERROR'] == "aucune  données n'a été trouvée":
			render_data = render_template("response.html", message="Aucune donnée n'a été trouvée.", alert="warning")
			resp = Response(render_data, status=404, content_type="text/html")
			return resp
		

		
		
	def post(self, contrib_name=None, public_id=None):
		"""Gère l'ajout, la modification et la suppression des données"""
		
		# On vérifié que le client est bien connecté grâce à la présence du token dans le cookie
		# Sinon on redirige vers une page d'erreur
		token = _check_cookie_auth()
		if token == None:
			return _login_error()
		
		# On prépare le header pour la future requête
		headers = { 'x-access-tokens' : token }
		
		# On récupère le les données envoyées par le formulaire
		data_form = request.form

		# Si une suppresion est demandée on récupère l'article_id 
		# dans les données du formulaire puis et 
		# on supprime l'élément associé par la requête delete
		if data_form['action'] == 'delete':
			article_id = data_form["article_id"]
			r = requests.delete(api_backend + '/data?article_id=' + article_id, headers=headers, verify=False)
			render_response = render_template("response.html", message="Données supprimées avec succès !", alert="success")
			resp = Response(render_response, status=200, content_type="text/html")
			return resp
		
		# Si une modification est demandée on récupère les données à modifier
		# et l'article_id envoyés par le formulaire puis on effectue la modification
		# avec la méthode post
		elif data_form['action'] == 'edit':
			article_id = data_form["article_id"]
			data_set_1 = {
				"contrib_data":data_form["contrib_data"],
				"contrib_name":data_form["contrib_name"],
				"contrib_path":data_form["contrib_path"],
				"contrib_type":data_form["contrib_type"],
				"dico_id":data_form["dico_id"],
				"last_update":data_form["last_update"],
				"ntealan":data_form["ntealan"],
				"public_id":data_form["public_id"],
				"user_id":data_form["user_id"],
				"user_name":data_form["user_name"],
				"validate":data_form["validate"]
			}
			r = requests.post(api_backend + '/data?article_id=' + article_id, json=data_set_1, headers=headers, verify=False)
			render_response = render_template("response.html", message="Données modifiées avec succès !", alert="success")
			resp = Response(render_response, status=200, content_type="text/html")
			return resp

		# Si un ajout est demandé, on recupère les données envoyées par le formulaires 
		# et on créé le nouvel élément grâce à la méthode put
		elif data_form['action'] == 'add':
			data_set = {
				"article_id":data_form["article_id"],
				"contrib_data":data_form["contrib_data"],
				"contrib_name":data_form["contrib_name"],
				"contrib_path":data_form["contrib_path"],
				"contrib_type":data_form["contrib_type"],
				"dico_id":data_form["dico_id"],
				"ntealan":data_form["ntealan"],
				"public_id":data_form["public_id"],
				"user_id":data_form["user_id"],
				"user_name":data_form["user_name"],
				"validate":data_form["validate"]
			}
			r = requests.put(api_backend + '/data', json=data_set, headers=headers, verify=False)
			render_response = render_template("response.html", message="Données ajoutées avec succès !", alert="success")
			resp = Response(render_response, status=200, content_type="text/html")
			return resp
		
		# Si une recherche est demandée on redirige vers la méthode get de data 
		# avec une url personnalisée en fonction des données recherchées
		elif data_form['action'] == 'search':
			contrib_name  = data_form['contrib_name']
			if data_form['public_id'] == '' : public_id = None
			else : public_id  = data_form['public_id']
			resp = redirect(url_for('data', contrib_name=contrib_name, public_id=public_id))
			return resp


class License(Resource):
	"""Gère la page contenant la licence"""

	def get(self):
		# On vérifié que le client est bien connecté grâce à la présence du token dans le cookie
		# Sinon on redirige vers une page d'erreur
		token = _check_cookie_auth()
		if token == None:
			return _login_error()

		# On prépare le header pour la future requête
		headers = { 'x-access-tokens' : token }

		# On renvoie la page contenant la licence
		render_licence = render_template("license.html")
		resp = Response(render_licence, status=200, content_type="text/html")
		return resp


api.add_resource(Login, "/", "/login")
api.add_resource(License, "/license")
api.add_resource(Data, "/data", "/data/<string:contrib_name>",
"/data/<string:contrib_name>/<string:public_id>")



if __name__ == '__main__':
	app.run(debug=True)