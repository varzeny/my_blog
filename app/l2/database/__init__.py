# database/__init__.py

# lib
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager

# attribute
DB_URL = None
ENGINE = None
SESSION = None

# method
def setup(config:dict):
    global DB_URL, ENGINE, SESSION
    DB_URL=config["url"]
    ENGINE=create_async_engine(DB_URL)
    SESSION=async_sessionmaker(
        bind=ENGINE,
        class_=AsyncSession,
        expire_on_commit=False
    )

# dependency
async def get_ss():
    try:
        ss:AsyncSession = SESSION()
        yield ss
    except Exception as e:
        print("ERROR from get_ss : ", e)
        await ss.rollback()
    finally:
        await ss.close()




# end of file