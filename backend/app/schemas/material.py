from pydantic import BaseModel
class MaterialOut(BaseModel):
    id:int; filename:str; subject:str; status:str; topics:list[str]=[]
class MaterialList(BaseModel):
    items:list[MaterialOut]
