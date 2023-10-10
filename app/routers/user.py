from .. import models, utils, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix="/users", # + id
    tags= ["Users"] # grouping
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) 
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): # pydantic user
    
    # hash the password
    hashed_password = utils.hash_password(user.password) # creating a hashed password
    user.password = hashed_password # updating the password to the hashed version
    new_user = models.User(**user.dict()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} is not found!")
    return user