# endpoint/common.py

# lib
from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates

# module


# definition
router = APIRouter()
template = Jinja2Templates(directory="app/template/common")

# endpoint
@router.get("/")
async def get_root(req:Request):
    resp = template.TemplateResponse(
        request=req,
        name="landing.html",
        context={},
        status_code=200
    )
    return resp

# end of file