from fastapi import APIRouter, Response
from config.db import conn
from models.user import users
from schemas.user import User
from sqlalchemy import select, delete, update
from starlette.status import HTTP_204_NO_CONTENT
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
user = APIRouter()


@user.get("/users", response_model=list[User], tags=["Users"])
def get_users():
    return conn.execute(select(users)).mappings().all()


@user.post("/users", tags=["Users"])
def create_user(usuario: User):
    new_user = dict({"name": usuario.name, "email": usuario.email})
    new_user["password"] = f.encrypt(usuario.password.encode("utf-8"))
    result = conn.execute(users.insert().values(new_user))
    print(result)
    return "User created successfully"


@user.get("/users/{id}", response_model=User, tags=["Users"])
def get_user(id: str):
    row_as_dict = conn.execute(select(users).where(users.c.id == id)).mappings().all()
    print(row_as_dict)
    return row_as_dict


@user.put("/users/{id}", tags=["Users"])
def update_user(id: str, usuario: User):
    conn.execute(update(users).where(users.c.id == id).values(name=usuario.name, email=usuario.email,
                                                              password=f.encrypt(usuario.password.encode("utf-8"))))
    return "User updated"


@user.delete("/users/{id}", status_code=HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(id: str):
    stmt = conn.execute(delete(users).where(users.c.id == id))
    print(stmt)
    return Response(status_code=HTTP_204_NO_CONTENT)
