from pydantic import BaseModel

class Product(BaseModel):
    id:int
    name:str
    price:float
    in_stock:bool=True


product_one=Product(id=1,name="Laptop",price=223000,in_stock=False)


#Always try it's best to convert the required datatype within the scope
product_two=Product(id="2",name="DESKTOP",price=32000,in_stock=True)

print(product_one)

print(product_two)