# access.py

# lib
from typing import Callable, Awaitable
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

# module
import app.l2.authorization as AUTH

# definition
class AccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:

        # 요청 전
        decoded_data = AUTH.get_token_from_cookie(req, "access_token")
        if decoded_data:
            req.state.access_token = AUTH.AccessToken(**decoded_data)
        else:
            req.state.access_token = AUTH.AccessToken()

        # 대기 중
        resp:Response = await call_next(req)

        # 요청 후
        access_token:AUTH.AccessToken = req.state.access_token
        access_token.extend_token()

        return AUTH.put_token_to_cookie(resp, access_token)

# end of file