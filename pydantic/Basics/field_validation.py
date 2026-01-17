from pydantic import BaseModel,field_validator,model_validator

class User(BaseModel):
    username:str

    @field_validator('username')
    def username_length(cls,v):
        if len(v)<4:
            raise ValueError("username must be atleast 4 characters")
        return v
    

class SignupData(BaseModel):
    password:str
    confirm_password:str

    @model_validator(mode='after')
    def password_match(cls,v):
        if v.password!=v.confirm_password:
            raise ValueError("Password do not match, please check it again and retry")
        return v
    