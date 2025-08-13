from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class StoryJobBase(BaseModel):
    theme: str

class StoryJobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    story_id: Optional[int]=None
    completed_at: Optional[datetime]=None
    error: Optional[str]=None

    class Config:
        from_attributes = True

# Convention: This allows to use JobStoryBase in other places and keep this for api creation call extension later
class StoryJobCreate(StoryJobBase):
    pass
