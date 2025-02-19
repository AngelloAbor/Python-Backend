def user_schema(user: dict) -> dict:
    """Convierte un documento de MongoDB en un diccionario con formato seguro."""
    if not user:
        return {}  # Devuelve un objeto vacío si el usuario no existe

    # Utiliza valores por defecto más claros
    return {
        "id": str(user.get("_id", "")),  # Convierte ObjectId a string, vacío si no existe
        "username": user.get("username", "N/A"),  # Evita valores vacíos con un valor predeterminado
        "email": user.get("email", "No proporcionado")  # Evita valores vacíos con un valor predeterminado
    }

def users_schema(users) -> list:
    """Convierte una lista de documentos de MongoDB en una lista de diccionarios."""
    if isinstance(users, list):
        return [user_schema(user) for user in users if user]  # Filtra valores nulos
    # Si `users` es un cursor de MongoDB, conviértelo a lista
    return [user_schema(user) for user in users]  # Si es un cursor, no es necesario filtrar por `user`
