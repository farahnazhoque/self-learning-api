from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from . import models, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db

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

@app.get("/")
def root():
    return {"message": "Hello World"}
    

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).all()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)): # ensuring the schema is validated from the front end 
    # post_dict = post.dict()
    # post_dict["id"] = randrange(0, 100000)
    # my_posts.append(post_dict)
    # print(my_posts)
    
    # new_post = models.Posts(title=post.title, content = post.content, published = post.published) 
    new_post = models.Posts(**post.dict()) # we are unpacking the dictionary post just as above as it will get redundant if there were so many fields
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # returninng the newly created post
    return {"data" : new_post}

@app.get("/posts/{id}")
def get_posts_id(id: int, db: Session = Depends(get_db)): # response is added to tweak the response anyway we want it
    # post = find_post(id) # we have to convert it to int as it is passed as str
    post = db.query(models.Posts).filter(models.Posts.id == id).first() # first instance and send this
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    return {"post details" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # index = find_index(id)
    
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    # my_posts.pop(index)
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    post = db.query(models.Posts).filter(models.Posts.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    post.delete(synchronize_session = False) # most efficient and reliable
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)): # ensuring the schema is verified so nothing else is allowed to change
    # index = find_index(id)
    
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    # post_dict = post.dict()  # creating the newly sent data into a dictionary
    # post_dict["id"] = id # adding the id to the newly created dictionary
    # my_posts[index] = post_dict # removing the old item in the array and replacing it with the new dictionary
    # return {"data" : post_dict} # returning the newly updated dictionary
    
    post_query = db.query(models.Posts).filter(models.Posts.id == id) # retrieving the posts using id and this is the query of doing so
    
    posts = post_query.first() # grabbing the first instance if a post does exist
    
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    post_query.update(post.dict(), synchronize_session = False)
    db.commit()
    
    return {"data" : post_query.first()}
    
