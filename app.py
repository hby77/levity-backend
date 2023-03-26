from models.db import db
from flask import Flask
from flask_session import Session
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
import os
from resources.user import Users, SignIn
from resources.episode import Episodes, SingleEpisode

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')

app = Flask(__name__)

app.config["MONGO_URI"] = MONGO_URI
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

CORS(app)
Session(app)
api = Api(app)

db.init_app(app)

api.add_resource(Users, '/users')
api.add_resource(SignIn, '/signin')
api.add_resource(Episodes, '/episodes')
api.add_resource(SingleEpisode, '/single_episode/<id>')

if __name__ == '__main__':
    app.run(debug=True)
