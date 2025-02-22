from pydantic import BaseModel
from db.db import conn
from models.models import categorias


class Categoria(BaseModel):
    id: int | None = None
    nombre: str
    descripcion: str

    def categoria_schema(categoria) -> dict:
        return {
            "id": categoria.id,
            "nombre": categoria.nombre,
            "descripcion": categoria.descripcion,
        }

    def categorias_schemas(categorias) -> list:
        return [Categoria.categoria_schema(categoria) for categoria in categorias]

    def get_categoria(id: int) -> dict:
        query = categorias.select().where(categorias.c.id == id)
        return Categoria.categoria_schema(conn.execute(query).first())
