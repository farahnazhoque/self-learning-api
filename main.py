from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel): # an extension of the BaseModel class
    title: str # setting the type as string there are many field types tho
    content: str # will try to convert anything to string if it is able to
    published: bool = True # setting a default
    rating: Optional[int] = None # completely optional values for ratings 
  
# storing information about posts to retrieve   
my_posts = [{"title": "post 1", "content" : "new content for post 1", "id": 1}, {"title": "fav food", "content": "nuggets", "id" : 2}]

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_post(post: Post): # ensuring the schema is validated from the front end
    print(post.dict())
    return {"data" : post.dict()}