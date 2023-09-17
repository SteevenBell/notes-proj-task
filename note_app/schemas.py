from typing import Union
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ModificationDateModel(BaseModel):
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None


class NoteBase(BaseModel):
    title: str
    text: Union[str, None] = None


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class Note(ModificationDateModel, NoteBase):
    id: int
    board_id: int
    views: int

    model_config = ConfigDict(from_attributes=True)


class BoardBase(BaseModel):
    name: str


class BoardCreate(BoardBase):
    pass


class BoardUpdate(BoardBase):
    pass


class Board(ModificationDateModel, BoardBase):
    id: int
    notes: list[Note] = []

    model_config = ConfigDict(from_attributes=True)


class BoardWithoutNotes(ModificationDateModel, BoardBase):
    id: int


class NoteBoardOut(Note):
    board: BoardWithoutNotes
    board_id: int = Field(exclude=True)
