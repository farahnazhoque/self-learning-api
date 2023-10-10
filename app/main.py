from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db

from .routers import post, user, aut

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:  
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='2152')
        cursor = conn.cursor()
        print('Database connection was successful')
        break
    except Exception as error:
        print('Connecting to database failed. The error was ', error)

        
# storing information about posts to retrieve   
my_posts = [{"title": "post 1", "content" : "new content for post 1", "id": 1}, {"title": "fav food", "content": "nuggets", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
    
# import all the paths
app.include_router(post.router) # first app object and go down this route and go down this route

app.include_router(user.router)
app.include_router(aut.router)