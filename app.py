from flask_jwt_extended import JWTManager
from resources.episode import Episodes, SingleEpisode, EpisodeLikes
from resources.user import Users, SignIn, SignUp, Logout
from flask_session import Session
from dotenv import load_dotenv
from flask_restful import Api
from flask_cors import CORS
from models.db import db
from flask import Flask
import datetime
import os

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
MONGO_URI = os.environ.get('MONGO_URI')

app = Flask(__name__)

app.config["MONGO_URI"] = MONGO_URI
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

CORS(app)
Session(app)
JWTManager(app)
api = Api(app)
db.init_app(app)

api.add_resource(Users, '/users')
api.add_resource(SignIn, '/signin')
api.add_resource(SignUp, '/signup')
api.add_resource(Logout, '/logout')
api.add_resource(Episodes, '/episodes')
api.add_resource(EpisodeLikes, '/episodes_likes/<id>')
api.add_resource(SingleEpisode, '/single_episode/<id>')

if __name__ == '__main__':
    app.run(debug=True)
