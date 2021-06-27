import os
import json
from flask import Flask, jsonify, request
import csv

from id_utils.cognito_handler import CognitoHandler

app = Flask(__name__)
id_handler = CognitoHandler()

@app.route('/users/signup', methods=['POST'])
def signup_user():
    data = request.get_json()
    return id_handler.signupUser(data['username'], data['password'], data['email'])

@app.route('/users/confirm', methods=['PUT'])
def confirm_user():
    data = request.get_json()
    return id_handler.confirmUser(data['username'], data['confirmation_code'])

@app.route('/users/get-all', methods=['GET'])
def get_all_users():
    return id_handler.listAllUsers()

@app.route('/users/search/<string:username>', methods=['GET'])
def search_by_username(username):
    return id_handler.searchByUserName(username)

@app.route('/users/login', methods=['PUT'])
def login():
    data = request.get_json()
    return id_handler.logIn(data['username'], data['password'])

@app.route('/users/update', methods=['PUT'])
def update_user():
    data = request.get_json()
    return id_handler.updateUser(data['access_token'], data['attributes'])

@app.route('/users/forget-pwd', methods=['PUT'])
def forget_password():
    data = request.get_json()
    return id_handler.forgetPassword(data['username'])

@app.route('/users/confirm-pwd', methods=['PUT'])
def confirm_password():
    data = request.get_json()
    return id_handler.confirmForgetPassword(data['username'], data['verification_code'], data['new_pwd'])

@app.route('/users/delete', methods=['PUT'])
def delete_user():
    data = request.get_json()
    return id_handler.deleteUser(data['access_token'])

@app.route('/users/signup-batch', methods=['POST'])
def signup_batch():
    data = request.get_json()
    users = data['users']
    resp_codes = []
    for user in users:
        response = id_handler.signupUser(user['username'], user['password'], user['email'])
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        resp_codes.append({user['username']:str(status_code)})
    return jsonify({"HTTPStatusCodes":json.dumps(resp_codes)})

# We only need this for local development.
if __name__ == '__main__':
    app.run()
