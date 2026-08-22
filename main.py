from fastapi import FastAPI
import json
from fastapi import Path
from fastapi import HTTPException
from fastapi import Query
from pydantic import BaseModel,Field,AnyUrl,computed_field,field_validator
from typing import List,Annotated,Dict, Literal
from fastapi.responses import JSONResponse
from fastapi import Form
from fastapi import Header
from fastapi import File,UploadFile
from fastapi.security import HTTPBearer 
from fastapi import Depends
from router_main import route
from function import calc_fibonacci, calc_factorial,add
from middle import MYMiddleware
from fastapi import Request
from fastapi.responses import Response
from fastapi import Cookie, WebSocket, WebSocketException
from fastapi import status
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app= FastAPI()
security=HTTPBearer()
app.include_router(route)
app.add_middleware(MYMiddleware)

def load_data():
    with open ("patient.json","r") as f:
        return json.load(f)

def save_data(data):
    with open ("patient.json","w") as f:
        return json.dump(data,f)



class Patient(BaseModel):
    id: Annotated[str,Field(...,description="the id of patient")]
    age: Annotated[int,Field(...,gt=0,lt=120,description="age of the patient")]
    height: Annotated[int, Field(...,gt=0,lt=150)]
    gender: Annotated[Literal["male","female"],Field("gender of patient")]
    phone: Annotated[int,Field(...,max_length=12,min_length=10,description="number of patient")]
    url:AnyUrl


class change_data(BaseModel):
        id: Annotated[str,Field(...,description="the id of patient")]
        age: Annotated[int,Field(...,gt=0,lt=120,description="age of the patient")]
        height: Annotated[int, Field(...,gt=0,lt=150)]
        gender: Annotated[Literal["male","female"],Field("gender of patient")]
        phone: Annotated[int,Field(...,max_length=12,min_length=10,description="number of patient")]
        url:AnyUrl

    
@field_validator("email")
@classmethod
def validate(cls,value):
    valid_domails=["hdfc","icic"]
    domain_name=value.split("@")[-1]
    if domain_name not in valid_domails:
        return value

@computed_field
@property
def bmi(self):
    bmi=round(self.weight/(self.height**2),2)
    return bmi



@app.get("/")
def root():
    return "good evening"

@app.get("/about")
def about():
    return "this is all about patients world"

@app.get("/greet")
def greet():
    return "welcome to patients world"


@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/view/{patient_id}")
def get_patient(patient_id:str=Path(...,description="get a particular patient_id",example="PAT1002")):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=200, detail="patient not found")

@app.get("/sort")
def sort(sort_by:str=Query(...,description="sort by height, weight and bmi"),order_by:str=Query(...,description="order by aesc and desc")):
    valid_domain=["height","weight","bmi"]
    if sort_by not in valid_domain:
        return HTTPException(status_code=404,detail="patient not found")
    if order_by not in ["aesc","desc"]:
        return HTTPException(status_code=404,detail="patient not found")
    data=load_data()
    sorted_order=True if order_by == "desc" else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(data,None),reverse=sorted_order)
    return sorted_data

@app.post("/new")
def create_new(patient:Patient):
    data=load_data()
    if patient.id in data:
        return HTTPException(status_code=400,detail="patient already exists")
    else:
        data[patient.id]=patient.model_dump(exclude=["id"])
        save_data(data)
    return JSONResponse(status_code=200, content= "new patient added")

@app.put("/update")
def update_patient(update:change_data,patient_id:str=Path(...,description="updating existing patient")):
    data=load_data()
    if patient_id not in data:
        return HTTPException(status_code=404,detail="patient not found")
    else:
        return data[patient_id]
    existing_user=data[patient_id]
    updated_patient=update.model_dump(exclude=["id"])
    for key,value in updated_patient.items():
        existing_user[key]=value
    existing_user[id]=patient_id
    updated_new_patient_object=Patient(**existing_user)
    existing_user=updated_new_patient_object.model_dump(exclude=["id"])
    data[patient_id]=existing_user
    save_data(data)
    return JSONResponse(status_code=200,content="patient updated successfully")

@app.delete("/delete")
def delete_patient(patient_id:str=Path(...,description="patient_id that need to be deleted")):
    data=load_data()
    if patient_id not in data:
        return HTTPException(status_code=404,detail="patient not found")
    else:
        return data[patient_id]
    wrong_patient=data[patient_id]
    del wrong_patient
    save_data(data)
    return JSONResponse(status_code=200,content="patient deleted successfully")

@app.post("/login")
def login(username:str=Form(...),password:str=Form(...)):
    return {"username":username,"password":password}

@app.get("/secure")
def secure_api(token:str=Header(...)):
    return {"token":token}

@app.post("/upload")
def upload(file:UploadFile=File()):
    return{"file":file.content_type}

@app.post("/authorize")
def auth(token=Depends(security)):
    return{"token":token}

@app.post("/fibonacci")
def fibonacci(n:int):
    return calc_fibonacci(n)

@app.post("/factorial")
def factorial(n:int):
    return calc_factorial(n) 

@app.post("/sum")
def total(n:int):
    return add(n)


@app.post("/create-cookie")
def create_cookies(response:Response):
    response.set_cookie(key="fake-session",value="fake-session-value")
    return {"message":"come to darkside we have cookies"}

    



html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")