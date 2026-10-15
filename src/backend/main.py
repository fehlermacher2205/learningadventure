from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from routers import (
    story, 
    user, 
    profile
)
from db.database import create_table,get_db

# Mostly defensive for circular import in database


from models.user import User, UserSession
from models.profile import Profile
from models.story import StoryPage,Story
from models.goal_action import Action, Goal

from services.InitServices import initAdmin,initProgrammingProfile
from core.exception_handlers import(
    register_exception_handler
)
create_table()



app = FastAPI(
    title= "Welcome to the workshop",
    description="AI assisstant",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
) 
register_exception_handler(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# the credentials let us send cookies to backend - IMPORTANT

app.include_router(story.router, prefix=settings.API_PREFIX)
app.include_router(user.router, prefix=settings.API_PREFIX)
app.include_router(profile.router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    initAdmin()
    initProgrammingProfile()
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)


# init profile