from pydantic import BaseModel,field_validator,model_validator
from datetime import datetime

class Person(BaseModel):
    first_name:str
    last_name:str
    @field_validator('firstname','lastname')
    def names_must_be_captitalized(cls,v):
        if not v.istitle():
            raise ValueError("Names must be capitalised")
        return v
    
class User(BaseModel):
    email:str

    @field_validator('email')
    def normalize_mail(cls,v):
        return v.tolower().strip()

class Product(BaseModel):
    price:str  #4,44

    @field_validator('price',mode='before')
    def parse_price(cls,v):
        if isinstance(v,str):
            return float(v.replace('$','').replace(',','.'))
        return v
    
class DateRange(BaseModel):
    start_Date:datetime
    end_date:datetime

    @model_validator(mode='after')
    def validate_date_range(cls,v):
        if v.start_date>= v.end_date:
            raise ValueError('end_date must be greater than start_date')
        return v
    

