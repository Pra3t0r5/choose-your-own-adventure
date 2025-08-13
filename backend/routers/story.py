import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CompleteStoryNodeResponse,
    CompleteStoryResponse,
    CreateStoryRequest
)
from schemas.job import StoryJobResponse

# adds /stories to URL/api giving URL/api/stories/<endpoint>
router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

# Having a session allows to recover the state of the user's session later
def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create",response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    # BackgroundTasks allow to run tasks in the background independently of the main thread
    background_tasks: BackgroundTasks,
    response: Response,
    # Depends allow to inject dependencies into the function
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id)

    # When we want to create a story, we want to create an async job that creates a story using llm
    job_id = str(uuid.uuid4())

    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        created_at=datetime.now(),
        status="pending"
    )
    # ORM takes care to execute the corresponding SQL query
    db.add(job)
    db.commit()

    # Run the story creation task in the background
    background_tasks.add_task(
        generate_story_task,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )

    # Returning immediately avoids forcing the user to hang with an open connection
    return job

def generate_story_task(job_id: str, theme: str, session_id:str):
    # A new session assures that the main session in the main thread is not blocked by the database operations
    db = SessionLocal()

    try:
        job:Optional[StoryJob] = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        if not job:
            return

        try:
            # First make sure to update the status to processing
            job.status = "processing"
            db.commit()

            story = {} #TODO: Generate story using llm

            job.story_id = 1 #TODO: Update story id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()

@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db:Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()

    if not story:
        raise HTTPException(status_code=404, detail = "Story not found")

    complete_story = build_complete_story_tree(db, story)
    return complete_story

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    pass
