# coding: utf-8
from flask import Flask, request, json, jsonify, request, Response, make_response, abort, redirect, render_template, url_for
from flask_restful import Resource, Api
import json
import requests

app = Flask(__name__)
api = Api(app)

api_backend = "https://api.ceptyconsultant.localhost"



def _check_cookie_auth():
	token = request.cookies.get('token')
	return token

class Login(Resource):
	"""Login"""

	def get(self):
		render_login = render_template("login.html")
		resp = Response(render_login, status=200, content_type="text/html")
		auth = _check_cookie_auth()
		if auth != None:
			resp.delete_cookie('token', domain="ceptyconsultant.localhost")
		return resp

	def post(self):

		info = request.form
		user_id = {"username":info["username"], "password":info["password"]}
		
		r = requests.post(api_backend + '/login', json=user_id, verify=False)
		
		token = r.json()["Token"]

		#global current_user
		# current_user = r.json()["User"]
		current_user="Mikolov"
		
		resp = redirect('/data')
		resp.set_cookie("token", token, domain="ceptyconsultant.localhost")

		return resp

class Data(Resource):

	def get(self, contrib_name=None, public_id=None):
		auth = _check_cookie_auth()
		if auth == None:
			abort(403)

		headers = { 'x-access-tokens' : auth }
		# if "username" in current_user:
		# 	param = "?user_search=" + current_user["username"]
		if public_id==None and contrib_name==None:
			r = requests.get(api_backend + "/data", headers=headers, verify=False)
		if public_id==None and contrib_name!=None:
			r = requests.get(api_backend + "/data/" + contrib_name, headers=headers, verify=False)
		if public_id!=None and contrib_name!=None:
			r = requests.get(api_backend + "/data/" + contrib_name + "/" + public_id, headers=headers, verify=False)
		
		# global current_user
		# print(current_user)

		#username = current_user["username"]
		username = "Mikolov"
		
		data_get = r.json()
		if "data" in data_get:
			data = data_get["data"]
			render_data = render_template(
				"data.html",
				current_user=username,
				data=data,
				visibility={}
			)
			resp = Response(render_data, status=200, content_type="text/html")
			return resp
		
		else :
			abort(404)
		
		
	def post(self):
		print("post")
		auth = _check_cookie_auth()
		if auth == None:
			abort(403)
		
		data_form = request.form

		if data_form['action'] == 'delete':
			article_id = data_form["article_id"]
			headers = { 'x-access-tokens' : auth }
			r = requests.delete(api_backend + '/data?article_id=' + article_id, headers=headers, verify=False)
			# resp = redirect('/data')
			# return resp
			render_response = render_template("response.html", message="Données supprimées avec succès!", alert="success")
			resp = Response(render_response, status=200, content_type="text/html")
			return resp
		
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

			headers = { 'x-access-tokens' : auth }
			r = requests.post(api_backend + '/data?article_id=' + article_id, json=data_set_1, headers=headers, verify=False)
			
			render_response = render_template("response.html", message="Données modifiées avec succès!", alert="success")
			resp = Response(render_response, status=200, content_type="text/html")
			return resp

		elif data_form['action'] == 'add':
			
			data_set = {
				"article_id":data_form["article_id"],
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
			headers = { 'x-access-tokens' : auth }
			r = requests.put(api_backend + '/data', json=data_set, headers=headers, verify=False)
			render_response = render_template("response.html", message="Données ajoutées avec succès!", alert="success")
			resp = Response(render_response, status=200, content_type="text/html")
			return resp
		
		elif data_form['action'] == 'search':
			headers = { 'x-access-tokens' : auth }
			contrib_name  = data_form['contrib_name']
			if data_form['public_id'] == '' : public_id = None
			else : public_id  = data_form['public_id']
			print(contrib_name, public_id)
			resp = redirect(url_for('data', contrib_name=contrib_name, public_id=public_id))
			return resp


class Licence(Resource):
	def get(self):
		auth = _check_cookie_auth()
		if auth == None:
			abort(403)

		headers = { 'x-access-tokens' : auth }
		render_licence = render_template("licence.html")
		resp = Response(render_licence, status=200, content_type="text/html")
		return resp


api.add_resource(Login, "/", "/login")
api.add_resource(Licence, "/licence")
api.add_resource(Data, "/data", "/data/<string:contrib_name>",
"/data/<string:contrib_name>/<string:public_id>")



if __name__ == '__main__':
	app.run(debug=True)