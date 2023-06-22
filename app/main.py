# from ast import Param
from tokenize import Single
import json
import configparser

from flask import Flask, render_template,jsonify
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPBasicAuth
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2





app = Flask(__name__, template_folder='./templates')
api = Api(app, prefix="/api/v1")

class Routing(Resource):
    # @auth.login_required
    def get(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('list_id', required=True, type=int)  # add locationId arg
        args = parser.parse_args()  # parse arguments to dictionary
        listId = args['list_id']
        return {"res":listId}, 200


api.add_resource(Routing, '/timerouting')


if __name__ == "__main__":
    host = '127.0.0.1'  # Listen on all network interfaces
    port = 8043
    app.run(host=host, port=port,debug=True)

