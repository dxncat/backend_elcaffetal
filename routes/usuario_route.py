from fastapi import APIRouter, HTTPException, Depends
from db.db import conn
from models.models import usuarios
from schemas.usuario_schema import Usuario
import jwt
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from decouple import config
from datetime import datetime, timedelta
from auth.user import user_actual

# from utils import send_mail

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = config("ALGORITHM")
SECRETE_KEY = config("SECRET_KEY")
ACCESS_TOKEN_DURATION = int(config("ACCESS_TOKEN_DURATION"))

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_usuarios():

    usuarios_src = Usuario.usuarios_schemas(
        conn.execute(usuarios.select().order_by(usuarios.c.nombre)).fetchall()
    )

    if not usuarios_src:
        raise HTTPException(status_code=404, detail="No hay usuarios registrados")

    return usuarios_src


@router.get("/activos")
async def get_usuarios_activos():

    usuarios_src = Usuario.usuarios_schemas(
        conn.execute(
            usuarios.select()
            .where(usuarios.c.es_activo == True)
            .order_by(usuarios.c.nombre)
        ).fetchall()
    )

    if not usuarios_src:
        raise HTTPException(status_code=404, detail="No hay usuarios activos")

    return usuarios_src


@router.get("/inactivos")
async def get_usuarios_inactivos():

    usuarios_src = Usuario.usuarios_schemas(
        conn.execute(
            usuarios.select()
            .where(usuarios.c.es_activo == False)
            .order_by(usuarios.c.nombre)
        ).fetchall()
    )

    if not usuarios_src:
        raise HTTPException(status_code=404, detail="No hay usuarios inactivos")

    return usuarios_src


@router.get("/allowmails")
async def get_usuarios_allowmails():

    usuarios_src = Usuario.usuarios_schemas(
        conn.execute(
            usuarios.select(usuarios.c.email)
            .where(usuarios.c.acepta_mails == True)
            .order_by(usuarios.c.nombre)
        ).fetchall()
    )

    if not usuarios_src:
        raise HTTPException(status_code=404, detail="No hay usuarios que acepten mails")

    return usuarios_src


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_src = conn.execute(
        usuarios.select().where(usuarios.c.email == form.username)
    ).first()

    if not user_src:
        raise HTTPException(status_code=404, detail="UCredenciales incorrectas")

    user = Usuario.usuario_schema_db(user_src)

    if not crypt_context.verify(form.password, user["contrasena"]):
        raise HTTPException(status_code=404, detail="Credenciales incorrectas")

    access_token = jwt.encode(
        {
            "sub": user["email"],
            "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_DURATION),
        },
        SECRETE_KEY,
        algorithm=ALGORITHM,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register")
async def register(user: Usuario):
    if conn.execute(usuarios.select().where(usuarios.c.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Correo  ya registrado")

    nuevo_usuario = Usuario.usuario_schema_db(user)
    nuevo_usuario["contrasena"] = crypt_context.hash(nuevo_usuario["contrasena"])
    result = conn.execute(usuarios.insert().values(nuevo_usuario))
    conn.commit()

    print(
        Usuario.usuario_schema(
            conn.execute(
                usuarios.select().where(usuarios.c.id == result.lastrowid)
            ).first()
        )
    )

    access_token = jwt.encode(
        {
            "sub": user.email,
            "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_DURATION),
        },
        SECRETE_KEY,
        algorithm=ALGORITHM,
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def me(user: Usuario = Depends(user_actual)):
    return user
