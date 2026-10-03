from pydantic import BaseModel, EmailStr, Field
class RegisterRequest(BaseModel):
    name:str=Field(min_length=2,max_length=120)
    email:EmailStr
    password:str=Field(min_length=6,max_length=128)
    course:str="Computer Science"
    semester:str="6"
class LoginRequest(BaseModel):
    email:EmailStr
    password:str
class StudentOut(BaseModel):
    id:int; name:str; email:EmailStr; course:str; semester:str
    model_config={"from_attributes":True}
