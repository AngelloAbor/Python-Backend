import stat
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt 
from passlib.context import CryptContext
from datetime import datetime, timedelta



algoritmo = "HS256"
access_token_duration = 1

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt_context = CryptContext(schemes=["bcrypt"])



class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

user_db = {
    "abor":{
        "username": "abor",
        "full_name": "Angello orrego",
        "email": "angello.bor@gmail.com",
        "disabled": False,
        "password": "$2a$12$hb10tDTK1qSXbl0Mp6OfW.Cj.V7rQb3cGHl67.fhVQ3GvRTkq0za."
    },
    "jose":{
        "username": "jose",
        "full_name": "Jose Perez",
        "email": "jose123@gmail.com",
        "disabled": True,
        "password": "$2a$12$VrCg5hMl7efjCRmvwYL5JeIl.JcEJouuOo5OLaESXB.GNgE9JZH6m",
    }
}

def search_user_db(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    else:
        return None

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_data = user_db.get(form.username)
    if not user_data:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    
    user = search_user_db(form.username)

    crypt_context.verify(form.password, "$2a$12$hb10tDTK1qSXbl0Mp6OfW.Cj.V7rQb3cGHl67.fhVQ3GvRTkq0za.")

    if not crypt_context.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    

    

    access_token ={"sub": user.username, "exp": datetime.utcnow() + timedelta(minutes=access_token_duration)}

    return {"access_token": jwt.encode(access_token, algorithm=algoritmo), "token_type": "bearer"}


async def auth_user(token: str = Depends(oauth2)):
    try:
        username= jwt.decode(token, algorithm=algoritmo).get("sub")
        if username is None:
            raise HTTPException(status_code=stat.http_401_unauthorized, detail="Credenciales de autenticación invalidas", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=stat.http_401_unauthorized, detail="Credenciales de autenticación invalidas", headers={"WWW-Authenticate": "Bearer"})

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=stat.http_400_bad_request, detail="Usuario inactivo")  
    return user

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user