from pydantic import BaseModel
from typing import Optional,List,Union

# Optional Nested Models

class Address(BaseModel):
    street:str
    city:str
    postal_code:str


class Company(BaseModel):
    name:str
    address:Optional[Address]=None


class Employee(BaseModel):
    name:str
    company:Optional[Company]=None

    # Mixed Datatypes

class TextContent(BaseModel):
    type:str="text"
    content:str

class ImageContent(BaseModel):
    type:str="Image"
    url:str
    alt_text:str

class Article(BaseModel):
    title:str
    sections:List[Union[TextContent,ImageContent]]


    # Deeply Nested Structure

class Country(BaseModel):
    name:str
    code:str

class State(BaseModel):
    name:str
    code:str
    country:Country

class City(BaseModel):
    name:str
    state:State

class Address1(BaseModel):
    street:str
    city:City
    postal_code:str

class Organization(BaseModel):
    name:str
    head_quarter:Address1
    branches:List[Address1]=[]