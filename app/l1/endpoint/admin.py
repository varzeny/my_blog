# endpoint/admin.py

# lib
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# module
import app.l2.authorization as AUTH
import app.l2.database as DB

# definition
router = APIRouter(
    prefix="/admin",
    dependencies=[ Depends(AUTH.admin_only) ]
)
template = Jinja2Templates(directory="app/template/admin")

# endpoint
@router.get("/")
async def get_root(req:Request):
    resp = template.TemplateResponse(
        request=req,
        name="dashboard.html",
        context={},
        status_code=200
    )
    return resp


@router.get("/postwriter")
async def get_postwriter(req:Request, ss:AsyncSession=Depends(DB.get_ss)):
    # 카테고리 목록 같은거 읽어오기
    result = await ss.execute(
        statement=text("SELECT * FROM category"),
        params={}
    )
    resultData = result.mappings().fetchall()
    print( resultData )

    resp = template.TemplateResponse(
        request=req,
        name="post_writer.html",
        context={},
        status_code=200
    )
    return resp



# end of file