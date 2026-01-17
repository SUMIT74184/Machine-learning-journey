from typing import Optional
from pydantic import BaseModel,Field
import re



class Employee(BaseModel):
    id:int
    name:str=Field(
        ...,
        min_length=2,
        max_length=50,
        description="Employee Name",
        examples="Hitesh Chodhary"

    )
    department:Optional[str]="General"
    salary:float=Field(
        ...,
        ge=320000,
        description="salary of the employee"
    )

class User(BaseModel):
    email:str=Field(
        ...,
        regex=r''
    )
    phone:int=Field(
        ...,
        regex=r''
    )
    age:int=Field(
        ...,
        ge=0,
        le=90,
        description="Age in years"
        
    )