from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import asyncio
from fastapi import HTTPException
import time
from fastapi.responses import JSONResponse

class MYMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request,call_next):
        print("before request")
        response=await call_next(request)
        print("after request")
        return response

class AUTHMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request, call_next):
        token=request.headers.get("Authorization")
        if token!="Bearer my-secret-token":
            return HTTPException(status_code=401,detail="unauthorizd")
        else:
            response=await call_next(request)
            return response

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request,call_next):
        start=time.perf_counter()
        response=await call_next(request)
        end=time.perf_counter()
        process_time=end-start
        print(end-start)
        return response      

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,request:Request,call_next):
        try:
            response=await call_next(request)
            return response
        except Exception as e:
            return JSONResponse(status_code=500,content="intenal server error")
        