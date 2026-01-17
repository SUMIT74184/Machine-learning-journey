from pydantic import BaseModel,computed_field,Field

class Product(BaseModel):
    price:float
    quantity:int

    @computed_field
    @property
    def total_price(self)-> float:
        return self.price*self.quantity
    

class Booking(BaseModel):
    user_id:int
    room_id:int
    nights:int = Field(...,ge=1)
    rate_per_night:float

    @computed_field
    @property
    def total_cost(self)->float:
        return self.nights*self.rate_per_night
    
booking=Booking(
    user_id=101,
    room_id=233,
    nights=4,
    rate_per_night=2000
)
print(booking.total_cost)
# printing what's going inside the model
print(booking.model_dump())