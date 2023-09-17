from sqlalchemy import and_, delete
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import exists
from . import models


async def is_note_item_of_board_exists(
        note_id: int,
        board_id: int,
        session: AsyncSession
) -> bool:
    return await session.scalar(
        exists(models.Note.id).where(
            and_(
                models.Note.id == note_id,
                models.Note.board_id == board_id
            )
        ).select()
    )


async def delete_one_row_by_id(
        model_entity: DeclarativeBase,
        id_for_delete: int,
        session: AsyncSession
) -> int:
    """
    Deletes an object
    :param model_entity:
    :param id_for_delete:
    :param session:
    :return: int,
            -1 - if an error occurred
            0 - if no row was deleted
            1 - successful completion of the function, one requested row was deleted
    """
    query = (
        delete(model_entity)
            .where(model_entity.id == id_for_delete)
            .returning(model_entity.id)
    )

    try:
        result = await session.execute(query)
        await session.flush()

        rows_retrieved = len(result.scalars().all())
        if rows_retrieved == 0:
            return rows_retrieved

        await session.commit()
        return rows_retrieved
    except Exception as e:
        print(e)
        await session.rollback()
        return -1
