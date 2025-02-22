from pydantic import BaseModel
from datetime import date


class Usuario(BaseModel):
    id: int | None = None
    nombre: str
    email: str
    contrasena: str
    direccion: str
    telefono: str
    es_admin: bool | None = False
    es_activo: bool | None = True
    fecha_creacion: date | None = date.today()
    fecha_actualizacion: date | None = date.today()
    acepta_mails: bool | None = True

    def usuario_schema(usuario) -> dict:
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "direccion": usuario.direccion,
            "telefono": usuario.telefono,
            "es_admin": usuario.es_admin,
            "es_activo": usuario.es_activo,
            "fecha_creacion": usuario.fecha_creacion,
            "fecha_actualizacion": usuario.fecha_actualizacion,
            "acepta_mails": usuario.acepta_mails,
        }

    def usuarios_schemas(usuarios) -> list:
        return [Usuario.usuario_schema(usuario) for usuario in usuarios]

    def usuario_schema_db(usuario) -> dict:
        return {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email,
            "contrasena": usuario.contrasena,
            "direccion": usuario.direccion,
            "telefono": usuario.telefono,
            "es_admin": usuario.es_admin,
            "es_activo": usuario.es_activo,
            "fecha_creacion": usuario.fecha_creacion,
            "fecha_actualizacion": usuario.fecha_actualizacion,
            "acepta_mails": usuario.acepta_mails,
        }

    def usuarios_schemas_db(usuarios) -> list:
        return [Usuario.usuario_schema_db(usuario) for usuario in usuarios]
