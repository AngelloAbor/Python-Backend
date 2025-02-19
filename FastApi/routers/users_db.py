from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(
    prefix="/userdb",
    tags=["userdb"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.local.users.find())


@router.get("/{id}", response_model=User)
async def get_user_by_id(id: str):
    user = search_user("_id", ObjectId(id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    """Crea un nuevo usuario en la base de datos."""
    if search_user("email", user.email):  # Verifica si el email ya existe
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    user_dict = user.dict(exclude={"id"})  # Excluye 'id' para evitar errores en MongoDB
    inserted = db_client.users.insert_one(user_dict)  # Inserta el usuario

    return search_user("_id", inserted.inserted_id)  # Devuelve el usuario insertado


@router.put("/{id}", response_model=User)
async def update_user(id: str, user: User):
    """Actualiza los datos de un usuario."""
    if not user.id or user.id != id:  # Asegura que el id en el cuerpo coincida con el ID de la URL
        raise HTTPException(status_code=400, detail="ID inválido o no coincide con el ID del cuerpo de la solicitud")

    user_dict = user.dict(exclude={"id"})
    result = db_client.users.find_one_and_replace({"_id": ObjectId(id)}, user_dict)

    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Retorna el usuario actualizado
    return search_user("_id", ObjectId(id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    """Elimina un usuario por su ID."""
    result = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}

# 🔹 Helper Functions
def search_user(field: str, key):
    """Busca un usuario en la base de datos por campo (ID o email)."""
    user = db_client.users.find_one({field: key})
    if user:
        user["id"] = str(user["_id"])  # Convierte el ObjectId a string
        return User(**user_schema(user))  # Asegúrate de que user_schema esté manejando bien este caso
    return None
