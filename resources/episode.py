from flask import request, session, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from models.episode import Episode
from models.user import User


class Episodes(Resource):
  def get(self):
    episodes = Episode.objects()
    return make_response(jsonify(episodes), 200)

  @jwt_required()
  def post(self):
    current_user = get_jwt_identity()
    user = User.objects(email=current_user).first()
    body = request.get_json()
    episode = Episode.objects(title=body.get("title")).first()
    if episode:
      return {"msg": "Episode title already in use"}
    if user:
      Episode(**body).save()
      return {"msg": "Episode created"}
  
class SingleEpisode(Resource):
  def get(self, id):
    episode = Episode.objects(id=id).first()
    if episode:
      return make_response(jsonify(episode), 200)
    return {"msg": "Episode doesn't exist"}
    
  @jwt_required()
  def put(self, id):
    current_user = get_jwt_identity()
    user = User.objects(email=current_user).first()
    episode = Episode.objects(id=id).first()
    if user and episode:
      body = request.get_json()
      episode.update(**body)
      return {"msg": "Episode updated"}
    return {"msg": "Episode doesn't exist"}
    
  @jwt_required()
  def delete(self, id):
    current_user = get_jwt_identity()
    user = User.objects(email=current_user).first()
    episode = Episode.objects(id=id).first()
    if user and episode:
      episode.delete()
      return {"msg": "Episode deleted"}
    return {"msg": "Episode doesn't exist"}
    
class EpisodeLikes(Resource):
  def put(self, id):
    episode = Episode.objects(id=id).first()
    if episode:
      episode.likes += 1
      episode.save()
      return {"msg": "Episode likes updated"}
    return {"msg": "Episode doesn't exist"}

class EpisodeTracks(Resource):
  def put(self, id):
    episode = Episode.objects(id=id).first()
    if episode:
      body = request.get_json()
      episode.track.append(body.get(''))