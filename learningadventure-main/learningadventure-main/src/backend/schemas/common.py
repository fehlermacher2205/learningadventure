from typing import List
from pydantic import BaseModel
from datetime import datetime
class MessageResponse(BaseModel):
    message: str