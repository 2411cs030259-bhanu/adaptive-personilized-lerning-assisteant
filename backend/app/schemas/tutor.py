from pydantic import BaseModel, Field
class TutorAsk(BaseModel):
    question:str=Field(min_length=2,max_length=2000)
class TutorResponse(BaseModel):
    answer:str
    sources:list[str]=[]
    mode:str
