# endpoint/common.py

# lib
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel

# module
import app.l2.authorization as AUTH
import app.l2.database as DB

# definition
router = APIRouter()
template = Jinja2Templates(directory="app/template/common")

# endpoint
@router.get("/favicon.ico")
async def get_favicon():
    return FileResponse( path="app/static/image/icon/favicon.ico" )

@router.get("/")
async def get_root(req:Request):
    resp = template.TemplateResponse(
        request=req,
        name="landing.html",
        context={},
        status_code=200
    )
    return resp

@router.get("/logout")
async def get_logout(req:Request):
    req.state.access_token = AUTH.AccessToken()
    return RedirectResponse(url="/")



# end of file