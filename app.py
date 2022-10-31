from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4 as uuid
from datetime import datetime
from register.register_face_id import facial_register
from login.login_face_id import facial_log 

app = FastAPI()

users_faceid = []
users = []

class User(BaseModel):
    id: Optional[str]
    username: str
    password: str
    register_at: datetime = datetime.now()

@app.get('/')
def face_id_home():
    '''
    Path operation funtion, return a dict with all specifications
    '''
    return {"Register and Login": "Face ID - Function"}

@app.get('/users')
def get_users():
    '''
    Path operation funtion, return all users in a dictionary 
    '''
    return users

@app.post('/register')
def register(user: User):
    '''
    Path operation funtion,  allows traditional registration
    '''
    user.id = str(uuid())
    users.append(user)
    return (f"Hi {user.username}, you have been successfully registered!")

@app.post('/register/faceid')
def register(user: str):
    '''
    Path operation funtion,  allows face id registration
    '''
    facial_register(user)
    users_faceid.append(user)
    return f"{user}, face ID successfully registered"

@app.get('/login')
def login(username: str, password: str):
    '''
    Path operation funtion,  allows traditional login
    '''
    for log in users:
        if log.username == username:
            if log.password == password:
                return "Hi! Welcome home" 
            raise HTTPException(status_code=404, detail="Incorrect password")
        raise HTTPException(status_code=404, detail="User not found")

@app.get('/login/faceid')
def login(username: str):
    '''
    Path operation funtion,  allows face id login
    '''
    for log in users_faceid:
        if log == username:
            if facial_log(username) == 1:
                return "Face ID verificated. Hi! Welcome home"
            else:
                raise HTTPException(status_code=404, detail=f"We're not sure that you're {username}, try again")
    raise HTTPException(status_code=404, detail="User not found")