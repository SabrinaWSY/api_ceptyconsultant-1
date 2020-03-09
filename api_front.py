# coding: utf-8
from flask import Flask, request, json, jsonify, request, Response, make_response, abort, redirect, render_template, after_this_request
from flask_restful import Resource, Api
import json
import requests

app = Flask(__name__)
api = Api(app)

api_backend = "https://api.ceptyconsultant.localhost"
current_user = {}

def _check_cookie_auth():
	token = request.cookies.get('token')
	print("TTTT",token)
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
		
		render_data = render_template("data.html")
		resp = Response(render_data, status=200, content_type="text/html")

		# resp = r.json()
		return resp
		


api.add_resource(Login, "/", "/login")
api.add_resource(Data, "/data",
"/data/<string:contrib_name>",
"/data/<string:contrib_name>/<string:public_id>")



if __name__ == '__main__':
	app.run(debug=True)