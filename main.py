# .venv\Scripts\activate активация окружения
# uvicorn dz:app --reload запуск фаст апи
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
app = FastAPI()
users: List['User '] = []
class User(BaseModel):
    id: int
    username: str
    age: int
@app.get("/users", response_model=List[User])
async def get_users() -> List[User]:
    return users
@app.post("/user/{username}/{age}", response_model=User)
async def create_user(username: str, age: int) -> User:
    if age < 0:
        raise HTTPException(status_code=400, detail="Возраст не может быть отрицательным")
    new_user_id = len(users) + 1  # Новый ID будет на 1 больше, чем количество пользователей
    new_user = User(id=new_user_id, username=username, age=age)
    users.append(new_user)
    return new_user
@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(user_id: int, username: str, age: int) -> User:
    if age < 0:
        raise HTTPException(status_code=400, detail="Возраст не может быть отрицательным")
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User  was not found")
@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int) -> User:
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User  was not found")