from core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import job, story
from db.database import create_tables

#This creates the tables if they do not exists
create_tables()

app = FastAPI(
    title="Choose Your Own Adventure",
    description="Choose Your Own Adventure Backend API",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job.router, prefix=settings.API_PREFIX)
app.include_router(story.router, prefix=settings.API_PREFIX)

# Standard python practice, only execute this if the file is direcly called
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
