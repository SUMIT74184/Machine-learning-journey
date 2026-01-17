from pydantic import BaseModel,ConfigDict
from typing import List
from datetime import datetime

class Address(BaseModel):
    street:str
    city:str
    zip_code:str

class User(BaseModel):
    id:int
    name:str
    email:str
    is_active:bool=True
    createdAt:datetime
    address:Address
    tags:List[str]=[]

    # model_config=ConfigDict(
    #     json_encoders={datetime:lambda v:v.strftime('%Y-%m-%d %H:%M:%S')}

    # )
user=User(
        id=1,
        name="sumit",
        email='abc@gmail.com',
        createdAt=datetime(2025,3,15,14,3),
        address=Address(
            street="capita road",
            city="san marko",
            zip_code="281293"
        ),
        is_active=False,
        tags=["premium","subscriber"]
    )

python_dict=user.model_dump()
print(user)
print('='*35)
print(python_dict)

print('='*35)
json_str=user.model_dump_json()
print(json_str)


