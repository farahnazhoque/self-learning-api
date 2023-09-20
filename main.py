from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel): # an extension of the BaseModel class
    title: str # setting the type as string there are many field types tho
    content: str # will try to convert anything to string if it is able to
    published: bool = True # setting a default
    rating: Optional[int] = None # completely optional values for ratings 
  
# storing information about posts to retrieve   
my_posts = [{"title": "post 1", "content" : "new content for post 1", "id": 1}, {"title": "fav food", "content": "nuggets", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post): # ensuring the schema is validated from the front end
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    print(my_posts)
    return {"data" : post_dict}

@app.get("/posts/{id}")
def get_posts_id(id: int, response: Response): # response is added to tweak the response anyway we want it
    post = find_post(id) # we have to convert it to int as it is passed as str
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    return {"post details" : post}