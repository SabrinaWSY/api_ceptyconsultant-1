# coding: utf-8
from flask import Flask, request, json, jsonify, Response, redirect, render_template
from flask_restful import Resource, Api
import json
import requests

app = Flask(__name__)
api = Api(app)

api_backend = "https://api.ceptyconsultant.localhost"

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
		token = r.json()
		print(token)
		if "Token" in r.json():
			return redirect("/data", code=302)
		else:
		 	return redirect("/login", code=302)
		# except :
		# 	# token = r.json()["Token"]
		# 	# headers = { 'x-access-tokens' : token}
		# 	return redirect("/login", code=302)

class Data(Resource):
	def get(self, contrib_name=None, public_id=None):
		r = requests.get(api_backend + "/data", verify=False)
		return {"test":"test"}

api.add_resource(Login, "/", "/login")
api.add_resource(Data, "/data","/data/<string:contrib_name>", "/data/<string:contrib_name>/<string:public_id>")



if __name__ == '__main__':
	app.run(debug=True)