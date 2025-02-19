from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    # `Optional[str]` ya implica que el valor puede ser `None`, no es necesario usar '| None'
    id: Optional[str] = None  # El id es opcional y se asignará a None si no se proporciona

    # El nombre de usuario debe tener una longitud mínima y máxima, con un ejemplo de valor
    username: str = Field(..., min_length=3, max_length=50, example="user123", description="Nombre de usuario único y entre 3 y 50 caracteres")

    # El campo `email` es validado automáticamente por Pydantic para asegurar que tenga el formato correcto
    email: EmailStr = Field(..., example="usuario@dominio.com", description="Correo electrónico del usuario en formato válido (ejemplo: usuario@dominio.com)")

    # Campo opcional para nombre completo
    full_name: Optional[str] = Field(None, example="Juan Pérez", description="Nombre completo del usuario (opcional)")

    # Puedes añadir más campos según lo que necesites.
    
    class Config:
        # Si deseas que los datos sean tratados como JSON serializables, es buena idea establecer `orm_mode = True`
        orm_mode = True

