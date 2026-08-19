from fastapi import APIRouter

route=APIRouter()

@route.post("/register")
def register(name:str, password:str):
    return {"name":name,"password":password}

@route.post("/add")
def add(additional_details:str):
    return {"additional_detalis":additional_details}