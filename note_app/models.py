from sqlalchemy.orm import DeclarativeBase, relationship, backref
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime


class BaseModel(DeclarativeBase):
    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Board(BaseModel):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)

    notes = relationship(
        "Note",
        backref="board",
        lazy="selectin",
        cascade="all,delete"
    )


class Note(BaseModel):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    text = Column(Text)
    views = Column(Integer, nullable=False, default=0)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
