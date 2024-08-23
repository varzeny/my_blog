# database/__init__.py

# lib
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
from sqlalchemy import text

# attribute
DB_URL = None
ENGINE = None
SESSION = None

# method
async def setup(config:dict):
    global DB_URL, ENGINE, SESSION
    DB_URL=config["url"]
    ENGINE=create_async_engine(DB_URL)
    SESSION=async_sessionmaker(
        bind=ENGINE,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # # 앱에서 기본적으로 불러와야 할것들
    # async with SESSION() as ss:
    #     try:
    #         result = await ss.execute(
    #             statement=text("SELECT * FROM account"),
    #             params={}
    #         )
    #         resultData = result.mappings().fetchone()
    #         print( resultData )

    #     except Exception as e:
    #         print("ERROR from setup : ", e)
            



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