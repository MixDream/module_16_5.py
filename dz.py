from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users: List['User '] = []

class User(BaseModel):
    id: int
    username: str
    age: int

# Создание нескольких пользователей
@app.on_event("startup")
async def startup_event():
    users.append(User(id=1, username="UrbanUser ", age=24))
    users.append(User(id=2, username="UrbanTest", age=22))
    users.append(User(id=3, username="Capybara", age=60))

@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def read_user(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

@app.post("/user/{username}/{age}", response_model=User )
async def create_user(username: str, age: int) -> User:
    if age < 0:
        raise HTTPException(status_code=400, detail="Возраст не может быть отрицательным")
    new_user_id = len(users) + 1
    new_user = User(id=new_user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", response_model=User )
async def update_user(user_id: int, username: str, age: int) -> User:
    if age < 0:
        raise HTTPException(status_code=400, detail="Возраст не может быть отрицательным")
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User  not found")

@app.delete("/user/{user_id}", response_model=User )
async def delete_user(user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User  not found")
