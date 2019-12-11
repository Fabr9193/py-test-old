from flask import Flask, request
import firebase_admin, json
from config import *
from models import User
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Init
cred = credentials.Certificate(DB_CERT)
firebase_admin.initialize_app(cred)
db = firestore.client()


# methods
def authenticate(username):
    user = User(username)
    try: 
        db.collection('users').add(user.__dict__)
        return json.dumps(
            {
                "message" : 'Welcome ' + user.name + '! Your token is ' + user.token
            }) , 200
    except Exception as e:
        return json.dumps(
            {
                "message" : 'Error',
                "error" :  e
            }) 



def group_associate(element_type, token):
    users = db.collection('users')
    groups = db.collection('groups')
    try:
        group = groups.where('type', '==', element_type).getRef()
        user = users.where('token', '==', token).getRef().push
        user.set(
            {'groups': group}, merge=True)
        return json.dumps(
            {
                "message" : 'Success'
            }) , 200
    except Exception as e:
         return json.dumps (
            {
                "message" : 'Error',
                "error" :  e
            }) 

def group_remove(element_type, token):
    users = db.collection('users')
    groups = db.collection('groups')
    try:
        group = groups.where('type', '==', element_type).getRef()
        user = users.where('token', '==', token).getRef().push
        user.delete(
            {'groups': group})
        return json.dumps(
            {
                "message" : 'Success'
            }) , 200
    except Exception as e:
         return json.dumps (
            {
                "message" : 'Error',
                "error" :  e
            }) 

    


# Routes 


@app.route('/')
def hello():
    return "Hello World!"

@app.route('/api/login', methods=['POST'])
def login():
    user = request.args['user']
    return authenticate(user)

@app.route('/api/group/<element_type>/add', methods=['POST'])
def associate(element_type=None):
    token = request.args['token']
    return user_associate(element_type, token)

@app.route('/api/group/<element_type>/remove', methods=['POST'])
def remove(elment_type=None):
    token = request.args['token']
    return User.remove(element_type, token)

@app.route('/api/user/me')
def show():
    token = request.args['token']
    return User.show(token)
    
if __name__ == '__main__':
    app.run()