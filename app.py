from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models import db, User
from flask_migrate import Migrate
import os



app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mystore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.json.compact=False
app.config['JWT_SECRET_KEY']=os.urandom(32).hex()

migrate=Migrate(app, db)
api=Api(app)
cors=CORS(app)
jwt=JWTManager(app)
db.init_app(app)


class Index(Resource):
    def get(self):
        return make_response(jsonify({'message':'Welcome to mystore APi'}), 200)
    
api.add_resource(Index, '/')

class UserRegister(Resource):
    def post(self):
        data=request.json

        new_user=User(
            full_name=data['full_name'],
            email=data['email']
        )

        db.session.add(new_user)
        db.session.commit()

        access_token=create_access_token(identity='email')

        user_data={
            "id":new_user.id,
            "full_name":new_user.full_name,
            "email":new_user.email,
            "access_token":access_token
        }
        response=make_response(jsonify(user_data), 201)
        return response
api.add_resource(UserRegister, '/register')

class UserLogIn(Resource):
    def post(self):
        data=request.json
        email=data['email']
        user=User.query.filter_by(email=email).first()
        if user:
            access_token=create_access_token(identity='email')
            user_data={
                "id":user.id,
                "full_name":user.full_name,
                "email":user.email,
                "access_token":access_token
            }
            response=make_response(jsonify(user_data), 200)
            return response
        else:
            return make_response(jsonify({'error':'Invalid email or password'}), 401)
        
api.add_resource(UserLogIn, '/login')
        


if __name__== '__main__':
    app.run(port=5555, debug=True)