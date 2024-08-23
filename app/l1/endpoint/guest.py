# endpoint/guest.py

# lib
from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from pydantic import BaseModel

# module
import app.l2.authorization as AUTH
import app.l2.database as DB

# definition
router = APIRouter(
    prefix="/guest",
    dependencies=[Depends(AUTH.guest_only)]
)
template = Jinja2Templates(directory="app/template/guest")


# schema
class LoginSchema(BaseModel):
    name_:str|None = None
    password_:str|None = None


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


@router.get("/login-page")
async def get_login_page(req:Request):
    return template.TemplateResponse(
        request=req,
        name="login-page.html",
        context={}
    )

@router.post("/login")
async def post_login(req:Request, reqData:LoginSchema, ss:AsyncSession=Depends(DB.get_ss)):
    print(reqData)
    try:
        result = await ss.execute(
            statement=text("SELECT * FROM account WHERE name_=:a"),
            params={"a":reqData.name_}
        )
        resultData = result.mappings().fetchone()

        if not resultData:
            raise Exception(f"{reqData.name_} doesn't exist")
        
        if not AUTH.verify_hash(reqData.password_, resultData["hashed_password_"]):
            raise Exception("doesn't same password")
        
        req.state.access_token = AUTH.AccessToken(
            account_id_=resultData["id_"],
            account_role_=resultData["role_"]
        )
        return JSONResponse(status_code=200, content={})

    except Exception as e:
        print("ERROR from post_login : ", e)
        return JSONResponse(status_code=401, content={})



# end of file