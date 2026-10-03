from pydantic import BaseModel, Field
class QuizGenerate(BaseModel):
    subject:str="Operating Systems"
    topic:str="Deadlocks"
    number_of_questions:int=Field(default=5,ge=1,le=20)
    difficulty:str="adaptive"
    question_type:str="mcq"
class AnswerItem(BaseModel):
    question_id:int
    answer:str
    time_taken:float=0
class QuizSubmit(BaseModel):
    answers:list[AnswerItem]
