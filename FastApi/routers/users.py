from typing import Union

from fastapi import  HTTPException
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter( prefix="/users",
                    tags=["users"],
                    responses={404: {"description": "Not found"}})

#entidad users

class User(BaseModel):
    id: int
    name: str
    lastname: str
    edad: int

users_list=[User(id=1, name="Angello", lastname="Orrego",edad= 26),
            User(id=2, name="Jenifer", lastname="Savoy",edad= 23),
            User(id=3, name="Tocino", lastname="Bull",edad= 4),
            User(id=4, name="Kissie", lastname="Chiquita",edad= 2),
            User(id=5, name="Bingo", lastname="Ringo",edad= 1)]
@router.get("/usersjson")
async def usersjson ():
    return [ { "name": "Angello", "lastname": "Orrego", "edad":26},
            { "name": "Jenifer", "lastname": "Savoy", "edad":23},
            { "name": "tocino", "lastname": "BULL", "edad":4}]

@router.get("/")
async def users():
    return users_list


#buscar por path cuando queremos pedir un dato de forma oblihatoria
@router.get("/{id}")
async def user(id: int):
    return search_user(id)

#buscar por query id
@router.get("/")
async def user(id: int):
    return search_user(id)

#buscar por query Name
@router.get("/username")
async def user(name: str):
    users = filter(lambda user: user.name == name, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "usuario no encontrado"}
    

@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="el usuario ya existe")
    else:
        users_list.append(user)
        return{"Usuario añadido"}
    
@router.put("/")
async def user(user: User):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "no se a podido actualizar"}
    
    

@router.delete("/{id}")
async def user(id: int):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            return {"usuario eliminado"}
        found = True
    if not found:
            return {"no se ha encontrado al usuario"}


def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return{"error":"No se encuentra el usuario"}
