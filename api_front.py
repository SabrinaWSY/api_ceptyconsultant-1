# coding: utf-8
from flask import Flask, request, json, jsonify, request, Response, make_response, abort, redirect, render_template, after_this_request
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
		return resp

	def post(self):

		info = request.form
		user_id = {"username":info["username"], "password":info["password"]}
		
		r = requests.post(api_backend + '/login', json=user_id, verify=False)
		
		token = r.json()["Token"]

		global current_user
		current_user = r.json()["User"]
		
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
		# params={
		# 	"username":current_user["username"]
		# }
		
		data = r.json()["data"]
		render_data = render_template(
			"data.html",
			username="Mikolov",
			data=data
		)
		resp = Response(render_data, status=200, content_type="text/html")

		# resp = r.json()
		return resp
		
	def post(self):

		auth = _check_cookie_auth()
		if auth == None:
			abort(403)
		headers = { 'x-access-tokens' : auth }


		data_add = request.form
		data_set = {
			"article_id":data_add["article_id"],
			"contrib_data":data_add["contrib_data"],
			"contrib_name":data_add["contrib_name"],
			"contrib_path":data_add["contrib_path"],
			"contrib_type":data_add["contrib_type"],
			"dico_id":data_add["dico_id"],
			"last_update":data_add["last_update"],
			"ntealan":data_add["ntealan"],
			"public_id":data_add["public_id"],
			"user_id":data_add["user_id"],
			"user_name":data_add["user_name"],
			"validate":data_add["validate"]
		}

		r = requests.put(api_backend + '/data', json=data_set, headers=headers, verify=False)
		
		resp = redirect('/data')
		return resp




api.add_resource(Login, "/", "/login")
api.add_resource(Data, "/data",
"/data/<string:contrib_name>",
"/data/<string:contrib_name>/<string:public_id>")



if __name__ == '__main__':
	app.run(debug=True)