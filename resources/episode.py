from flask import request, session, jsonify, make_response
from flask_restful import Resource
from models.episode import Episode


class Episodes(Resource):
  def get(self):
    episodes = Episode.objects()
    return make_response(jsonify(episodes), 200)

  def post(self):
    body = request.get_json()
    episode = Episode.objects(title=body.get("title")).first()
    if episode:
      return {"msg": "Episode title already in use"}
    Episode(**body).save()
    return {"msg": "Episode created"}
  
class SingleEpisode(Resource):
    def get(self, id):
      episode = Episode.objects(id=id).first()
      if episode:
        return make_response(jsonify(episode), 200)
      return {"msg": "Episode doesn't exist"}
    
    def put(self, id):
      episode = Episode.objects(id=id).first()
      if episode:
        body = request.get_json()
        episode.update(**body)
        return {"msg": "Episode updated"}
      return {"msg": "Episode doesn't exist"}
    
    def delete(self, id):
      episode = Episode.objects(id=id).first()
      if episode:
        episode.delete()
        return {"msg": "Episode deleted"}
      return {"msg": "Episode doesn't exist"}
