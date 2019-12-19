from flask import Flask, jsonify, make_response
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# DB_URL = 'postgres://postgres:root@127.0.0.1:5433/techcamp_quiz'
DB_URL = 'postgres://postgres:123456@172.17.0.1:5433/techcamp_quiz'

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'
db = SQLAlchemy(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_SECRET_KEY'] = 'quiz-tech'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

api = Api(app)
import resources, userModel

@app.before_first_request
def createTables():
    db.create_all()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return userModel.RevokedTokenModel.isJtiBlacklisted(jti)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found!'}), 404)

api.add_resource(resources.Homepage, '/')
api.add_resource(resources.Quizzes, '/quizzes')
api.add_resource(resources.Quiz, '/quiz/<int:id>')
api.add_resource(resources.UserQuiz, '/quiz/answers')
api.add_resource(resources.UserQuizResponse, '/quiz/response/<int:quizId>')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserRegistration, '/register')
api.add_resource(resources.UserLogoutAccess, '/logout')


#
# if __name__ == '__main__':
#     app.run(debug=True)
