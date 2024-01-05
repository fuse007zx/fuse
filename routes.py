# routes.py
from fastapi import APIRouter, HTTPException
from db import conn, users
from models import User, UserResponse

user = APIRouter()

@user.get("/")
async def read_all_data():
    try:
        result = conn.execute(users.select()).fetchall()
        return [dict(row) for row in result]
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user.get("/{id}", response_model=UserResponse)
async def read_data(id: int):
    try:
        result = conn.execute(users.select().where(users.c.id == id)).fetchone()
        if result:
            return UserResponse(**dict(result))
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user.post("/", response_model=UserResponse)
async def create_user(user: User):
    try:
        print(f"Received user data: {user}")
        result = conn.execute(users.insert().values(
            name=user.name,
            email=user.email,
            password=user.password
        ))
        user_id = result.lastrowid
        created_user = dict(id=user_id, **user.dict())
        return UserResponse(**created_user)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user.put("/{id}", response_model=UserResponse)
async def update_data(id: int, user: User):
    try:
        result = conn.execute(users.update().values(
            name=user.name,
            email=user.email,
            password=user.password
        ).where(users.c.id == id))
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(id=id, **user.dict())
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@user.delete("/{id}", response_model=UserResponse)
async def delete_data(id: int):
    try:
        result = conn.execute(users.delete().where(users.c.id == id))
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(id=id)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
