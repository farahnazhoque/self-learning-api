from pydantic import BaseModel


class PostBase(BaseModel): # an extension of the BaseModel class -> Schema
    """
    THis ensures that the user wants to create a post, the request will only go through if it has a title and content in the body
    """
    title: str # setting the type as string there are many field types tho
    content: str # will try to convert anything to string if it is able to
    published: bool = True # setting a default
    
class PostCreate(PostBase):
    """
    This is an extension the the PostBase schema class.
    It will inherit all its attributes.
    As updating and creating a post requires fundamentally the same 
    fields, we will use this class mainly for both.
    """
    pass
