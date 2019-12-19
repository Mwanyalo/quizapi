from flask import request
from flask_restful import Resource
import datetime
from quizModel import *
from userModel import *
from flask_jwt_extended import (create_access_token,
                                jwt_required,
                                get_jwt_identity,
                                get_raw_jwt)

## User Authentication Class and Methods ##

class UserRegistration(Resource):
    def post(self):
        if request.is_json:
            try:
                fullName = request.get_json()['fullName']
                email = request.get_json()['email']
                password = request.get_json()['password']
            except Exception as e:
                return {"Message": "Some field is empty"}, 400
        else:
            return {"Message": "Request body is null/not JSON"}, 400

        if UserModel.findByEmail(email):
            return {"Message":"Email {} already registered".format(email)}, 409
        else:
            try:
                user = UserModel(fullName=fullName, email=email, password=UserModel.generateHash(password))
                user.createUser()
                accessToken = create_access_token(identity=email)

                return {'message': 'User {} was created'.format(fullName),
                        'token': accessToken
                     },201
            except Exception as e:
                return {"Message":"Unable to create user"}, 500

class UserLogin(Resource):
    def post(self):
        if request.is_json:
            try:
                email = request.get_json()['email']
                password = request.get_json()['password']
            except KeyError:
                return {"Message": "Some field is empty"}, 400
        else:
            return {"Message": "Request body is null/not JSON"}, 400

        currentUser = UserModel.findByEmail(email)
        if not currentUser:
            return {"Message":"User {} doesnt exist".format(email)},400
        if UserModel.verifyHash(password,currentUser.password):
            accessToken = create_access_token(identity=email)
            return {
            'message': 'User {} Logged in Successfully'.format(email),
            'token': accessToken },200
        else:
            return {'message': 'Wrong credentials'},403

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'},200
        except:
            return {'message': 'Something went wrong'}, 500


## User Quiz Class and Methods ##

class Homepage(Resource):
    def get(self):
        return {'message': 'This is a private API!'}, 200

    def post(self):
        return {'message': 'This is a private API!'}, 200

class Quiz(Resource):
    def get(self,id):
        quiz = QuizModel.fetchQuiz(id=id)
        return quiz

    @jwt_required
    def put(self,id):
        if request.is_json:
            data = request.get_json()
            title = data['title']
            description = data['description']
            passMark = data['passMark']
            timeInSeconds =data['timeInSeconds']
            updatedAt = datetime.datetime.now(),
            questions = data['questions']

            quiz = QuizModel.updateQuiz(id=id, newTitle=title, newDescription=description, newPassMark=passMark, newTimeInSeconds=timeInSeconds, newQuestions=questions, newUpdatedAt=updatedAt)

            return {'message': 'Quiz {} saved successfully'.format(title)}, 200
        else:
            return {'message': 'Json format is wrong'}, 400

    @jwt_required
    def delete(self, id):
        if request.is_json:
            quiz = QuizModel.deleteQuiz(id=id)
            return {'message': 'Quiz deleted successfully'}, 200
        else:
            return {'message': 'Quiz not deleted'}, 400

class Quizzes(Resource):
    @jwt_required
    def post(self):
        if request.is_json:
            data = request.get_json()
            title = data['title']
            description = data['description']
            passMark = data['passMark']
            timeInSeconds = data['timeInSeconds']
            questions = data['questions']
            updatedAt = data['updatedAt']

            quiz = QuizModel(title=title, description=description, passMark=passMark, timeInSeconds=timeInSeconds, questions=questions, updatedAt=updatedAt)
            quiz.createQuiz()

            return {'message':'Quiz {} saved successfully'.format(title)}, 200
        else:
            return {'message':'Json format is wrong'}, 400

    @jwt_required
    def get(self):
        quizzes = QuizModel.fetchQuizzes()
        return quizzes

class UserQuiz(Resource):
    def post(self):
        if request.is_json:
            data = request.get_json()
            quizId = data['quizId']
            courseId = data['courseId']
            bootcampId = data['bootcampId']
            userMarks = data['userMarks']
            mobileNumber = data['mobileNumber']
            answers = data['answers']

            quizUser = QuizUserModel(quizId=quizId, bootcampId=bootcampId, courseId=courseId, userMarks=userMarks, mobileNumber=mobileNumber, answers=answers)
            quizUser.createQuizUser()

            return {'message':'Answer {} saved successfully'.format(mobileNumber)}, 200
        else:
            return {'message':'Json format is wrong'}, 400

    def get(self):
        quizUser = QuizUserModel.fetchQuizUser()
        return quizUser

class UserQuizResponse(Resource):
    def get(self, quizId):
        quizUser = QuizUserModel.fetchQuizUser(quizId=quizId)
        return quizUser

    def post(self, quizId):
        if request.is_json:
            data = request.get_json()
            mobileNumber = data['mobileNumber']
            bootcampId = data['bootcampId']
            courseId = data['courseId']
            quiz = QuizUserModel.findQuizByMobileNumber(quizId=quizId, mobileNumber=str(mobileNumber), bootcampId=bootcampId, courseId=courseId)
            if quiz:
                return True
            else:
                return False
        else:
            return {'message': 'Json format is wrong'}, 400








