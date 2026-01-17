from typing import List,Optional
from pydantic import BaseModel

class Address(BaseModel):
    street:str
    city:str
    postal_code:str


class User(BaseModel):
    id:int
    name:str
    address:Address   #Using above class here

address=Address(
    street="104 new capita",
    city="trivial rn",
    postal_code="100021"
)

user=User(
    id=1,
    name="sam patricks",
    address=address
)

print(f"printing the address first {address}\n")
print(user)

# Another way of using the Nested model

user_data={
    "id":1,
    "name":"sam patricks",
    "address":{
        "street":"104 new capita",
        "city":"trivial rn",
        "postal_code":"100021"
    }
}

user=User(**user_data)
print("printing the another method sol")
print(user)