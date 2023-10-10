from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Posts(Base):
    __tablename__ = 'posts'
    """
    Responsible for defining the columns of our posts table within postgres
    """
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable= False)
    published = Column(Boolean, server_default= 'True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    """
    Creating a User class that will store user information
    in the user table
    """
    
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, nullable= False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
