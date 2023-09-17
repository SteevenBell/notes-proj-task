import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from note_app.database import SessionLocal
from note_app.crud import create_board, create_note
from note_app.schemas import BoardCreate, NoteCreate


async def main():
    session: AsyncSession = SessionLocal()

    for x in range(11):
        board = BoardCreate(**{"name": f"Board {str(x)}"})
        board_created = await create_board(session=session, board=board)

        for i in range(5):
            note_in = NoteCreate(**{
                "title": f"Title {str(x)}-{str(i)}",
                "text": f"Simple text {str(x)}-{str(i)}"
            })
            await create_note(
                session=session,
                board_id=board_created.id,
                note_in=note_in
            )

    await session.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
