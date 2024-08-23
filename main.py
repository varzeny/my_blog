# main.py

# lib
from fastapi import FastAPI, staticfiles

# module
from app.l1.middleware.access import AccessMiddleware
import app.l2.util as UTIL
import app.l2.database as DB
import app.l2.authorization as AUTH

from app.l1.endpoint.common import router as common_router
from app.l1.endpoint.admin import router as admin_router
from app.l1.endpoint.guest import router as guest_router

# definition
async def startup():
    # database
    await DB.setup( app.state.config["database"] )

    # authorization
    AUTH.setup( app.state.config["authorization"] )

async def shutdown():
    return

# app
app = FastAPI(
    on_startup=[ startup ],
    on_shutdown=[ shutdown ]
)

# config
app.state.config = UTIL.read_json_from_file("config.json")

# mount
app.mount(
    path="/static",
    app=staticfiles.StaticFiles(directory="app/static")
)

# middleware
app.add_middleware( AccessMiddleware )

# router
app.include_router( common_router )
app.include_router( admin_router )
app.include_router( guest_router )





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9100, reload=True)


