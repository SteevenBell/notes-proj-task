from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import exists

from . import schemas, models, utility


async def get_notes(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
):
    result = await session.execute(
        select(models.Note).options(joinedload(models.Note.board, innerjoin=True))
            .offset(skip)
            .limit(limit)
    )
    return result.scalars().all()


async def create_board(
        session: AsyncSession,
        board: schemas.BoardCreate
):
    db_board = models.Board(**board.model_dump())
    session.add(db_board)
    await session.commit()
    await session.refresh(db_board)

    return db_board


async def delete_board(
        session: AsyncSession,
        board_id: int
) -> int:
    return await utility.delete_one_row_by_id(
        model_entity=models.Board,
        id_for_delete=board_id,
        session=session
    )


async def get_boards(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
):
    results = await session.execute(
        select(models.Board).offset(skip).limit(limit)
    )
    return results.scalars().all()


async def update_board(
        session: AsyncSession,
        board_id: int,
        board_in: schemas.BoardUpdate
):
    board_exist = await session.scalar(
        exists(models.Board.id).where(models.Board.id == board_id).select()
    )
    if board_exist:
        try:
            query = (
                update(models.Board)
                    .where(models.Board.id == board_id)
                    .values(board_in.model_dump(exclude_unset=True))
                    .returning(models.Board)
            )

            result = await session.execute(query)
            await session.flush()

            result = result.scalar()
            await session.commit()

            return result
        except Exception:
            await session.rollback()
            return None

    return None


async def create_note(
        session: AsyncSession,
        board_id: int,
        note_in: schemas.NoteCreate
):
    board_exists = await session.scalar(
        exists(models.Board.id)
            .where(models.Board.id == board_id)
            .select()
    )

    if not board_exists:
        raise NoResultFound(
            "Board is not found"
        )

    note = models.Note(
        board_id=board_id,
        **note_in.model_dump(exclude_unset=True)
    )
    session.add(note)

    await session.commit()
    await session.refresh(note)

    return note


async def update_note(
        session: AsyncSession,
        note_id: int,
        board_id: int,
        note_data: schemas.NoteUpdate
):
    note_board_ids_exists = await utility.is_note_item_of_board_exists(note_id=note_id, board_id=board_id,
                                                                       session=session)

    if not note_board_ids_exists:
        raise NoResultFound(
            "One of the passed identifiers is not found"
        )

    update_note_query = (
        update(models.Note)
            .where(models.Note.id == note_id)
            .values(note_data.model_dump(exclude_unset=True))
            .returning(models.Note)
    )

    try:
        result = await session.execute(update_note_query)
        await session.flush()

        result = result.scalar()
        await session.commit()

        return result

    except Exception:
        await session.rollback()
        return None


async def get_note_by_id(
        session: AsyncSession,
        note_id: int,
        board_id: int
):
    note_exist = await utility.is_note_item_of_board_exists(
        note_id=note_id,
        board_id=board_id,
        session=session
    )

    if not note_exist:
        raise NoResultFound(
            "One of the passed identifiers is not found"
        )

    note = await session.get(models.Note, note_id)
    note.views = note.views + 1
    session.add(note)
    await session.commit()
    await session.refresh(note)

    return note


async def delete_note(
        session: AsyncSession,
        board_id: int,
        note_id: int
) -> int:
    valid_item = await utility.is_note_item_of_board_exists(
        note_id=note_id,
        board_id=board_id,
        session=session
    )

    if not valid_item:
        raise NoResultFound(
            "The note does not reference the board"
        )

    return await utility.delete_one_row_by_id(
        model_entity=models.Note,
        id_for_delete=note_id,
        session=session
    )
