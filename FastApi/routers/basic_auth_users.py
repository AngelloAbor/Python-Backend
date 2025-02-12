import stat
from fastapi import Depends, APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "1234"
    },
    "jose":{
        "username": "jose",
        "full_name": "Jose Perez",
        "email": "jose123@gmail.com",
        "disabled": True,
        "password": "4321",
    }
}

def search_user(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    else:
        return None
    
def search_user_db(username: str):
    if username in user_db:
        return UserDB(**user_db[username])
    else:
        return None
    
    

async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=stat.http_401_unauthorized, detail="Credenciales de autenticación invalidas", headers={"www-Authenticate": "bearer"})
    if user.disabled:
        raise HTTPException(status_code=stat.http_400_bad_request, detail="Usuario inactivo")  
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_data = user_db.get(form.username)
    if not user_data:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    
    user = search_user(form.username)
    if form.password != user.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user