
################################SChema
from typing import List
from pydantic import BaseModel,ConfigDict
from datetime import datetime



class ActionResponse(BaseModel):
    id: int # this id is fetched from the database after commit and refresh
    type : str
    action : str
    title : str
    value : int
    reasoning :str
    category : str
    skill : str
    created_at : datetime
    
    model_config = ConfigDict(from_attributes=True)
