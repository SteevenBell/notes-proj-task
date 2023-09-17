from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:admin@127.0.0.1:5432/notes_db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
