from pydantic import BaseModel
from typing import List,Dict,Optional

class Cart(BaseModel):
    user_id:int
    items:List[str]
    quantities:Dict[str,int]
    image_url:Optional[str]

class BlogPost(BaseModel):
    title:str
    content:str
    image_url:Optional[str] = None


cart_data={
    "user_id":101,
    "items":["laptop","Mouse","SMPS"],
    "quantities":{"laptop":1,"Mouse":2,"Keyboard":3}  
}

print(cart_data)

BlogPost1=BlogPost(title="true sense",content="description",image_url="image.png")
print(BlogPost1)