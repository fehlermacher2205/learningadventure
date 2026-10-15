
from typing import List
from datetime import datetime

from pydantic import BaseModel, Field,ConfigDict
from schemas.profile import ShortProfileResponse
# 1. The shared fields that belong to a User everywhere
class UserBase(BaseModel):
# enforce 7 digit
    matriculation_number: str = Field(
        ..., 
        min_length=7, 
        max_length=7, 
        pattern=r"^\d{7}$",
        description="Matriculation number must be exactly 7 digits."
    )

# Enforce URL-safe usernames right at the base level
    username: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Username can only contain letters, numbers, underscores, and hyphens."
    )
# 2. What you need ONLY when creating a user
# request
class UserCreateRequest(UserBase):
    # todo 
    # we might need password or webmail validation here later
    pass 

# It is possible for a request to fail 
# So it is recommended to distinct between the request and response models

# 3. What you return back to the frontend
class UserPageResponse(UserBase):
    id: int
    created_at: datetime
    profiles: List[ShortProfileResponse] # List of profile ids associated with the user
    is_admin: bool = Field(default=False, description="Indicates if the user has admin privileges.")
    model_config = ConfigDict(from_attributes=True)
class UserLoginResponse(BaseModel):
    username: str
    matriculation_number: str
    token: str

class RegisterRequest(UserBase):
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_-]+$", description="Username can only contain letters, numbers, underscores, and hyphens.")
    matriculation_number: str = Field(..., min_length=7, max_length=7, pattern=r"^\d{7}$", description="Matriculation number must be exactly 7 digits.")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")


class LoginRequest(BaseModel):
    matriculation_number: str = Field(..., min_length=7, max_length=7, pattern=r"^\d{7}$", description="Matriculation number must be exactly 7 digits.")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")
