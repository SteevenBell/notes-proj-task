from note_app.database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from note_app import schemas, crud

app = FastAPI()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@app.get("/boards/", response_model=list[schemas.Board])
async def get_boards(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    boards = await crud.get_boards(db, skip, limit)
    return boards


@app.post("/boards/", response_model=schemas.Board)
async def create_board(
        board_create: schemas.BoardCreate,
        db: AsyncSession = Depends(get_db)
):
    board = await crud.create_board(db, board_create)
    return board


@app.put("/boards/{board_id}/", response_model=schemas.Board)
async def update_board(
        board_id: int,
        board_in: schemas.BoardUpdate,
        db: AsyncSession = Depends(get_db)
):
    updated_board = await crud.update_board(
        session=db,
        board_id=board_id,
        board_in=board_in
    )

    if not updated_board:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error during data update"
        )
    return updated_board


@app.delete("/boards/{board_id}/")
async def delete_board(
        board_id: int,
        db: AsyncSession = Depends(get_db)
):
    deleted_rows = await crud.delete_board(
        session=db,
        board_id=board_id
    )

    if deleted_rows == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    elif deleted_rows == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/boards/{board_id}/notes/", response_model=schemas.Note)
async def create_note(
        board_id: int,
        note_body: schemas.NoteCreate,
        db: AsyncSession = Depends(get_db)
):
    try:
        note = await crud.create_note(
            session=db,
            board_id=board_id,
            note_in=note_body
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

    return note


@app.get("/boards/{board_id}/notes/{note_id}/", response_model=schemas.Note)
async def get_note_by_id(
        board_id: int,
        note_id: int,
        db: AsyncSession = Depends(get_db)
):
    try:
        note = await crud.get_note_by_id(
            session=db,
            note_id=note_id,
            board_id=board_id
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return note


@app.put("/boards/{board_id}/notes/{note_id}/", response_model=schemas.Note)
async def update_note(
        board_id: int,
        note_id: int,
        note_body: schemas.NoteUpdate,
        db: AsyncSession = Depends(get_db)
):
    try:
        note_upd = await crud.update_note(
            session=db,
            note_id=note_id,
            board_id=board_id,
            note_data=note_body
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect parameters"
        )

    if not note_upd:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating data"
        )

    return note_upd


@app.delete("/boards/{board_id}/notes/{note_id}/")
async def delete_note(
        board_id: int,
        note_id: int,
        db: AsyncSession = Depends(get_db)
):
    try:
        deleted_rows = await crud.delete_note(
            session=db,
            board_id=board_id,
            note_id=note_id
        )
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.__str__()
        )

    if deleted_rows == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )
    elif deleted_rows == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/notes/", response_model=list[schemas.NoteBoardOut])
async def read_notes(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    notes = await crud.get_notes(db, skip, limit)
    return notes
