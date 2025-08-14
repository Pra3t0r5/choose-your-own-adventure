# Story Model:
#
# story name
# theme
# first option
# children: [go left, go right]
#
# each children option has a text and a new set of childrens

# from time import timezone
#from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
#from sqlalchemy.sql import func
#from sqlalchemy.orm import relationship
#
#from db.database import Base
#
#
#class Story(Base):
#    __tablename__ = "stories"
#
#    id = Column(Integer, primary_key=True, index=True)
#    title = Column(String, index=True)
#    # To track all stories created by a specific web session
#    session_id = Column(String, index=True)
#    created_at = Column(DateTime(timezone=True), default=func.now())
#
#    nodes = relationship("StoryNode", back_populates="story")
#
#
#class StoryNode(Base):
#    __tablename__ = "story_nodes"
#
#    id = Column(Integer, primary_key=True, index=True)
#    story_id = Column(Integer, ForeignKey("stories.id"), index=True)
#    content = Column(String)
#    is_root = Column(Boolean, default=False)
#    is_ending = Column(Boolean, default=False)
#    is_winning = Column(Boolean, default=False)
#    options = Column(JSON, default=list)
#
#    story = relationship("Story", back_populates="nodes")

from typing import Any
from sqlalchemy import DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base

from datetime import datetime

class Story(Base):
    __tablename__ = "stories"

    id: Mapped[int] = mapped_column( primary_key=True, index=True)
    title: Mapped[str] = mapped_column( index=True)
    # To track all stories created by a specific web session
    session_id: Mapped[str] = mapped_column( index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    nodes = relationship("StoryNode", back_populates="story")


class StoryNode(Base):
    __tablename__ = "story_nodes"

    id: Mapped[int] = mapped_column( primary_key=True, index=True)
    story_id: Mapped[int] = mapped_column( ForeignKey("stories.id"), index=True)
    content: Mapped[str] = mapped_column()
    is_root: Mapped[bool] = mapped_column(default=False)
    is_ending: Mapped[bool] = mapped_column(default=False)
    is_winning: Mapped[bool] = mapped_column(default=False)
    options: Mapped[list[dict[str, Any]]] = mapped_column(JSON)
    story = relationship("Story", back_populates="nodes")
