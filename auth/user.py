from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from db.db import conn
from decouple import config
from models.models import usuarios
from schemas.usuario_schema import Usuario

oauth_schema = OAuth2PasswordBearer(tokenUrl="login")

ALGORITHM = config("ALGORITHM")
SECRETE_KEY = config("SECRET_KEY")


async def auth_user(token: str = Depends(oauth_schema)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        email = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM]).get("email")
        if email is None:
            raise exception
    except jwt.PyJWTError:
        raise exception
    return Usuario.usuario_schema(
        conn.execute(usuarios.select().where(usuarios.c.email == email)).fetchone()
    )


async def user_actual(current: Usuario = Depends(auth_user)):
    return current
