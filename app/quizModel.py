from main import db
import json
import datetime

class QuizModel(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    passMark = db.Column(db.Integer, nullable=False)
    timeInSeconds = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updatedAt = db.Column(db.String(120), nullable=True)
    questions = db.Column(db.JSON, nullable=False)

    # CREATE Quiz to DB
    def createQuiz(self):
        db.session.add(self)
        db.session.commit()
        return True

    # READ quiz by ID
    @classmethod
    def fetchQuiz(cls, id):
        quiz = QuizModel.query.filter_by(id=id).first()
        quizQ = {'data':{'id':quiz.id, 'title':quiz.title, 'description':quiz.description, 'passMark':quiz.passMark, 'timeInSeconds':quiz.timeInSeconds, 'createdAt':str(quiz.createdAt), 'updatedAt': str(quiz.updatedAt), 'questions':quiz.questions }}

        return quizQ

    # READ Quiz from DB
    @classmethod
    def fetchQuizzes(cls):
        quizes = QuizModel.query.all()
        def to_json(x):
            return {
                'id': x.id,
                'title': x.title,
                'description': x.description,
                'passMark': x.passMark,
                'timeInSeconds': x.timeInSeconds,
                'createdAt': str(x.createdAt),
                'updatedAt': str(x.updatedAt),
                'questions': str(x.questions)
            }
        return {'data': list(map(lambda x:to_json(x), quizes))}

    #UPDATE Quiz
    @classmethod
    def updateQuiz(cls, id, newTitle, newDescription, newPassMark, newTimeInSeconds, newQuestions, newUpdatedAt):
        quiz = QuizModel.query.filter_by(id=id).first()
        if quiz:
            quiz.title = newTitle
            quiz.description = newDescription
            quiz.passMark = newPassMark
            quiz.timeInSeconds = newTimeInSeconds
            quiz.updatedAt = newUpdatedAt
            quiz.questions = newQuestions
            db.session.commit()
            return True
        else:
            return False

    # Delete Quiz
    @classmethod
    def deleteQuiz(cls, id):
        quiz = QuizModel.query.filter_by(id=id)
        if quiz.first():
            quiz.delete()
            db.session.commit()
            return True
        else:
            return False


class QuizUserModel(db.Model):
    __tablename__ = 'quiz_user'
    id = db.Column(db.Integer, primary_key=True)
    quizId = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    quiz = db.relationship(QuizModel)
    courseId = db.Column(db.Integer, nullable=True)
    bootcampId = db.Column(db.Integer, nullable=True)
    userMarks = db.Column(db.Integer, nullable=True)
    mobileNumber = db.Column(db.String(120), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    answers = db.Column(db.JSON, nullable=False)

    # CREATE QuizAnswers to DB
    def createQuizUser(self):
        db.session.add(self)
        db.session.commit()
        return True

    # READ QuizAnswers from DB
    @classmethod
    def fetchQuizUser(cls, quizId):
        quizUser = QuizUserModel.query.filter_by(quizId = quizId)

        def to_json(x):

            return {
                'id': x.id,
                'quizId': x.quizId,
                'bootcampId': x.bootcampId,
                'courseId': x.courseId,
                'userMarks': x.userMarks,
                'mobileNumber': x.mobileNumber,
                'createdAt': str(x.createdAt),
                'answers': x.answers
            }
        return {'data': list(map(lambda x:to_json(x), quizUser))}

    @classmethod
    def findQuizByMobileNumber(cls, quizId, mobileNumber, bootcampId, courseId):

        quizUser = QuizUserModel.query.filter_by(quizId=quizId, mobileNumber=mobileNumber, bootcampId=bootcampId, courseId=courseId)
        if quizUser.first():
            return True
        else:
            return False