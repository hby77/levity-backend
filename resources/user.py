from flask import request, session, jsonify, make_response
from flask_restful import Resource
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_bcrypt import Bcrypt
import os

bcrypt = Bcrypt()

SALT_ROUNDS = os.environ.get('SALT_ROUNDS')

class Users(Resource):
  def get(self):
    users = User.objects()
    return make_response(jsonify(users), 200)
  

  def post(self):
    body = request.get_json()
    email = User.objects(email=body.get("email")).first()
    count = User.objects.count()
    if email or count == 1:
        return {"message": "Email already exists or max users"}, 500
    hashed = bcrypt.generate_password_hash(
    body.get("password"), int(SALT_ROUNDS))
    user = User()
    user.email = body.get("email")
    user.password = hashed
    user.save()
    return {"message": "User created"}, 200


class SignUp(Resource):
  def post(self):
    body = request.get_json()
    email = User.objects(email=body.get("email")).first()
    if email:
      return {"message": "Email already exists"}, 500
    hashed = bcrypt.generate_password_hash(
      body.get("password"), int(SALT_ROUNDS))
    user = User()
    user.email = body.get("email")
    user.password = hashed
    user.save()
    return {"message": "User created"}, 200
    

class SignIn(Resource):
  def post(self):
    body = request.get_json()
    user = User.objects(email=body.get("email")).first()
    if user:
      if bcrypt.check_password_hash(user["password"], body.get("password")):
        session['email'] = body.get('email')
        access_token = create_access_token(identity=body.get("email"))
        return make_response(jsonify(access_token=access_token, user=user, message="User logged in"), 200)
      return {"message": "Email & Password combination is wrong"}, 500
    return {"message": "User does not exist"}, 500
  

class Logout(Resource):
  def post(self):
    session.pop("email", None)
    return {"message": "User logged out"}
  

class CheckSession(Resource):
  @jwt_required()
  def get(self):
    current_user = get_jwt_identity()
    user = User.objects(email=current_user).first()
    if user:
      return make_response(jsonify(user), 200)
    return {"message": "User not authenticated"}, 404
