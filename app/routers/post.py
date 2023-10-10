from .. import models, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import List

# we no longer have to type /posts in all our methods
router = APIRouter(
    prefix="/posts", # + id
    tags=["Posts"] # groupings
) 

@router.get("/", response_model = List[schemas.Post]) 
# response_model = schemas.Post this will not work as we need list of posts
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Posts).all()
    print(posts)
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post) # adding our response model
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
    return new_post # it is expecting a dictionary type

@router.get("/{id}, response_model = schemas.Post")
def get_posts_id(id: int, db: Session = Depends(get_db)): # response is added to tweak the response anyway we want it
    # post = find_post(id) # we have to convert it to int as it is passed as str
    post = db.query(models.Posts).filter(models.Posts.id == id).first() # first instance and send this
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}, response_model = schemas.Post")
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
    
    post_query.first()