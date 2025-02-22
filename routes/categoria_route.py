from fastapi import APIRouter, HTTPException
from db.db import conn
from models.models import categorias
from schemas.categoria_schema import Categoria

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_categorias():

    categorias_src = Categoria.categorias_schemas(
        conn.execute(categorias.select().order_by(categorias.c.nombre)).fetchall()
    )

    if not categorias_src:
        raise HTTPException(status_code=404, detail="No hay categorias registradas")

    return categorias_src


@router.get("/{id}")
async def get_categoria(id: int):

    categoria_src = Categoria.categoria_schema(
        conn.execute(categorias.select().where(categorias.c.id == id)).fetchone()
    )

    if not categoria_src:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return categoria_src


@router.post("/")
async def create_categoria(categoria: Categoria):

    nueva_categoria = Categoria.categoria_schema(categoria)
    result = conn.execute(categorias.insert().values(nueva_categoria))
    conn.commit()

    return Categoria.categoria_schema(
        conn.execute(
            categorias.select().where(categorias.c.id == result.lastrowid)
        ).first()
    )


@router.put("/{id}")
async def update_categoria(id: int, categoria: Categoria):

    categoria_src = conn.execute(
        categorias.select().where(categorias.c.id == id)
    ).fetchone()

    if not categoria_src:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    categoria_src = Categoria.categoria_schema(categoria)

    categoria_src["id"] = id

    conn.execute(categorias.update().values(categoria_src).where(categorias.c.id == id))
    conn.commit()

    return {"id": id, **categoria.dict()}


@router.delete("/{id}")
async def delete_categoria(id: int):

    categoria_src = conn.execute(
        categorias.select().where(categorias.c.id == id)
    ).fetchone()

    if not categoria_src:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    conn.execute(categorias.delete().where(categorias.c.id == id))
    conn.commit()

    return {"message": "Categoria eliminada"}
