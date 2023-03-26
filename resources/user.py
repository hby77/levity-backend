from flask import request, jsonify, make_response
from flask_restful import Resource
from models.user import User


class Users(Resource):
  def get(self):
    users = User.objects()
    return make_response(jsonify(users), 200)
  
  def post(self):
    body = request.get_json()
    email = User.objects(email=body.get("email")).first()
    count = User.objects.count()
    if email or count == 1:
      return {"msg": "Email already in use or max users"}
    User(**body).save()
    return {"msg": "Account created"}, 200